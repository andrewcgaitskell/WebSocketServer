/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/AnalogReadSerial
*/

#define samplesLength 115200

void setup() {
  analogReadResolution(10);
  analogSetAttenuation(ADC_0db);
  Serial.begin(115200);
}

void loop() {
  int measures[samplesLength];
  int i = 0;
  while (i <= samplesLength) {
    measures[i++] = analogRead(34);
  }
  for(int i = 0; i <= samplesLength; i++) {
    Serial.println(measures[i]);
  }
  delay(10000);
}
