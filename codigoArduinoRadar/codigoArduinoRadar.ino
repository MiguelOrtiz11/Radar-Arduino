// Librerías
#include <NewPing.h>
#include <Servo.h>
#include <SoftwareSerial.h>

// Configuración de pines
#define TRIG_PIN A3
#define ECHO_PIN A2
#define MAX_DISTANCE 200
#define SERVO_PIN 9
#define BLUETOOTH_RX 3
#define BLUETOOTH_TX 2

// Instancias de componentes
NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo servo;
SoftwareSerial bluetooth(BLUETOOTH_RX, BLUETOOTH_TX);

bool radarActivo = false;

void setup() {
    Serial.begin(9600);
    bluetooth.begin(9600);
    servo.attach(SERVO_PIN);
    servo.write(0); // Posición inicial del servo
}

void loop() {
    if (bluetooth.available()) {
        char comando = bluetooth.read();
        if (comando == 'H') {         // Comando para iniciar radar
            iniciarRadar();
        } else if (comando == 'Q') {  // Comando para detener radar
            detenerRadar();
        }
    }
    if (radarActivo) {
        escanearEntorno();
    }
}

void iniciarRadar() {
    radarActivo = true;
    bluetooth.println("Radar iniciado");
}

void detenerRadar() {
    radarActivo = false;
    bluetooth.println("Radar detenido");
}

void escanearEntorno() {
    for (int angulo = 0; angulo <= 180; angulo += 10) {
        servo.write(angulo);
        delay(500);
        int distancia = sonar.ping_cm();
        // Enviar datos en formato CSV: "ángulo,distancia"
        bluetooth.print(angulo);
        bluetooth.print(",");
        bluetooth.println(distancia);
    }
}
