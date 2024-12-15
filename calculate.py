import math
import pandas as pd

# 定义常量
R = 500  # 圆曲线半径，单位：米
l1 = 70  # 第一缓和曲线长度，单位：米
l2 = 100  # 第二缓和曲线长度，单位：米
alpha_deg = 38 + 23 / 60  # 右转角，单位：度
alpha = math.radians(alpha_deg)  # 右转角，转换为弧度
road_width = 30  # 路宽，单位：米
outer_width = 15  # 边桩到曲线的外围距离，单位：米
JD_coords = (6354.618, 5211.539)  # JD点坐标
JD_mileage_km = 10 + 518.66 / 1000  # JD桩的里程，转换为公里的小数形式

# 计算缓和曲线参数
beta0_1_rad = l1 / (2 * R)  # 第一缓和曲线角度，弧度
beta0_2_rad = l2 / (2 * R)  # 第二缓和曲线角度，弧度

# 计算第一段缓和曲线的曲线要素
T1 = l1 / 2 * (1 + (l1 / (2 * R)) * math.tan(alpha / 2))
L1 = R * beta0_1_rad  # 第一缓和曲线长度（弧长公式）

# 计算圆曲线的曲线要素
Lc = R * alpha

# 计算第二段缓和曲线的曲线要素
T2 = l2 / 2 * (1 + (l2 / (2 * R)) * math.tan(alpha / 2))
L2 = R * beta0_2_rad  # 第二缓和曲线长度（弧长公式）

# 合并曲线要素
T_total = T1 + T2 + R * math.tan(alpha / 2)  # 总切线长度
L_total = L1 + Lc + L2  # 总曲线长度
E = R * (1 / math.cos(alpha / 2) - 1)  # 外距
q = L_total - T_total  # 曲线偏移

# 计算ZH点坐标
zh_bearing = 62 + 30 / 60 + 48 / 3600  # ZH到JD的方位角，转换为度
zh_bearing_rad = math.radians(zh_bearing)  # 转换为弧度
x_zh = JD_coords[0] - T_total * math.cos(zh_bearing_rad)
y_zh = JD_coords[1] - T_total * math.sin(zh_bearing_rad)

# 创建中、边桩坐标和桩里程DataFrame
stakes_data = {
    '桩号': [],
    'X 中桩': [],
    'Y 中桩': [],
    'X 边桩': [],
    'Y 边桩': []
}

offset = 0
while offset <= L_total:
    # 计算当前里程桩号
    km = int(JD_mileage_km * 1000 + offset) // 1000  # 计算公里数
    m = (JD_mileage_km * 1000 + offset) % 1000  # 计算米数

    # 计算当前曲线点的方位角
    theta = offset / R  # 根据弧长计算曲线点的偏转角
    current_bearing = zh_bearing_rad + theta

    # 计算中桩和边桩的坐标
    x_center = x_zh + offset * math.cos(current_bearing)
    y_center = y_zh + offset * math.sin(current_bearing)
    x_edge = x_center + outer_width * math.cos(current_bearing + math.pi / 2)
    y_edge = y_center + outer_width * math.sin(current_bearing + math.pi / 2)

    stakes_data['桩号'].append(f"DK{km:03d}+{m:06.2f}")
    stakes_data['X 中桩'].append(x_center)
    stakes_data['Y 中桩'].append(y_center)
    stakes_data['X 边桩'].append(x_edge)
    stakes_data['Y 边桩'].append(y_edge)

    offset += 10  # 步长为10米

# 转换为DataFrame
stakes_df = pd.DataFrame(stakes_data)

# 保存到Excel
with pd.ExcelWriter('curve_elements_and_stakes.xlsx', engine='openpyxl') as writer:
    # 曲线要素
    curve_elements_df = pd.DataFrame({
        '要素': ['T1', 'L1', 'Lc', 'T2', 'L2', 'T_total', 'L_total', 'E', 'q'],
        '值': [T1, L1, Lc, T2, L2, T_total, L_total, E, q]
    })
    curve_elements_df.to_excel(writer, sheet_name='Curve Elements', index=False, float_format="%.4f")
    # 中、边桩坐标
    stakes_df.to_excel(writer, sheet_name='Stakes Coordinates', index=False, float_format="%.4f")

print("Excel文件已生成，包含曲线要素、中、边桩坐标和桩里程。")
