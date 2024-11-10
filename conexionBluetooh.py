import serial
import time
import csv

# Configuración del puerto serie Bluetooth
bluetooth_port = 'COM6'  
baud_rate = 9600
arduino = serial.Serial(bluetooth_port, baud_rate)

# Crear un archivo CSV para almacenar los datos
with open('datos_radar.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Tiempo", "Ángulo", "Distancia"])

    # Función para recolectar datos del radar
    while True:
        try:
            # Leer datos de Bluetooth
            data = arduino.readline().decode().strip()
            if data:
                # Dividir ángulo y distancia
                angulo, distancia = data.split(',')
                timestamp = time.time()  # Registrar el tiempo de detección
                writer.writerow([timestamp, angulo, distancia])
                
                print(f"Tiempo: {timestamp}, Ángulo: {angulo}, Distancia: {distancia}")
                
                # Puedes incluir aquí análisis en tiempo real, como calcular velocidades o guardar datos

        except KeyboardInterrupt:
            print("Finalizando la recolección de datos.")
            break
