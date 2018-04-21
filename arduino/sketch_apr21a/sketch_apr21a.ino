void setup() {
  Serial.begin(115200); // use the same baud-rate as the python side
}
void loop() {
  Serial.println("SERIAL IS AVAILABLE"); // write a string
  delay(1000);
}
