# 科研示意图资产说明

首页主视觉、八个策展项目封面和待策展兜底图均使用 Codex `imagegen` 生成，并以 PNG 原图保存在 `assets/images/`。Hugo 构建时自动生成 WebP 展示版本；网页只引用这些仓库内的静态资产，不在访问时请求外部图床或生成服务。

## 统一风格约束

- 画幅：3:2 横图，网页使用 `object-fit: contain` 完整展示，不裁切科研构图。
- 视觉：高水平学术期刊图版与工业工程可视化的结合。
- 色彩：纸白、冷灰、墨蓝、工程蓝、场分布青和克制铜橙。
- 内容：科学对象居中并保留安全边距；不生成可读文字、Logo、水印、界面面板或通用科幻背景。

## 资产主题

| 文件 | 科研对象 |
| --- | --- |
| `assets/images/lab-hero.png` | 磷酸铁锂方形电芯剖面、颗粒电极、隔膜、离子通量、温度场与浓度场 |
| `assets/images/projects/batteryoptimization-nsga-ii.png` | 多目标电池设计、Pareto 前沿、代理响应面与约束平面 |
| `assets/images/projects/electrodereconstruction-matlab.png` | 多相多孔电极的体素重构与微结构体积 |
| `assets/images/projects/pore-network-model-application.png` | 孔体、孔喉、扩散和反应路径 |
| `assets/images/projects/cnn-for-battery-soh.png` | 早期循环信号、三通道张量、卷积特征图与健康轨迹 |
| `assets/images/projects/batteryaging-matlab.png` | SEI、生物质颗粒裂纹、锂库存损失与容量衰减 |
| `assets/images/projects/nature-energy2019.png` | 早期循环曲线、方差特征与寿命分布复现 |
| `assets/images/projects/paper-reproduce.png` | 论文、数据、计算网格和结果对齐验证流程 |
| `assets/images/projects/ml-dev.png` | 科研数据、特征处理、训练、验证与实验部署链路 |
| `assets/images/projects/project-fallback.png` | 未策展科研仓库的通用工程对象与测量场 |

更新图片时，保持相同构图、色彩和禁止项；生成后复制到上述稳定路径，不直接引用生成目录。
