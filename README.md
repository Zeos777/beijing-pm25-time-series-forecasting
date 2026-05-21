# Beijing PM2.5 Forecasting Using Python  
# 基于 Python 的北京 PM2.5 浓度预测分析项目

## Project Overview｜项目概述

This project uses Python to analyze and forecast hourly Beijing PM2.5 concentration based on historical pollution records and meteorological variables.

The project builds a baseline regression model using lagged PM2.5 features, dew point, temperature, atmospheric pressure, wind speed, snow, and rain variables. It covers the full workflow of data preprocessing, feature engineering, chronological train-test splitting, statistical modeling, model evaluation, and result visualization.

本项目基于 Python 对北京逐小时 PM2.5 浓度进行数据分析与短期预测建模。项目使用历史 PM2.5 滞后变量和气象变量作为解释变量，构建基础回归预测模型，并完成数据预处理、特征工程、时间序列式训练集 / 测试集划分、统计建模、误差评估和结果可视化。

This project is positioned as a reproducible Python data analysis and statistical modeling project.

本项目定位为一个可复现的 Python 数据分析与统计建模项目。

---

## Dataset｜数据集说明

The dataset contains hourly Beijing PM2.5 and meteorological records from 2010 to 2014.

原始数据包含 2010 年至 2014 年北京逐小时 PM2.5 浓度与气象变量记录。

### Basic Information｜基本信息

| Item | Value |
|---|---:|
| Time range | 2010-01-01 to 2014-12-31 |
| Frequency | Hourly |
| Rows | 43,824 |
| Original columns | 13 |
| Missing PM2.5 values | 2,067 |

### Main Variables｜主要变量

| Original Column | Renamed Variable | Description | 中文含义 |
|---|---|---|---|
| pm2.5 | pollution | PM2.5 concentration | PM2.5 浓度 |
| DEWP | dew | Dew point | 露点 |
| TEMP | temp | Temperature | 温度 |
| PRES | press | Atmospheric pressure | 气压 |
| Iws | wnd_spd | Wind speed-related variable | 风速相关变量 |
| Is | snow | Snow | 降雪 |
| Ir | rain | Rain | 降雨 |
| cbwd | cbwd | Wind direction | 风向 |

---

## Project Workflow｜项目流程

The project follows the workflow below:

1. Load the raw PM2.5 dataset;
2. Construct a datetime variable from year, month, day, and hour;
3. Rename variables for clearer analysis;
4. Handle missing PM2.5 values;
5. Create lagged PM2.5 features;
6. Split the dataset chronologically into training and test sets;
7. Fit an ordinary least squares regression model;
8. Evaluate model performance using multiple error metrics;
9. Generate diagnostic and prediction visualizations.

本项目主要流程包括：

1. 读取原始 PM2.5 数据；
2. 基于 year、month、day、hour 构造时间变量；
3. 对变量进行重命名，方便后续建模；
4. 处理 PM2.5 缺失值；
5. 构造 PM2.5 滞后特征；
6. 按时间顺序划分训练集和测试集；
7. 使用 OLS 多元线性回归进行建模；
8. 使用多种误差指标评估模型表现；
9. 生成预测结果和模型诊断图表。

---

## Methodology｜方法说明

The model uses ordinary least squares regression implemented with `statsmodels`.

本项目使用 `statsmodels` 构建 OLS 多元线性回归模型。

### Target Variable｜目标变量

```text
pollution

pollution represents the current-hour PM2.5 concentration.

pollution 表示当前小时的 PM2.5 浓度。

Predictor Variables｜解释变量
dew
temp
press
wnd_spd
snow
rain
pollution_Lag1
pollution_Lag2
pollution_Lag3
Lagged PM2.5 Features｜PM2.5 滞后特征
pollution_Lag1 = previous-hour PM2.5
pollution_Lag2 = PM2.5 from two hours before
pollution_Lag3 = PM2.5 from three hours before

中文说明：

pollution_Lag1 = 前 1 小时 PM2.5
pollution_Lag2 = 前 2 小时 PM2.5
pollution_Lag3 = 前 3 小时 PM2.5

The lagged pollution variables are used to capture the short-term persistence of PM2.5 concentration.

滞后 PM2.5 变量用于刻画空气污染浓度在短时间内的持续性。

Train-Test Split｜训练集与测试集划分

The dataset is split chronologically rather than randomly.

本项目按照时间顺序划分训练集和测试集，不使用随机划分。

Dataset	Time Range	Rows
Training set	2010-01-01 00:00 to 2014-12-24 23:00	43,656
Test set	2014-12-25 00:00 to 2014-12-31 23:00	168

Lagged variables are constructed before the chronological split. This allows the first test-set observation to use historical PM2.5 values from the end of the training period.

滞后变量先在全量数据上构造，再按照时间顺序划分训练集和测试集。这样测试集第一小时可以使用训练集末尾的历史 PM2.5 值作为滞后项，因为这些信息在预测时已经发生，不属于未来数据泄漏。

Results｜建模结果
Training Metrics｜训练集指标
Metric	Result
R-squared	0.913620
Adjusted R-squared	0.913602
Residual standard error	27.084649
Durbin-Watson	1.995136

The model shows strong explanatory power on the training set, mainly due to the strong short-term persistence of PM2.5 concentration.

模型在训练集上具有较强解释能力，主要原因是 PM2.5 浓度在短时间内存在明显持续性。

Regression Coefficients｜回归系数
Variable	Coefficient
const	98.365774
dew	0.310956
temp	-0.424900
press	-0.085797
wnd_spd	-0.016379
snow	-0.091234
rain	-0.884674
pollution_Lag1	0.959758
pollution_Lag2	0.003146
pollution_Lag3	-0.025375

The coefficient of pollution_Lag1 is close to 0.96, suggesting that the previous-hour PM2.5 value is highly informative for current-hour PM2.5 prediction.

pollution_Lag1 的系数接近 0.96，说明前一小时 PM2.5 浓度对当前小时 PM2.5 浓度具有较强解释作用。

Test-Set Metrics｜测试集指标
Metric	Result
MAD	18.813214
MSE	870.109807
RMSE	29.497624
MAPE	26.637482%
MPE	-10.525987%

The model achieves reasonable short-term prediction performance on the final-week test set.

模型在最后一周测试集上取得了较稳定的短期预测效果。

Generated Figures｜输出图表

The project generates the following figures:

figures/training_pollution_timeseries.png
figures/actual_vs_predicted.png
figures/prediction_errors.png
figures/residuals_vs_fitted.png
figures/residual_distribution.png
Figure Descriptions｜图表说明
Figure	Description	中文说明
training_pollution_timeseries.png	PM2.5 trend in the training set	训练集 PM2.5 时间序列变化
actual_vs_predicted.png	Actual vs predicted PM2.5 on the test set	测试集真实值与预测值对比
prediction_errors.png	Prediction errors over the test period	测试集预测误差变化
residuals_vs_fitted.png	Residuals against fitted values	残差与拟合值关系
residual_distribution.png	Distribution of training residuals	训练集残差分布
Project Structure｜项目结构
beijing-pm25-time-series-forecasting/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── README.md
│   ├── raw/
│   │   └── beijing_pm25.csv
│   └── processed/
├── notebooks/
│   └── 01_pm25_baseline_regression.ipynb
├── figures/
│   ├── actual_vs_predicted.png
│   ├── prediction_errors.png
│   ├── residual_distribution.png
│   ├── residuals_vs_fitted.png
│   └── training_pollution_timeseries.png
├── outputs/
│   ├── regression_summary.txt
│   └── baseline_metrics.csv
├── report/
└── src/
    ├── data_preprocessing.py
    ├── evaluation.py
    ├── feature_engineering.py
    ├── modeling.py
    └── visualization.py
Requirements｜环境依赖

Main Python packages:

pandas
numpy
matplotlib
scikit-learn
statsmodels
jupyter

Install dependencies:

pip install -r requirements.txt
How to Run｜运行方式

Open and run the notebook:

notebooks/01_pm25_baseline_regression.ipynb

The notebook will:

load the raw dataset;
construct the datetime variable;
rename variables;
handle missing PM2.5 values;
create lagged PM2.5 features;
split the dataset chronologically;
fit the OLS regression model;
calculate training and test-set metrics;
save output files and figures.

中文说明：

运行 notebook 后，会依次完成数据读取、时间变量构造、变量重命名、缺失值处理、滞后变量构造、训练集 / 测试集划分、OLS 回归建模、指标计算、结果保存和图表输出。

Limitations｜局限性
Missing PM2.5 values are filled with 0 in the baseline version, which may introduce statistical bias.
The model uses observed lagged PM2.5 values, so it is closer to one-step-ahead prediction than full recursive multi-step forecasting.
The linear regression model may struggle with extreme pollution peaks and sudden pollution changes.
Wind direction is not included in the current baseline model.
The current model is designed as an interpretable baseline rather than a complex machine learning or deep learning model.

中文说明：

当前基础版本将缺失 PM2.5 填充为 0，该处理方式可能带来统计偏差。
模型使用已观测到的滞后 PM2.5 值，因此更接近一步预测，而不是完整递归式多步预测。
线性回归模型对极端污染峰值和污染水平突变的捕捉能力有限。
当前基础模型暂未加入风向变量。
当前模型定位为可解释的基础预测模型，而不是复杂机器学习或深度学习模型。
Future Improvements｜后续改进

Planned improvements:

compare different missing-value handling strategies;
add time-based features such as hour, month, day of week, and seasonal indicators;
encode wind direction variables;
compare Ridge Regression, Random Forest Regressor, and Gradient Boosting Regressor;
improve model interpretation with feature importance and additional residual diagnostics.

后续可以继续扩展：

比较不同缺失值处理方式；
加入小时、月份、星期、季节等时间特征；
对风向变量进行编码；
比较 Ridge Regression、Random Forest Regressor、Gradient Boosting Regressor 等模型；
通过特征重要性和更多残差诊断增强模型解释。
