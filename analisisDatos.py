import pandas as pd

# Cargar datos
df = pd.read_csv('datos_radar.csv')

# Calcular velocidades aproximadas
df['Tiempo_dif'] = df['Tiempo'].diff()
df['Distancia_dif'] = df['Distancia'].diff()
df['Velocidad'] = df['Distancia_dif'] / df['Tiempo_dif']

# Imprimir resultados
print(df[['Tiempo', 'Ángulo', 'Distancia', 'Velocidad']])
