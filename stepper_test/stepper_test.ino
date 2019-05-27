#define dirPin 2
#define stpPin 3
#define minDelay 20
void setup() {
  // put your setup code here, to run once:
  pinMode(dirPin, OUTPUT);
  pinMode(stpPin, OUTPUT);
  pinMode(13, OUTPUT);

}

void loop() {
  digitalWrite(dirPin, HIGH);
  // put your main code here, to run repeatedly:
  for (int i = 200; i > minDelay; i--) {
    for (int j = 0; j < 1; j++) {
      digitalWrite(stpPin, HIGH);
      digitalWrite(13, HIGH);
      delayMicroseconds(i);
      digitalWrite(stpPin, LOW);
      digitalWrite(13, LOW);
      delayMicroseconds(i);
    }
  }
  for (int j = 0; j < 10000; j++) {
    digitalWrite(stpPin, HIGH);
    digitalWrite(13, HIGH);
    delayMicroseconds(20);
    digitalWrite(stpPin, LOW);
    digitalWrite(13, LOW);
    delayMicroseconds(20);
  }
  for (int i = minDelay; i < 200; i++) {
    for (int j = 0; j < 1; j++) {
      digitalWrite(stpPin, HIGH);
      digitalWrite(13, HIGH);
      delayMicroseconds(i);
      digitalWrite(stpPin, LOW);
      digitalWrite(13, LOW);
      delayMicroseconds(i);
    }
  }
  digitalWrite(dirPin, LOW);
  delay(2000);
}
