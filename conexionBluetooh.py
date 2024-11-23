import serial
import matplotlib.pyplot as plt
import numpy as np

# Configuración del puerto serial
puerto = 'COM6'  # Cambiar según tu sistema
baudrate = 9600

# Conectar al módulo Bluetooth
arduino = serial.Serial(puerto, baudrate, timeout=1)

# Función para recibir datos del radar
def recibir_datos():
    datos = []
    while len(datos) < 19:  # 180 grados en pasos de 10
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            try:
                angulo, distancia = map(int, linea.split(","))
                datos.append((angulo, distancia))
            except ValueError:
                continue
    return datos

# Procesar datos
def analizar_datos(datos):
    angulos, distancias = zip(*datos)
    min_dist = min(distancias)
    max_dist = max(distancias)
    prom_dist = np.mean(distancias)

    print(f"Distancia mínima: {min_dist} cm")
    print(f"Distancia máxima: {max_dist} cm")
    print(f"Distancia promedio: {prom_dist:.2f} cm")

    # Crear gráfico polar
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    angulos_rad = [np.deg2rad(a) for a in angulos]
    ax.plot(angulos_rad, distancias, marker='o')
    ax.set_title("Radar: Distancia vs Ángulo")
    plt.show()

    return f"Min:{min_dist},Max:{max_dist},Prom:{prom_dist:.2f}"

# Enviar datos analizados al radar
def enviar_analisis(analisis):
    arduino.write(analisis.encode())

# Ejecución del programa
if __name__ == "__main__":
    print("Esperando datos...")
    datos = recibir_datos()
    analisis = analizar_datos(datos)
    enviar_analisis(analisis)
    arduino.close()
