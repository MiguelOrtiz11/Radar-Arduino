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
  servo.write(0);  // Posición inicial del servo
  pinMode(11, OUTPUT);
}

void loop() {
  if (bluetooth.available()) {
    char comando = bluetooth.read();
    if (comando == 'H') {  // Iniciar radar
      iniciarRadar();
    } else if (comando == 'Q') {  // Detener radar
      detenerRadar();
    }
  }
  if (radarActivo) {
    escanearEntorno();
  }
}

void iniciarRadar() {
  radarActivo = true;
  digitalWrite(11, HIGH);  // Encender el LED al iniciar el radar
  bluetooth.println("Radar iniciado");
}

void detenerRadar() {
  radarActivo = false;
  digitalWrite(11, LOW);  // Apagar el LED al detener el radar

  bluetooth.println("Radar detenido");
}

void escanearEntorno() {

  // Haga recorrido de 180 grados cada 10 grados
  for (int angulo = 0; angulo <= 180; angulo += 10) {

    servo.write(angulo);
    delay(500);
    int distancia = sonar.ping_cm();

    // Depuración para confirmar envío
    Serial.print("Ángulo: ");
    Serial.print(angulo);
    Serial.print(", Distancia: ");
    Serial.println(distancia);

    // Enviar datos por Bluetooth 
    bluetooth.println(String(angulo) + "," + String(distancia));
  }
}
