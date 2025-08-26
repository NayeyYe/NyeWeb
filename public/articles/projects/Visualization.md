

# 温度数据可视化系统

本项目提供完整的温度数据可视化解决方案，支持使用Matplotlib和PyEcharts生成24种专业图表，满足从基础趋势分析到复杂三维建模的全方位需求。

## 项目亮点
- **双引擎驱动**：同时支持Matplotlib（静态图）和PyEcharts（交互图）
- **配置中心化**：300+可调参数集中管理
- **智能数据处理**：自动处理时间序列与数据重采样
- **工业级输出**：支持300DPI高清图片与交互式HTML
## 功能全景
### Matplotlib可视化矩阵
| 图表类型   | 功能特性              | 输出示例         |
| ---------- | --------------------- | ---------------- |
| 面积图     | 梯度填充/透明度控制   | `area_plot.png`  |
| 箱线图     | 离群点检测/分组对比   | `box_plot.png`   |
| 日历热力图 | 周-日布局/月份标签    | `calendar.png`   |
| 热力图     | 多时间粒度/自定义色阶 | `heatmap.png`    |
| 折线图     | 数据平滑/标记点控制   | `line_plot.png`  |
| 3D曲面图   | 多维度分析/视角控制   | `3d_surface.png` |
### PyEcharts交互矩阵
| 图表类型 | 交互特性            | 输出文件          |
| -------- | ------------------- | ----------------- |
| 日历图   | 日期悬停/色阶缩放   | `calendar.html`   |
| 热力图   | 矩阵聚焦/数据筛选   | `heatmap.html`    |
| 折线图   | 区域缩放/数据对比   | `line_chart.html` |
| 3D曲面图 | 自由旋转/多维度提示 | `3d_surface.html` |
## 快速启动
### 环境配置
```bash
conda create -n visualization python=3.9
conda activate visualization
pip install -r requirements.txt
```

### 数据生成
```python
# 生成模拟数据（365天*24小时）
python src/data_generator.py
```
### 全量可视化
```python
# 生成所有24种图表（Matplotlib+PyEcharts）
python main.py
```
## 配置中心
所有可视化参数通过`config/visualization_config.py`集中管理：
```python
# 示例：修改Matplotlib折线图样式
MATPLOT_LINE_CONFIG = {
    "line": {
        "color": "#FF5733",       # 主色修改
        "linewidth": 2.5,         # 线宽调整
        "marker": "D"             # 标记形状
    },
    "text": {
        "title_fontsize": 18      # 标题字号
    }
}
# 示例：调整PyEcharts热力图交互
PYE_HEATMAP_CONFIG = {
    "visualmap_colors": ["#2E86C1", "#AED6F1", "#F9E79F", "#EB984E"],  # 渐变色
    "datazoom_range": [20, 80]    # 初始缩放范围
}
```
## 项目架构
```
temperature_visualization/
├── config
│   ├── settings.py            # 路径配置
│   └── visualization_config.py # 300+可视化参数
├── data
│   ├── temperature.py         # 数据生成器
│   └── temperature_data.csv   # 数据集样例
├── outputs
│   ├── matplotlib/            # 静态图输出
│   └── pyecharts/             # 交互图输出
├──src
│    ├── data_generator.py      # 数据管道
│    ├── matplot/               # 12种Matplotlib视图
│    ├── pyeplot/               # 12种PyEcharts视图
└──main.py                      # 执行入口
```
## 定制化示例
### 生成月度对比箱线图
```python
def custom_box_plot():
    create_box_plot(
        df, 
        group_by="month",
        config={
            "box": {
                "widths": 0.8,
                "flier_color": "#C0392B"
            },
            "output": {
                "filename": "monthly_comparison"
            }
        }
    )
```
### 创建交互式温度地图
```python
def interactive_heatmap():
    create_pye_heatmap(
        df,
        time_granularity="hour",
        config={
            "visualmap_colors": ["#1A5276", "#3498DB", "#85C1E9"],
            "tooltip_formatter": "时间: {b}时<br>温度: {c}℃"
        }
    )
```
## 技术支持

- **数据问题**：检查`data/temperature.py`中的模拟算法
- **样式调整**：修改`visualization_config.py`对应配置段
- **输出异常**：确认`settings.py`中的路径权限
---
> 本项目持续更新，欢迎提交Issue或Fork改进。可视化参数配置指南详见[CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)