import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("battery_simulation_results.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])

plt.figure(figsize=(12, 4))
plt.plot(df["timestamp"], df["total_savings"] / 100)

plt.title("Cumulative battery savings")
plt.xlabel("Time")
plt.ylabel("Savings (€)")

plt.tight_layout()
plt.grid(True)
plt.show()