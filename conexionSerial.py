import serial
from collections import deque
from flask import Flask, jsonify
import time

# Configuración del puerto serial
arduino = serial.Serial('COM6', baudrate=9600, timeout=1) 

# Crear servidor Flask
app = Flask(__name__)

# Ventana de promedios para tiempo, distancia y velocidad
ventana = deque(maxlen=10)

# Función para recibir un recorrido completo con tiempo
def recibir_recorrido():
    arduino.reset_input_buffer()
    datos_recorrido = []
    tiempo_inicial = time.time()  # Marcar el inicio del recorrido

    while len(datos_recorrido) < 19:  # Lecturas (ejemplo: 180° con pasos de 10°)
        if arduino.in_waiting > 0:
            raw_line = arduino.readline()
            linea = raw_line.decode('utf-8', errors='ignore').strip()
            print(f"Medidas tomadas: {linea}")
            try:
                partes = linea.split(',')
                angulo = float(partes[0].split(':')[1].strip())
                distancia = float(partes[1].split(':')[1].strip())
                tiempo_actual = time.time() - tiempo_inicial
                ventana.append(tiempo_actual)  # Añadir el tiempo relativo
                datos_recorrido.append({"angulo": angulo, "distancia": distancia, "tiempo": tiempo_actual})
            except (ValueError, IndexError) as e:
                print(f"Error al procesar datos ({e}), esperando nueva lectura...")
                continue

    return datos_recorrido


@app.route('/analisis', methods=['GET'])
def enviar_analisis():
    datos_recorrido = recibir_recorrido()

    # Calcular promedios
    promedio_distancia = sum([dato["distancia"] for dato in datos_recorrido]) / len(datos_recorrido)
    promedio_angulo = sum([dato["angulo"] for dato in datos_recorrido]) / len(datos_recorrido)

    # Calcular velocidad promedio: v = d / t
    tiempos = [dato["tiempo"] for dato in datos_recorrido]
    distancia_total = sum([dato["distancia"] for dato in datos_recorrido])
    tiempo_total = tiempos[-1] - tiempos[0] if len(tiempos) > 1 else 0
    promedio_velocidad = distancia_total / tiempo_total if tiempo_total > 0 else 0

    # Crear respuesta
    respuesta = {
        "recorrido": datos_recorrido,
        "promedios": {
            "distancia": promedio_distancia,
            "angulo": promedio_angulo,
            "velocidad": promedio_velocidad
        }
    }
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
