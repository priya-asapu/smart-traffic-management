import pandas as pd
import random

times = [
    "06:00","07:00","08:00","09:00","10:00","11:00",
    "12:00","13:00","14:00","15:00","16:00","17:00",
    "18:00","19:00","20:00","21:00","22:00"
]

days = [
    "Monday","Tuesday","Wednesday",
    "Thursday","Friday","Saturday","Sunday"
]

weather = ["Sunny","Cloudy","Rainy"]

rows = []

for _ in range(1000):

    time = random.choice(times)
    day = random.choice(days)
    weather_type = random.choice(weather)

    vehicle_count = random.randint(20,300)
    speed = random.randint(10,80)

    # Rule for traffic level
    if vehicle_count > 220 or speed < 20:
        traffic = "High"
    elif vehicle_count > 120 or speed < 40:
        traffic = "Medium"
    else:
        traffic = "Low"

    rows.append([
        time,
        day,
        weather_type,
        vehicle_count,
        speed,
        traffic
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "Time",
        "Day",
        "Weather",
        "Vehicle_Count",
        "Speed",
        "Traffic_Level"
    ]
)

df.to_csv("dataset/traffic_data.csv", index=False)

print("✅ 1000-row dataset created successfully!")