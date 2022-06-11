#include <Servo.h> 

int pinServo = 5;
Servo servomotor; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servomotor.attach(pinServo); 
  servomotor.write(88);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Incepe rotirea la stanga");
  for (int pos = 88; pos <= 176; pos += 4) {
          servomotor.write(pos);
          delay(50);
  }
  Serial.println("Rotire la stanga terminata");
  delay(2000);
  Serial.println("Revenire la pozitia initiala");
  servomotor.write(88);
  delay(2000);
  Serial.println("Incepe rotirea la dreapta");
  for (int pos = 88; pos >= 0; pos -= 4) {
        servomotor.write(pos);
        delay(50);
  }
  Serial.println("Rotire la dreapta terminata");
  delay(2000);
  Serial.println("Revenire la pozitia initiala");
  servomotor.write(88);
  delay(2000);
}
