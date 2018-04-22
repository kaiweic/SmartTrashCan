#include <Servo.h>

#define SERVO_PIN 9
#define SERVO_PIN_2 7

Servo servo;
Servo servo2;
int cat;
int degrees;

void setup() {
  Serial.begin(9600); // use the same baud-rate as the python side
  servo.attach(SERVO_PIN); // connects the servo
  servo2.attach(SERVO_PIN_2);
  servo.write(0); // default
  servo2.write(0);
  degrees = 0;
}

void loop() {
  if (Serial.available() > 0) { // if there's data to read
    cat = (int) Serial.read();
    servoExe(); // executes the servo
  }
//  Serial.println("SERIAL IS AVAILABLE"); // writes a string
  delay(100);
}

// executes the servo
void servoExe() {
  if (cat == 'R') { // recycle
    servo.write(10); // sets the angle of servo
  } else if (cat == 'L') { // landfill
    servo.write(45); 
  } else if (cat == 'C') { // compost
    servo.write(90);
  }
  degrees = (degrees + 90) % 180;
  servo2.write(degrees);
//  servo.write(cat + 10);
//  servo2.write(cat + 20);
}

