\# Data Description｜数据说明



This folder stores the dataset used in the Beijing PM2.5 forecasting project.



本文件夹用于存放北京 PM2.5 浓度预测项目所使用的数据。



\---



\## Raw Data｜原始数据



Raw dataset path:



```text

data/raw/beijing\_pm25.csv



The dataset contains hourly Beijing PM2.5 and meteorological records from 2010 to 2014.



该数据集包含 2010 年至 2014 年北京逐小时 PM2.5 浓度和气象变量记录。



Main Fields｜主要字段

Column	Description	中文说明

No	Record index	序号

year	Year	年

month	Month	月

day	Day	日

hour	Hour	小时

pm2.5	PM2.5 concentration	PM2.5 浓度

DEWP	Dew point	露点

TEMP	Temperature	温度

PRES	Atmospheric pressure	气压

cbwd	Wind direction	风向

Iws	Wind speed-related variable	风速相关变量

Is	Snow	降雪

Ir	Rain	降雨

Preprocessing Note｜预处理说明



In the baseline version, missing PM2.5 values are filled with 0 before constructing lagged features.



在当前基础版本中，缺失 PM2.5 值会在构造滞后变量前填充为 0。



This is a simple baseline preprocessing strategy and may be improved in later versions.



这是一种基础版预处理策略，后续版本可以进一步比较更合理的缺失值处理方法。



Processed Data｜处理后数据



The processed/ folder is reserved for future cleaned or feature-engineered datasets.



processed/ 文件夹用于后续存放清洗后数据或特征工程后的数据文件。

