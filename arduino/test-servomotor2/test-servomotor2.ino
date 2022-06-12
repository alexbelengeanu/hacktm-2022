#include <Servo.h> 

int pinServo1 = 5;
int pinServo2 = 6;
Servo servomotor1;
Servo servomotor2; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servomotor1.attach(pinServo1); 
  servomotor1.write(98);
  servomotor2.attach(pinServo2); 
  servomotor2.write(98);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Incepe rotirea la stanga");
  int pos1, pos2;
  pos1=98;
  pos2=98;
  do{
    servomotor1.write(pos1);
    servomotor2.write(pos2);
    pos1 = pos1 + 2;
    pos2 = pos2 - 2;
    delay(50);
  }while(pos1<=138);
  Serial.println("Rotire la stanga terminata");
  delay(2000);
  Serial.println("Revenire la pozitia initiala");
  do{
    servomotor1.write(pos1);
    servomotor2.write(pos2);
    pos1 = pos1 - 2;
    pos2 = pos2 + 2;
    delay(50);
  }while(pos1!=pos2);
  delay(2000);
  Serial.println("Incepe rotirea la dreapta");
  do{
    servomotor1.write(pos1);
    servomotor2.write(pos2);
    pos1 = pos1 - 2;
    pos2 = pos2 + 2;
    delay(50);
  }while(pos1>=58);
  Serial.println("Rotire la dreapta terminata");
  delay(2000);
  Serial.println("Revenire la pozitia initiala");
  do{
    servomotor1.write(pos1);
    servomotor2.write(pos2);
    pos1 = pos1 + 2;
    pos2 = pos2 - 2;
    delay(50);
  }while(pos1!=pos2);
  delay(2000);
}
