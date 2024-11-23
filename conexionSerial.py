import serial
from collections import deque
from flask import Flask, jsonify

# Configuración del puerto serial
arduino = serial.Serial('COM6', baudrate=9600, timeout=1)  

# Ventana para promedio móvil
ventana = deque(maxlen=10)

# Función para recibir datos del Arduino
def recibir_datos():
    arduino.reset_input_buffer()  # Limpiar el buffer de entrada
    while True:
        if arduino.in_waiting > 0:
            raw_line = arduino.readline()  # Leer la línea en bruto
            linea = raw_line.decode('utf-8', errors='ignore').strip()  # Decodificar ignorando errores

            if linea:  # Verificar que no esté vacía
                try:
                    angulo, distancia = map(float, linea.split(','))
                    print(f"Ángulo: {angulo}, Distancia: {distancia}")  # Mostrar solo ángulo y distancia
                    return angulo, distancia
                except ValueError:
                    continue  # Ignorar líneas mal formateadas


# Función para analizar los datos
def analizar_datos(angulo, distancia):
    ventana.append(distancia)
    promedio = sum(ventana) / len(ventana)
    return {"angulo": angulo, "distancia": distancia, "promedio": promedio}

# Crear servidor Flask
app = Flask(__name__)

@app.route('/datos', methods=['GET'])
def enviar_datos():
    angulo, distancia = recibir_datos()
    resultado = analizar_datos(angulo, distancia)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
