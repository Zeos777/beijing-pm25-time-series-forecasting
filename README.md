# Beijing PM2.5 Forecasting Using Python
# 基于 Python 的北京 PM2.5 浓度预测分析项目

## Project Overview / 项目概述

This project is a Beijing PM2.5 concentration data analysis project built around a baseline ordinary least squares regression model.
It uses lagged PM2.5 variables and meteorological features to study short-term PM2.5 behavior and generate a simple prediction baseline.
The current Python version has been organized into a notebook, reusable `src/` modules, and a root-level runner script, `run_baseline_analysis.py`.

本项目是一个北京 PM2.5 浓度预测的数据分析项目，核心方法是使用 OLS multiple linear regression 构建 baseline。
项目主要依赖 PM2.5 滞后变量和气象变量来分析短期污染变化，并已经整理成 notebook、`src/` 模块和根目录运行入口 `run_baseline_analysis.py` 的 Python analysis workflow。
它的目标是把原始分析过程整理得更清晰、可检查、可说明，而不是包装成更复杂的预测系统。

---

## Dataset / 数据集说明

The raw data is stored at `data/raw/beijing_pm25.csv`.
It contains 43,824 hourly records from 2010 to 2014.
The main fields are:

- `year`
- `month`
- `day`
- `hour`
- `pm2.5`
- `DEWP`
- `TEMP`
- `PRES`
- `cbwd`
- `Iws`
- `Is`
- `Ir`

原始数据文件位于 `data/raw/beijing_pm25.csv`，共有 43,824 条逐小时记录，时间范围覆盖 2010 到 2014 年。
其中 `pm2.5` 存在缺失值。当前 baseline 为了保持原始分析口径，先将 missing PM2.5 filled with 0，再继续后续建模。
这不是最理想的统计处理方式，但它保留了当前分析链路的可追踪性，也为后续改进留出了空间。

---

## Methodology / 方法流程

The current Python analysis workflow follows these steps:

1. data loading
2. datetime construction
3. column renaming
4. missing value handling
5. lag feature construction
6. chronological train/test split
7. OLS modeling
8. metric calculation
9. residual diagnostics
10. visualization and output saving

本项目的 Python 分析流程按时间顺序组织，先完成数据读取和时间字段构造，再做变量重命名、缺失值处理、滞后特征构造和训练集 / 测试集划分，随后使用 OLS 回归建模，并输出训练与测试指标、残差诊断图和结果文件。
这个流程的重点是清楚地说明每一步是怎么来的，而不是把所有逻辑堆在 notebook 里。

---

## Python Analysis Workflow / Python 分析流程

The project is now split into a thin runner script, reusable modules, and a notebook version for step-by-step review.

- `run_baseline_analysis.py` is the main entry point.
- `src/data_preprocessing.py` handles data loading, datetime construction, sorting, column renaming, and PM2.5 missing-value handling.
- `src/feature_engineering.py` handles lag features and time-based train/test splitting.
- `src/modeling.py` handles OLS fitting and prediction.
- `src/evaluation.py` handles training and test metrics, plus saving the summary and metric files.
- `src/visualization.py` handles figure generation.
- `notebooks/01_pm25_baseline_analysis.ipynb` is kept as the notebook version of the analysis for step-by-step review.

项目现在已经从单一 notebook 的写法整理成 notebook + `src` modules + `run_baseline_analysis.py` 的结构。
这样做的好处是：主流程可以直接运行，分析步骤也可以逐段检查，结果文件和图表的来源更明确。

---

## Results / 结果

### Training metrics / 训练集指标

| Metric | Value |
|---|---:|
| R-squared | 0.913620 |
| Adjusted R-squared | 0.913602 |
| S | 27.084649 |
| Durbin-Watson | 1.995136 |

### Test metrics / 测试集指标

| Metric | Value |
|---|---:|
| MAD | 18.813214 |
| MSE | 870.109807 |
| RMSE | 29.497624 |
| MAPE | 26.637482 |
| MPE | -10.525987 |

The lagged PM2.5 features capture strong short-term persistence.
The linear baseline performs reasonably on common pollution levels.
Prediction errors can still increase when pollution changes quickly or reaches extreme values.

PM2.5 的滞后特征确实能捕捉到短时间内的持续性，所以模型在常见污染水平附近表现还可以。
但当污染值快速变化，或者遇到极端污染峰值时，误差会更明显，这也是线性 baseline 的典型局限。

---

## Output Files / 输出文件

### `outputs/`

- `regression_summary.txt`
- `baseline_metrics.csv`

### `figures/`

- `training_pollution_timeseries.png`
- `actual_vs_predicted.png`
- `prediction_errors.png`
- `residuals_vs_fitted.png`
- `residual_distribution.png`

这些文件由 `run_baseline_analysis.py` 统一写出，也可以通过 notebook 逐步查看每个中间步骤。

---

## How to Run / 如何运行

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the baseline workflow:

```bash
python run_baseline_analysis.py
```

If you want to review the process step by step, you can open:

```text
notebooks/01_pm25_baseline_analysis.ipynb
```

如果希望逐步查看每一步的数据处理和建模过程，也可以打开 notebook 版本进行检查。

---

## Project Structure / 项目结构

```text
beijing-pm25-time-series-forecasting/
├── README.md
├── requirements.txt
├── run_baseline_analysis.py
├── data/
│   └── raw/
│       └── beijing_pm25.csv
├── notebooks/
│   └── 01_pm25_baseline_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── modeling.py
│   ├── evaluation.py
│   └── visualization.py
├── outputs/
├── figures/
└── report/
```

---

## Limitations / 局限性

- Missing PM2.5 values are filled with 0 mainly to keep the baseline workflow traceable.
- Linear regression may lag when pollution changes suddenly.
- Extreme pollution peaks are harder to capture with this baseline.
- Lag features are correlated, so individual lag coefficients should not be over-interpreted.
- This is a baseline statistical modeling workflow, not a real-time forecasting system.

- 当前对 missing PM2.5 的处理主要是为了保持 baseline 分析流程清晰可追踪，后续还可以继续比较更合理的处理方式。
- 线性回归在污染水平突然变化时容易跟慢半拍。
- 对极端污染峰值的捕捉能力有限。
- 滞后特征之间本身相关性较强，所以单个滞后项系数不宜过度解读。
- 这个项目是一个 baseline statistical modeling workflow，不是实时预测系统。

---

## Skills Demonstrated / 项目体现能力

- Python data analysis workflow organization
- pandas-based preprocessing
- time-based feature construction
- OLS regression with statsmodels
- model evaluation with MAE/RMSE/MAPE-style metrics
- residual diagnostics and visualization
- GitHub project organization

项目的重点是把一个基础统计建模流程整理成结构清楚、可运行、可检查的 Python implementation。
它展示的是数据分析和项目组织能力，而不是更复杂的建模堆叠。

---

## Future Improvements / 后续改进

Possible future work:

- better missing-value handling
- wind direction encoding
- time features such as hour, month, and day of week
- baseline model comparison

后续可以继续在不改变项目定位的前提下，比较不同缺失值处理方式、加入时间特征、编码风向变量，并做更完整的 baseline model comparison。
