# src/model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from preprocess import preprocess_data

def train_predictive_models():
    """
    Entrena modelos de predicción para temperatura, humedad y energía.
    Usa un RandomForestRegressor para cada variable.
    """

    # Cargar y preprocesar los datos
    df = preprocess_data()

    # Variables de entrada (features)
    features = [
        col for col in df.columns
        if any(v in col for v in ['temp_C', 'humedad_pct', 'energia_kW'])
        and 'rolling' in col or 'lag' in col
    ]

    # Variables objetivo (targets)
    targets = ['temp_C', 'humedad_pct', 'energia_kW']

    models = {}
    results = {}

    for target in targets:
        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        models[target] = model
        results[target] = mae

        print(f"✅ Modelo entrenado para {target}: MAE = {mae:.3f}")

    return models, results


if __name__ == "__main__":
    models, results = train_predictive_models()
    print("\n🎯 Errores medios absolutos (MAE):")
    for target, mae in results.items():
        print(f"{target}: {mae:.3f}")
