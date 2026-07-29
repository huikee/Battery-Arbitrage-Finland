# SQL Analysis Findings

## Dataset overview
Total rows: 31 368

## Price Analysis

### Check for the analysis time period

```sql
SELECT
    MIN(timestamp::timestamp) AS start_date,
    MAX(timestamp::timestamp) AS end_date
FROM electricitydata;
```

Result: 
Start: 2023-01-01 00:00:00.000
End: 2026-07-30 23:00:00.000

31368 hours = 1307 days = 3,6 years

### Check for average, standard deviation, minimum, maximum prices

```sql
SELECT
    AVG("Price_cpkWh") AS average_price,
    STDDEV("Price_cpkWh") AS price_volatility,
    MIN("Price_cpkWh") AS minimum_price,
    MAX("Price_cpkWh") AS maximum_price
FROM electricitydata;
```

Results:
AVG: 6.170, Volatility: 7.82, MIN: -62, MAX: 235,10

### Observation

Electricity prices show significant volatility. The large difference between minimum and maximum prices indicates potential for battery arbitrage.

### Check for count of negative (cheap) hours

```sql
SELECT
    COUNT(*) AS negative_price_hours
FROM electricitydata
WHERE "Price_cpkWh" < 0;
```

Results:
Negative hours: 1704
1704/31368 ≈ 5,4 % of all hours

### Observation

Negative electricity prices occurred frequently enough to be relevant for battery charging analysis. However, negative spot prices do not directly represent the final consumer electricity cost since most of the consumers do not sell their electricity. Consumer price model will be created later.

### Check for expensive hours (>20c/kWh)

```sql
SELECT
    COUNT(*) AS expensive_hours
FROM electricitydata
WHERE "Price_cpkWh" > 20;
```

Results:
Expensive hours: 1244
1244/31368 ≈ 4,0 % of all hours

### Observation

A significant number of high electricity prices. Potential battery discharge opportunities if they occur after low-price charging periods.

### Checking average price in each hour of the day

```sql
SELECT
    EXTRACT(HOUR FROM timestamp::timestamp) AS hour,
    AVG("Price_cpkWh") AS average_price
FROM electricitydata
GROUP BY hour
ORDER BY hour;
```

Results:

Highest average prices:
06:00: 8.84 c/kWh
16:00: 8.78 c/kWh
17:00: 8.78 c/kWh

Lowest average prices:

01:00: 3.41 c/kWh
00:00: 3.49 c/kWh
02:00: 3.52 c/kWh

### Observation

Electricity prices follow a daily pattern
- Prices are lowest during night hours
- Prices are highest during morning and afternoon demand peaks
- This pattern suggests possible battery charging during low-price hours and usage during expensive periods

### Daily spread analysis

``` sql
SELECT
    DATE(timestamp::timestamp) AS day,
    MIN("Price_cpkWh") AS minimum_price,
    MAX("Price_cpkWh") AS maximum_price,
    MAX("Price_cpkWh") - MIN("Price_cpkWh") AS daily_spread
FROM electricitydata
WHERE "Price_cpkWh" IS NOT NULL
GROUP BY day
ORDER BY daily_spread DESC;
```

Results:

The largest daily price spreads were:
2024-01-05: 221.32 c/kWh
2023-11-21: 85.07 c/kWh
2023-11-24: 65.48 c/kWh

### Observations
Electricity prices can vary significantly within a single day. Large differences indicate potential for battery arbitrage.

### Checking days where daily spread is 50c/kWh, >20c/kWh and >10c/kWh

``` sql
SELECT
    COUNT(*) AS days_with_spread_over_50c
FROM (
    SELECT
        DATE(timestamp::timestamp) AS day,
        MAX("Price_cpkWh") - MIN("Price_cpkWh") AS daily_spread
    FROM electricitydata
    WHERE "Price_cpkWh" IS NOT NULL
    GROUP BY day
) AS daily_prices
WHERE daily_spread > 50;
```
Results: 
>50c/kwh: 10/1307 ≈ 0,8% of all days
>20c/kwh: 147/1307 ≈ 11,2% of all days
>10c/kwh: 487/1307 ≈ 37,3% of all days

### Observations

Large spreads about occur frequently enough suggesting that battery arbitrage opportunities exist. However, actual profitability depends on multiple factors such as battery capacity, efficiency losses, degradation, investment cost, taxes and transmission fees.