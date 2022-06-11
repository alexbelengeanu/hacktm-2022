#include <Servo.h> 

const int pinEcho = 2;
const int pinTrigger = 3;
const int pinServo1 = 5;
const int pinServo2 = 6;

long durata;
int distanta;

int pos1, pos2;
String serial_message;

Servo servomotor1;
Servo servomotor2; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pinTrigger, OUTPUT);
  pinMode(pinEcho, INPUT);
  servomotor1.attach(pinServo1); 
  servomotor1.write(98);
  servomotor1.attach(pinServo2); 
  servomotor2.write(98);
  delay(2000);
}

int check_ultrasonic(){
  char message[40];

  digitalWrite(pinTrigger, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrigger, LOW);

  durata = pulseIn(pinEcho, HIGH);
  
  distanta = durata*0.0346/2;

  sprintf(message, "[ultrasonic] %d ", distanta);
  if(distanta < 20)
    return 1;
  else
    Serial.println(message);
  return 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    serial_message = String(Serial.readString());
    pos1=98;
    pos2=98;
    if(serial_message.substring(0) == "organic"){
      do{
        servomotor1.write(pos1);
        servomotor2.write(pos2);
        pos1 = pos1 + 2;
        pos2 = pos2 - 2;
        delay(50);
      }while(pos1<=138);
      delay(3000);
      do{
        servomotor1.write(pos1);
        servomotor2.write(pos2);
        pos1 = pos1 - 2;
        pos2 = pos2 + 2;
        delay(50);
      }while(pos1!=pos2);
      delay(3000);
    }
    else if(serial_message.substring(0) == "recyclable"){
      do{
        servomotor1.write(pos1);
        servomotor2.write(pos2);
        pos1 = pos1 - 2;
        pos2 = pos2 + 2;
        delay(50);
      }while(pos1>=58);
      delay(3000);
      do{
        servomotor1.write(pos1);
        servomotor2.write(pos2);
        pos1 = pos1 + 2;
        pos2 = pos2 - 2;
        delay(50);
      }while(pos1!=pos2);
      delay(3000);
    }
  }
  if(check_ultrasonic())
    Serial.println("[detection] Obiect detectat");
  delay(1000);
}
