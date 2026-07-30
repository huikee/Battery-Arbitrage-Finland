import pandas as pd

# explore_data.py: Basic exploratory data-analysis
df = pd.read_csv("data/electricitydata.csv")

# Print the 5 first rows
print("*** First 5 rows ***")
print(df.head())

# Print Dataframe information
print("\n*** Dataframe info ***")
print(df.info())

# Print summary stats
print("\n*** Stats ***")
print(df.describe(include='all'))

# Print missing values
print("\n*** Missing values ***")
print(df.isnull().sum())

# Print the number of rows and columns
print("\n*** Amount of rows and columns ***")
print(df.shape)

# Print column names
print("\n*** Column names ***")
print(df.columns)

# Print duplicate rows
print("\n*** Duplicate Rows***")
print(df.duplicated().sum())

# Print missing Price_cpkWh values
print("\n *** Missing Price_cpkwh ***")
print(df["Price_cpkWh"].isna().sum())

# Print amount and percentage of missing Price_cpkWh data
print(f"Total rows: {len(df)}")
print(f"Missing Price_cpkWH values {df['Price_cpkWh'].isnull().sum()}")
print(f"Percentage: {df['Price_cpkWh'].isnull().mean() * 100:.2f}%")

# Printing Price_cpkWh rows that are missing data and where they are located
missing_prices = df[df["Price_cpkWh"].isnull()]
print(missing_prices.head(20))
print(missing_prices.index)

# Dropping empty Price_cpkWh rows
df = df.dropna(subset=["Price_cpkWh"])

# Print rows after removing missing prices
print("\nRows after removing missing prices:")
print(len(df))