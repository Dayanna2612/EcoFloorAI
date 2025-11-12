import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(start_time, minutes=360):
    rows = []
    floors = [1,2,3]
    for m in range(minutes):
        ts = start_time + timedelta(minutes=m)
        minute_of_day = ts.hour*60 + ts.minute
        base_temp = {1:24, 2:25.5, 3:26.5}
        for f in floors:
            diurnal = 2 * np.sin((minute_of_day/1440)*2*np.pi)
            noise = np.random.normal(0, 0.3)
            temp = base_temp[f] + diurnal + noise + (0.05*(f-1))
            humidity = max(30, 60 - (temp-22)*2 + np.random.normal(0,1))
            base_energy = {1:3.5, 2:5.5, 3:7.0}
            spike = np.random.choice([0,0,0,1], p=[0.85,0.1,0.03,0.02]) * np.random.uniform(1,3)
            energy = base_energy[f] + 0.5*np.sin(minute_of_day/30) + spike + np.random.normal(0,0.2)
            rows.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "edificio": "A",
                "piso": f,
                "temp_C": round(temp,2),
                "humedad_pct": round(humidity,2),
                "energia_kW": round(max(0.1, energy),2)
            })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    start = datetime.now().replace(second=0,microsecond=0) - timedelta(minutes=300)
    df = generate_data(start_time=start, minutes=600)
    df.to_csv("data/data_simulada.csv", index=False)
    print("✅ Datos guardados en data/data_simulada.csv")
