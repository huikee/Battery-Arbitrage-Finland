import pandas as pd
import matplotlib.pyplot as plt

# Load simulation results
df = pd.read_csv("battery_simulation_results.csv")

# Convert timestamps to datetime for plotting
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Create new figure
plt.figure(figsize=(12, 4))
# Plot cumulative savings over time
plt.plot(df["timestamp"], df["total_savings"] / 100)

# Add chart title and axis names
plt.title("Cumulative battery savings")
plt.xlabel("Time")
plt.ylabel("Savings (€)")

# Prevent overlapping labels
plt.tight_layout()
# Display grid lines
plt.grid(True)
# Display chart
plt.show()