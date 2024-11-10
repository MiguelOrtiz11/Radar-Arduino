//Inclusión de librerias
#include <NewPing.h>
#include <Servo.h>
#include <SoftwareSerial.h> //Definir los pines de los sensores
#define TRIG_PIN A3 //sensor de proximidad
#define ECHO_PIN A2 //sensor de proximidad
#define MAX_DISTANCE 200 //distancia máxima del sensor en cm
#define SERVO_PIN 9 // servomotor
#define BLUETOOTH_RX 3 //bluetooth RX
#define BLUETOOTH_TX 2 //bluetooth TX



NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo servo;
SoftwareSerial bluetooth(BLUETOOTH_RX, BLUETOOTH_TX);
bool radarActivo = false; // Estado del radar

void setup() {
    Serial.begin(9600);
    bluetooth.begin(9600);
    servo.attach(SERVO_PIN); // Conecta el servo al pin correspondiente
}

void loop() {
    if (bluetooth.available()) {
        char comando = bluetooth.read();
        if (comando == 'H') {
            iniciarRadar();
        } else if (comando == 'Q') {
            detenerRadar();
        }
    }
    if (radarActivo) {
        escanearEntorno();
    }
}

void iniciarRadar() {
    radarActivo = true;
    Serial.println("Radar iniciado"); // bluetooth.println("Radar iniciado");
}

void detenerRadar() {  // Corrección de paréntesis
    radarActivo = false;
    Serial.println("Radar detenido"); // bluetooth.println("Radar detenido");
}

void escanearEntorno() {  // Corrección de paréntesis
    for (int angulo = 0; angulo <= 180; angulo += 10) {
        servo.write(angulo); // Mover el servo al ángulo especificado
        delay(500); // Tiempo de espera para el movimiento del servo
        int distancia = sonar.ping_cm(); // Medir distancia actual
        
        // Enviar datos por Bluetooth
        bluetooth.print(angulo);
        bluetooth.print(",");
        bluetooth.println(distancia);
        
        // Mostrar datos en el monitor serial
        Serial.print("Ángulo: ");
        Serial.print(angulo);
        Serial.print(" grados, Distancia: ");
        Serial.print(distancia);
        Serial.println(" cm");
    }
}