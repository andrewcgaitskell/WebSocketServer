void setup() {
 Serial.begin(115200);
 uint16_t buffer[2] = {0};
}

void loop() {
  // put your main code here, to run repeatedly:
uint16_t buffer[2] = {0};
buffer[0] = 8888;
Serial.print(buffer[0],DEC);
Serial.println();
byte Hi = buffer[0] >> 8;
byte Lo = buffer[0] & 0x00FF;
Serial.print(Hi,HEX);
Serial.print(":");
Serial.print(Lo,HEX);
Serial.println();
delay(500);
}
