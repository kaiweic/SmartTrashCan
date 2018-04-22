#include <Servo.h>

#define SERVO_PIN 9
#define SERVO_PIN_2 7
#define trigPin 11
#define echoPin 12
#define SPEED_OF_SOUND 340

Servo servo;
Servo servo2;
char cat;
int distance, i, total;
long duration;

void setup() {
  Serial.begin(9600); // use the same baud-rate as the python side 
  Serial.println("SERIAL IS AVAILABLE");
  servo.attach(SERVO_PIN);
  servo2.attach(SERVO_PIN_2);
  servo.write(90); // default
  servo2.write(0);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  delay(8000);
  cat = (char)Serial.read();
  Serial.print("F"); // dump the trash in the Serial
}

void loop() {
  delay(1000);
  cat = (char) Serial.read();
  while (cat == '\xff') {
      delay(1000);
      cat = (char)Serial.read();
  }
  servoExe(); // executes the servo
  Serial.println("SERIAL IS AVAILABLE");
}

// executes the servo
void servoExe() { 
  if (cat == 'R' || cat == 'L' || cat == 'C') {
    /* detects if the can is full */
    total = 0;
    for (i = 0; i < 10; i++) {
      delay(100);
      digitalWrite(trigPin, LOW);
      delayMicroseconds(2);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      duration = pulseIn(echoPin, HIGH);
      distance= 1.0 * duration * SPEED_OF_SOUND / 10000 / 2;
      total += distance;
    } 
    /* sending signal on whether or not this trash can is full */
    if (total >= 150) {
      Serial.print(1);
    } else {
      Serial.print(0);
    }
    /* sort the waste */
    if (cat == 'R') { // recycle
      servo.write(30);
    } else if (cat == 'L') { // landfill
      servo.write(90);
    } else if (cat == 'C') { // compost
      servo.write(150);
    } 
    delay(1000);
    servo2.write(150);
    delay(2000);
    servo2.write(0);
    delay(500);
    servo.write(90);
  }
}

