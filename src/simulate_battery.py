import pandas as pd
from sqlalchemy import create_engine
import math

# URL of database
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/battery_arbitrage"

# Connecting to database
engine = create_engine(DATABASE_URL)

# Saving electricity_prices_clean to df
df = pd.read_sql("SELECT * FROM electricity_prices_clean", engine)

# Battery capacity (kWh)
battery_capacity = 10.0

# How much electricity is in the battery currently
battery_level = 0.0

# How much battery can be charged in an hour
charge_rate = 5.0

# How much of the battery can be discharged in an hour
discharge_rate = 5.0

# Battery efficiency (expected to lose 1kwh per 10kwh)
efficiency = 0.90

# Total savings
total_savings = 0.0

# Statistics for average charging price
charged_energy = 0.0
total_charge_cost = 0.0

# Empty list for storing simulation results
results = []

# Number of charging and discharging hours required
hours_to_charge = math.ceil(battery_capacity / (charge_rate * efficiency))
hours_to_discharge = math.ceil(battery_capacity/discharge_rate)

# Simulate one day at a time using day-ahead prices
for date, day_data in df.groupby("date"):
    # Select the cheapest charging hours
    cheapest_hours = day_data.nsmallest(hours_to_charge, "spot_price")
    # Select the most expensive discharging hours
    most_expensive_hours = day_data.nlargest(hours_to_discharge, "spot_price")
    
    # Store charging and discharging hours
    charge_hours = set(cheapest_hours["hour"])
    discharge_hours = set(most_expensive_hours["hour"])
    
    # Process each hour of the day
    for index, row in day_data.iterrows():
        # Current spot price and hour
        price = row['spot_price']
        hour = row["hour"]
        # Default action if nothing happens during this hour
        action = 'idle'
        # Charge the battery during selected hours
        if hour in charge_hours and battery_level < battery_capacity:
            # Add energy to the battery without exceeding its capacity
            energy_added = min(charge_rate * efficiency, battery_capacity - battery_level)
            if energy_added > 0:
                action = 'charge'
                # Increase battery level
                battery_level += energy_added
                # Update charging stats
                charged_energy += energy_added
                total_charge_cost += price * energy_added

        # Discharge the battery during selected hours    
        elif hour in discharge_hours and battery_level > 0:
            action = "discharge"

            # Discharge only as much as the inverter allows
            energy_discharged = min(discharge_rate, battery_level)

            if charged_energy > 0:
                # Calculate average charging price
                average_charge_price = total_charge_cost / charged_energy

                # Calculate savings
                saving = (price - average_charge_price) * energy_discharged
                total_savings += saving

                # Update battery state
                battery_level -= energy_discharged

                # Update charging statistics
                charged_energy -= energy_discharged
                total_charge_cost -= average_charge_price * energy_discharged

                # Reset statistics when battery becomes empty
                if battery_level <= 0.001:
                    battery_level = 0.0
                    charged_energy = 0.0
                    total_charge_cost = 0.0

        # Save simulation results
        results.append({
        'timestamp': row['timestamp'],
        'price': price,
        'battery_level': battery_level,
        'total_savings': total_savings,
        'action': action})

# Changing the results into a DataFrame
results_df = pd.DataFrame(results)

# Save results for visualization and further analysis
results_df.to_csv("battery_simulation_results.csv", index=False)

# Print simulation summary
print("\nSimulation summary")
print("------------------")
print(f"Total savings: {total_savings / 100:.2f} €")
print(f"Charge events: {(results_df['action'] == 'charge').sum()}")
print(f"Discharge events: {(results_df['action'] == 'discharge').sum()}")
print(f"Idle hours: {(results_df['action'] == 'idle').sum()}")