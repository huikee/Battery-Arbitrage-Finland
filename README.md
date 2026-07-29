# Battery-Arbitrage-Finland
Data analysis project investigating whether residential battery storage can reduce electricity costs in Finland using historical Nord Pool spot electricity prices. 

## Technologies 
Python, SQL (PostgreSQL), DBeaver, Pandas, Matplotlib, Power BI and Git.

## Dataset
Nord Pool Finland spot electricity prices:
https://github.com/vividfog/nordpool-predict-fi/blob/main/data/dump.csv

The dataset contained 170 missing values in the Price_cpkWh column (0,54% of all observations). These missing values were located at the end of the dataset indicating future timestamps without available market prices. Since this project analyzes historical electricity prices, these rows were removed before further analysis.

## Workflow
1. Collect data
2. Explotary data analysis using Python & PostgreSQL
3. Analyze behaviors of electricity prices
4. Develop a simple battery usage strategy
5. Simulate strategy using historical data
6. Present findings in Power BI
