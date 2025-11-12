# src/preprocess.py
import pandas as pd

def preprocess_data(path="../data/data_simulada.csv"):
    """
    Limpia, organiza y enriquece los datos para el modelo predictivo.
    - Crea variables con valores anteriores (lags)
    - Calcula promedios móviles
    - Ordena por piso y tiempo
    """

    # Leer los datos
    import os
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "..", "data", "data_simulada.csv")
    df = pd.read_csv(data_path)


    # Convertir la columna timestamp a formato de fecha y hora
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Ordenar los datos por piso y tiempo
    df = df.sort_values(['piso', 'timestamp']).reset_index(drop=True)

    # Crear variables con rezagos (lags): los valores anteriores
    for var in ['temp_C', 'humedad_pct', 'energia_kW']:
        for lag in [1, 5, 15, 30]:  # minutos anteriores
            df[f'{var}_lag{lag}'] = df.groupby('piso')[var].shift(lag)

    # Crear promedios móviles (para ver tendencias suaves)
    for var in ['temp_C', 'humedad_pct', 'energia_kW']:
        df[f'{var}_rolling15'] = (
            df.groupby('piso')[var]
              .rolling(window=15, min_periods=1)
              .mean()
              .reset_index(level=0, drop=True)
        )

    # Eliminar las primeras filas que no tienen datos suficientes para los lags
    df = df.dropna().reset_index(drop=True)

    return df


if __name__ == "__main__":
    df_prep = preprocess_data()
    print("✅ Datos preprocesados correctamente:")
    print(df_prep.head())
