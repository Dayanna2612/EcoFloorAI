# ======================================================
# Proyecto: EcoFloorAI
# Descripción: Panel de monitoreo y predicción ambiental
# ======================================================

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from src.preprocess import preprocess_data
import time

# -----------------------------------
# Configuración general del panel
# -----------------------------------
st.set_page_config(page_title="EcoFloorAI Dashboard", layout="wide")
st.title("🌱 EcoFloorAI - Monitoreo y Predicción Ambiental en Edificios")

st.sidebar.markdown("⏱️ Actualización automática cada 60 segundos")
if st.sidebar.button("🔄 Actualizar ahora"):
    st.rerun()

# -----------------------------------
# Carga y preparación de los datos
# -----------------------------------
df = preprocess_data()

pisos_disponibles = sorted(df["piso"].unique())
piso_seleccionado = st.selectbox("🏢 Selecciona un piso para visualizar:", pisos_disponibles)
df_piso = df[df["piso"] == piso_seleccionado]

st.subheader("📊 Datos recientes del piso seleccionado")
st.dataframe(df_piso.tail(10))

# -----------------------------------
# Entrenamiento de modelos y predicciones
# -----------------------------------
features = [c for c in df.columns if ("lag" in c or "rolling" in c)]
targets = ["temp_C", "humedad_pct", "energia_kW"]

models = {}
for target in targets:
    X = df[features]
    y = df[target]
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    models[target] = model

last_row = df_piso.iloc[[-1]][features]
predictions = {t: models[t].predict(last_row)[0] for t in targets}

temp = predictions["temp_C"]
hum = predictions["humedad_pct"]
ener = predictions["energia_kW"]

# -----------------------------------
# Estado general por variable 
# -----------------------------------
st.subheader("⚠️ Estado actual y predicciones a +60 minutos")

col1, col2, col3 = st.columns(3)

# Temperatura (°C)
if temp >= 29.5:
    temp_status = "🔴 Crítica"
elif 28 <= temp < 29.5:
    temp_status = "🟠 Media"
elif 26 <= temp < 28:
    temp_status = "🟡 Informativa"
else:
    temp_status = "🟢 Normal"
col1.metric("Temperatura (°C)", f"{temp:.2f}", temp_status)

# Humedad relativa (%)
if hum > 80 or hum < 20:
    hum_status = "🔴 Crítica"
elif hum > 75 or hum < 22:
    hum_status = "🟠 Media"
elif hum > 70 or hum < 25:
    hum_status = "🟡 Informativa"
else:
    hum_status = "🟢 Normal"
col2.metric("Humedad (%)", f"{hum:.2f}", hum_status)

# Energía (kW) 
if ener > 1.4:
    ener_status = "🔴 Crítica"
elif ener > 1.2:
    ener_status = "🟠 Media"
elif ener > 1.0:
    ener_status = "🟡 Informativa"
else:
    ener_status = "🟢 Normal"
col3.metric("Energía (kW)", f"{ener:.2f}", ener_status)


# -----------------------------------
# Recomendaciones automáticas
# -----------------------------------
st.subheader("💡 Recomendaciones automáticas")

recomendaciones = []

# Temperatura
if temp >= 29.5:
    recomendaciones.append(f"🔴 Temperatura crítica detectada en el Piso {piso_seleccionado}. Ajustar el setpoint a 24 °C y aumentar el flujo de aire acondicionado.")
elif 28 <= temp < 29.5:
    recomendaciones.append(f"🟠 Temperatura media en el Piso {piso_seleccionado}. Se sugiere reducir carga térmica o revisar los equipos de climatización.")
elif 26 <= temp < 28:
    recomendaciones.append(f"🟡 Temperatura informativa en el Piso {piso_seleccionado}. Supervisar la tendencia durante los próximos 30 min.")

# Humedad
if hum > 80 or hum < 20:
    recomendaciones.append(f"🔴 Humedad crítica en el Piso {piso_seleccionado}. Ajustar humidificadores/deshumidificadores y verificar ventilación.")
elif hum > 75 or hum < 22:
    recomendaciones.append(f"🟠 Humedad media en el Piso {piso_seleccionado}. Revisar filtros y calibración del sistema de ventilación.")
elif hum > 70 or hum < 25:
    recomendaciones.append(f"🟡 Humedad fuera del rango óptimo en el Piso {piso_seleccionado}. Observar si se mantiene la tendencia.")

# Energía
if ener > 1.4:
    recomendaciones.append(f"🔴 Consumo energético crítico en el Piso {piso_seleccionado}. Redistribuir carga hacia pisos con menor demanda y revisar equipos.")
elif ener > 1.2:
    recomendaciones.append(f"🟠 Consumo energético medio. Evaluar horarios de funcionamiento y reducir picos de carga.")
elif ener > 1.0:
    recomendaciones.append(f"🟡 Consumo energético informativo. Monitorear durante la próxima hora para evitar sobrecarga.")

# Condición general
if not recomendaciones:
    recomendaciones.append(f"🟢 Piso {piso_seleccionado} en condiciones estables. Mantener parámetros actuales y continuar monitoreo.")

for rec in recomendaciones:
    st.write(rec)

# -----------------------------------
# Registro de alertas recientes (con columnas y filtros oficiales)
# -----------------------------------
st.subheader("📋 Alertas recientes")

alertas = []

# Temperatura
if temp >= 29.5:
    alertas.append(["Temperatura crítica", f"Piso {piso_seleccionado}", "Ajustar setpoint a 24 °C y aumentar ventilación"])
elif 28 <= temp < 29.5:
    alertas.append(["Temperatura media", f"Piso {piso_seleccionado}", "Reducir carga térmica o revisar sistema de climatización"])
elif 26 <= temp < 28:
    alertas.append(["Temperatura informativa", f"Piso {piso_seleccionado}", "Monitorear evolución de la temperatura"])

# Humedad
if hum > 80 or hum < 20:
    alertas.append(["Humedad crítica", f"Piso {piso_seleccionado}", "Ajustar sistema de humidificación/deshumidificación"])
elif hum > 75 or hum < 22:
    alertas.append(["Humedad media", f"Piso {piso_seleccionado}", "Revisar calibración del sistema de ventilación"])
elif hum > 70 or hum < 25:
    alertas.append(["Humedad informativa", f"Piso {piso_seleccionado}", "Observar la tendencia en las próximas horas"])

# Energía
if ener > 1.4:
    alertas.append(["Energía crítica", f"Piso {piso_seleccionado}", "Redistribuir carga eléctrica y revisar equipos"])
elif ener > 1.2:
    alertas.append(["Energía media", f"Piso {piso_seleccionado}", "Evaluar horarios y picos de uso energético"])
elif ener > 1.0:
    alertas.append(["Energía informativa", f"Piso {piso_seleccionado}", "Monitorear demanda eléctrica en la próxima hora"])

# -----------------------------------
# Explicabilidad: por qué ocurrió la alerta
# -----------------------------------
explicaciones = []

for alerta in alertas:
    tipo, ubicacion, recomendacion = alerta
    motivo = ""

    if "Temperatura" in tipo:
        if temp >= 29.5 and ener > 1.2:
            motivo = "Alta carga térmica combinada con alto consumo energético."
        elif temp >= 28:
            motivo = "Incremento sostenido de temperatura en el último periodo."
        else:
            motivo = "Variación leve de temperatura detectada."

    elif "Humedad" in tipo:
        if hum > 80:
            motivo = "Exceso de humedad posiblemente por baja ventilación."
        elif hum < 20:
            motivo = "Ambiente demasiado seco, revisar sellado y flujo de aire."
        else:
            motivo = "Pequeña desviación respecto al rango óptimo."

    elif "Energía" in tipo:
        if ener > 1.4:
            motivo = "Demanda energética crítica posiblemente por sobreuso de equipos."
        elif ener > 1.2:
            motivo = "Consumo elevado fuera del promedio reciente."
        else:
            motivo = "Aumento leve en el consumo energético."

    else:
        motivo = "Comportamiento anómalo detectado por el sistema."

    explicaciones.append(motivo)

# Crear DataFrame de alertas con formato oficial
if alertas:
    timestamp_actual = df_piso.iloc[-1]["timestamp"] if not df_piso.empty else "N/A"
    data_alertas = []
    for alerta in alertas:
        tipo, ubicacion, recomendacion = alerta
        nivel = tipo.split()[-1].capitalize()
        variable = tipo.split()[0].capitalize()
        piso_num = piso_seleccionado
        data_alertas.append([timestamp_actual, piso_num, variable, nivel, recomendacion, explicaciones[len(data_alertas)]])

    df_alertas = pd.DataFrame(data_alertas, columns=["timestamp", "piso", "variable", "nivel", "recomendación", "explicación"])

    # Filtro por nivel de alerta
    nivel_filtro = st.selectbox("🔍 Filtrar alertas por nivel:", ["Todas"] + df_alertas["nivel"].unique().tolist())
    if nivel_filtro != "Todas":
        df_alertas = df_alertas[df_alertas["nivel"] == nivel_filtro]

    st.dataframe(df_alertas)

    
else:
    st.success("✅ No se detectan alertas en este momento.")

    # Notificación visual automática (bonus alternativo)
if not df_alertas.empty:
    alertas_criticas = df_alertas[df_alertas["nivel"].isin(["Media", "Crítica"])]
    if not alertas_criticas.empty:
        st.toast(f"🚨 {len(alertas_criticas)} alerta(s) media(s) o crítica(s) detectadas. Revisa la tabla inferior.", icon="⚠️")

# -----------------------------------
# Gráficos de tendencias
# -----------------------------------
st.subheader(f"📈 Tendencias del Piso {piso_seleccionado}")

# Temperatura
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_piso["timestamp"], df_piso["temp_C"], color="tomato")
ax.set_title(f"Tendencia de Temperatura - Piso {piso_seleccionado}")
ax.set_xlabel("Tiempo")
ax.set_ylabel("Temperatura (°C)")
st.pyplot(fig)

# Humedad
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(df_piso["timestamp"], df_piso["humedad_pct"], color="skyblue")
ax2.set_title(f"Tendencia de Humedad - Piso {piso_seleccionado}")
ax2.set_xlabel("Tiempo")
ax2.set_ylabel("Humedad (%)")
st.pyplot(fig2)

# Energía
fig3, ax3 = plt.subplots(figsize=(10, 5))
ax3.plot(df_piso["timestamp"], df_piso["energia_kW"], color="green")
ax3.set_title(f"Tendencia de Energía - Piso {piso_seleccionado}")
ax3.set_xlabel("Tiempo")
ax3.set_ylabel("Energía (kW)")
st.pyplot(fig3)

# -----------------------------------
# Pie de página
# -----------------------------------
st.caption("👩‍💻 Desarrollado por Dayanna Chávez, Juan José Ayala y Dilan Steven Torres — Hackathon Innovación y Tecnología para el Futuro 🌍")
st.info("♻️ El panel se actualizará automáticamente en 60 segundos...")

time.sleep(60)
st.rerun()
