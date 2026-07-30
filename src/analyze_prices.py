import pandas as pd

# Load dataset
df = pd.read_csv("data/electricitydata.csv")

# Remove rows with missing electricity prices
df = df.dropna(subset=['Price_cpkWh'])

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df['timestamp'])

# Create time-based columns
df["year"] = df["timestamp"].dt.year
df["month"] = df["timestamp"].dt.month
df["day_of_week"] = df["timestamp"].dt.day_name()
df["hour"] = df["timestamp"].dt.hour

print(df.head())
