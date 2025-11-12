🌱 EcoFloorAI

Monitoreo y Predicción Ambiental por Piso – Hackathon Innovación y Tecnología para el Futuro 2025
EcoFloorAI es un panel web interactivo desarrollado en Streamlit que permite monitorear las condiciones ambientales y energéticas de un edificio de varios niveles. El sistema analiza los datos de temperatura (°C), humedad relativa (%) y consumo energético (kW) por piso, realiza predicciones a +60 minutos, detecta anomalías y genera alertas automáticas con recomendaciones accionables.

🚀 Ejecución rápida

Clona o descarga el proyecto:
git clone https://github.com/usuario/EcoFloorAI.git

cd EcoFloorAI

Instala las dependencias necesarias ejecutando:
pip install -r requirements.txt

Ejecuta la aplicación con:
streamlit run app.py

Abre el enlace local que aparecerá en la consola, por ejemplo:
http://localhost:8501

🧩 Estructura del proyecto

EcoFloorAI/
├── app.py → Panel principal con Streamlit
├── src/
│ └── preprocess.py → Limpieza y generación de datos simulados
├── data/
│ └── datos_simulados.csv → Dataset base del edificio (simulado)
├── requirements.txt → Dependencias del proyecto
└── README.md → Guía de uso y descripción general

🧠 Funcionalidades principales

Monitoreo por piso (1, 2 y 3)
Predicción de temperatura, humedad y energía a +60 minutos
Detección automática de anomalías
Alertas clasificadas (Informativa, Media y Crítica)
Recomendaciones claras y accionables
Exportación de alertas a CSV
Gráficos de tendencias de las últimas horas
Notificaciones visuales en tiempo real

⚙️ Tecnologías utilizadas

Python 3.11
Streamlit
Pandas
Matplotlib
Scikit-learn (RandomForestRegressor)
Numpy

🧮 Ejemplo de uso

Selecciona un piso desde el panel lateral.
Observa las métricas actuales y las predicciones a +60 minutos.
Revisa las recomendaciones automáticas y la tabla de alertas filtrable.
Descarga el reporte de alertas en formato CSV.
Observa las gráficas de tendencia para temperatura, humedad y energía.

👩‍💻 Equipo desarrollador

Dayanna Chávez
Juan José Ayala
Dilan Steven Torres
Hackathon Innovación y Tecnología para el Futuro – XI Semana de la Ingeniería
Zonamerica | Universidad Autónoma de Occidente – 2025

🏁 Objetivo del proyecto

Contribuir a la eficiencia energética y al confort térmico en edificios inteligentes mediante monitoreo en tiempo real, predicciones automáticas y alertas preventivas.

📦 Dependencias (requirements.txt)

streamlit==1.40.0
pandas==2.2.3
matplotlib==3.9.2
scikit-learn==1.5.2
numpy==1.26.4