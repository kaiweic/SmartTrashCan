// defines pins numbers
const int trigPin = 11;
const int echoPin = 12;
// defines variables
long duration;
int distance;
int arr[10], i, avg;
void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(9600); // Starts the serial communication
  for (i = 0; i < 10; i++) {
    arr[i] = 0;
  }
}
void loop() {
  delay(500);
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  // Prints the distance on the Serial Monitor
  Serial.print("Distance: ");
  Serial.println(distance);
  avg = 0;
  for (i = 0; i < 9; i++) {
    arr[i] = arr[i + 1];
    avg += arr[i];
  }
  arr[9] = distance;
  avg += arr[9];
  if (avg >= 150) {
    Serial.print(1);
  } else {
    Serial.print(0);
  }
}
