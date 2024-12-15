# 曲线要素与桩号坐标生成工具

此 Python 脚本用于计算公路设计中的曲线要素以及中、边桩坐标，并将结果导出为 Excel 文件。适用于需要进行公路或铁路设计中的曲线计算和桩号标定的工程师。

## 功能

- 计算第一、第二缓和曲线、圆曲线和总曲线的几何要素。
- 生成中桩和边桩的坐标，并以桩号标记。
- 导出包含曲线要素和桩号坐标的 Excel 文件。

## 依赖项

此项目需要以下 Python 库：

- `pandas`：用于数据处理和表格生成。
- `openpyxl`：用于将数据导出为 Excel 文件。

### 安装依赖

在项目目录中，运行以下命令安装所需的依赖：

```bash
pip install pandas openpyxl