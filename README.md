# 瓷音未来 Link-50 频响曲线数据 / Frequency Response Data

从公开频响曲线图数字化的 **瓷音未来 Link-50** 头戴式耳机频率响应数据，可直接导入
REW、AutoEQ、VituixCAD、squig.link 等工具。

Digitized frequency response data for the **Ciyin Link-50** closed-back monitor
headphone, ready to import into REW, AutoEQ, VituixCAD or squig.link.

---

## 数据来源 / Source

| 项目 | 内容 |
|---|---|
| 产品 | 瓷音未来 Link-50（参考售价 269 元） |
| 测试设备 | B&K 5128 人工耳 |
| 补偿曲线 | JM-1 DF Target（即图中的 `JM-1 DF(B_8dB,T_-4dB)`） |
| 原始出处 | 哔哩哔哩 UP主 **A子如是说** |
| 视频 | [【A子】推荐评级：A+，优秀的入门封闭式监听头戴。 —— 瓷音 Link50](https://www.bilibili.com/video/BV1gEZ4BMEEZ) |
| 原始图表 | [`source/chart.png`](source/chart.png) |

**本仓库的数据是本人从上述视频中的频响曲线图逐像素数字化的结果，并非原始测量文件。**
原始测量与图表版权归原 UP主所有；如果你需要权威数据，请以原始视频为准。

This data was digitized by hand (per-pixel) from the chart in the source video.
It is not the original measurement file. The measurement and chart remain the
property of the original creator.

---

## 文件说明 / Files

```
data/
  Link-50_BK5128_1-24oct.csv     1/24 倍频程，240 点（推荐使用）
  Link-50_BK5128_raw.csv         像素级原始分辨率，1338 点（未平滑）
  Link-50_BK5128_normalized.csv  以 1 kHz 归零
  Link-50_BK5128.frd             REW / ARTA / VituixCAD 导入格式
  Link-50_BK5128_REW.txt         REW 文本导入（制表符分隔）
plots/
  Link-50_BK5128_response.png    曲线总览
verification/
  Link-50_BK5128_extraction_check.png   提取轨迹叠加在原图上的验证图
source/
  chart.png                      原始曲线图
digitize.py                      数字化脚本，可复现全部数据
```

### CSV 格式

两列，带表头，逗号分隔：

```csv
frequency,spl
20.00,4.55
20.59,4.55
21.19,4.59
```

请按纯文本导入，不要对首行做数值解析。

---

## 主要数据特征 / Highlights

以 1 kHz 归一后（dB 相对 1 kHz）：

- **低频**：60 Hz 以下有约 +4 dB 的抬高，80 Hz 附近下陷至 +0.2 dB
- **中频**：200 Hz – 1 kHz 平坦，在 0 dB 附近
- **高频**：1.5 kHz 起爬升，3 kHz（+11 dB）、5.5 kHz（+11 dB）、9 kHz（+12 dB）三处高耸
- **深谷**：4.3 kHz 与 6.5 kHz 各有一个 +3～5 dB 的凹陷
- **极高频**：12 kHz 后急剧滚降，20 kHz 处到 −22 dB

三个高频峰的形态是该型号的显著特征，注意这不是平滑的扩散场响应。

---

## 精度说明 / Accuracy

- **坐标标定**：图内 36 条竖网格线与 11 条横网格线逐条核对，残差均在 1 px 以内
  （x 轴 20 Hz–20 kHz 对数，y 轴 +25～−25 dB 线性）
- **提取方式**：按颜色掩膜分离红色实测曲线，再按列连续性追踪，剔除图例色块干扰
- **精度估计**：受曲线线宽与抗锯齿影响，约 **±0.2 dB**
- **Y 轴含义**：图中纵轴是相对显示刻度，**不是校准后的绝对声压级**；引用时请注明归一化基准
- **相位**：原图无相位信息，`.frd` 文件中相位列全部填 0

验证图 [`verification/`](verification/) 中的青色描线叠加在原曲线上，可与原图逐点比对。

---

## 复现 / Reproduce

```bash
pip install pillow numpy
python digitize.py 24oct > data/Link-50_BK5128_1-24oct.csv
python digitize.py raw   > data/Link-50_BK5128_raw.csv
```

脚本从 `source/chart.png` 读取图像，把 CSV 输出到标准输出，由 shell 重定向写入，
自身不打开任何文件用于写入。已确认重跑结果与仓库中的数据逐点一致。

---

## 许可证 / License

- **数字化脚本与仓库整理工作**：[MIT](LICENSE)（代码部分）
- **曲线数据本身**：建议按 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
  使用，转载或二次发布时请注明原始测量来源（UP主 A子如是说）与本仓库

---

## 免责声明 / Disclaimer

本数据仅供个人学习、EQ 调试与技术交流使用。数字化的过程不可避免地引入误差，
不适合作为产品验收、退换货或商业宣传的依据。
