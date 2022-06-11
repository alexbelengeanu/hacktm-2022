

const int triggerPin = 3;
const int echoPin = 2;
long durata;
int distanta;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  durata = pulseIn(echoPin, HIGH);
  
  distanta= durata*0.0346/2;
  Serial.println(distanta);
  if (distanta < 20) {
    Serial.println(" | New object detected");
  }
}
