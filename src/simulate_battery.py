import pandas as pd
from sqlalchemy import create_engine

# URL of database
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/battery_arbitrage"

# Connecting to database
engine = create_engine(DATABASE_URL)

# Saving electricity_prices_clean to df
df = pd.read_sql("SELECT * FROM electricity_prices_clean", engine)

print(df.head())
print(df.shape)

# How much electricity can fit in a battery
battery_capacity = 10.0

# How much electricity is in the battery currently
battery_level = 0.0

# How much battery can be charged in an hour
charge_rate = 5.0
# How much of the battery can be discharged in an hour
discharge_rate = 5.0

#  
efficiency = 0.90

for index, row in df.iterrows():
    price = row['spot_price']
    print(price)
    # Returns maximum 10kwh (battery capacity)
    if price < 5:
        battery_level = min(battery_level + charge_rate, battery_capacity)
    if price > 15:
        print('discharge')