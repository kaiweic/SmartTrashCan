#include <Servo.h>

#define SERVO_PIN 9

Servo servo;
char cat;

void setup() {
  Serial.begin(115200); // use the same baud-rate as the python side
  servo.attach(SERVO_PIN); // connects the servo
  servo.write(90); // default
}

void loop() {
  if (Serial.available()) { // if there's data to read
    cat = (char) Serial.read();
    servoExe(); // executes the servo
  }
  Serial.println("SERIAL IS AVAILABLE"); // writes a string
  delay(1000);
}

// executes the servo
void servoExe() {
  if (cat == 'R') { // recycle
    servo.write(0); // sets the angle of servo
  } else if (cat == 'L') { // landfill
    servo.write(90); 
  } else if (cat == 'C') { // compost
    servo.write(180); 
  }
  delay(4000);
  servo.write(90);
}

