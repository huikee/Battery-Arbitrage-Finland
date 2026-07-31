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

# Battery efficiency (expected to lose 1kwh per 10kwh)
efficiency = 0.90

# Price that the battery was charged with
charge_price = None

# Total savings
total_savings = 0.0

# Empty list for stroring results
results = []

# Iterating through spot_price
for index, row in df.iterrows():
    price = row['spot_price']
    action = 'idle'
    if price < 5 and battery_level < battery_capacity:
        action = 'charge'
        battery_level = min(battery_level + charge_rate * efficiency, battery_capacity)
        if charge_price is None:
            charge_price = price
            
    elif price > 15 and battery_level > 0 and charge_price is not None:
        action = 'discharge'
        energy_discharged = battery_level
        saving = (price - charge_price) * energy_discharged
        total_savings += saving

        print(
        f"Charge: {charge_price:.2f} c/kWh | "
        f"Discharge: {price:.2f} c/kWh | "
        f"Energy: {energy_discharged:.1f} kWh | "
        f"Saving: {saving:.2f} cents")
        
        battery_level = 0
        charge_price = None

    # Adding results to  a list
    results.append({
        'timestamp': row['timestamp'],
        'price': price,
        'battery_level': battery_level,
        'total_savings': total_savings,
        'action': action})

# Chnaging list into a DataFrame
results_df = pd.DataFrame(results)
results_df.to_csv("battery_simulation_results.csv", index=False)

print("\nSimulation summary")
print("------------------")
print(f"Total savings: {total_savings / 100:.2f} €")
print(f"Charge events: {(results_df['action'] == 'charge').sum()}")
print(f"Discharge events: {(results_df['action'] == 'discharge').sum()}")
print(f"Idle hours: {(results_df['action'] == 'idle').sum()}")