unsigned int udppacketcount=0;
int loopcount=0;
unsigned int adcvalue;

char ADCBuffer[20001] = "";

void setup() {
  Serial.begin(115200);
}

void loop() {
    adcvalue=analogRead(34);

    ADCBuffer[udppacketcount] = adcvalue;
    udppacketcount++;
    loopcount++;
    if(udppacketcount == 20000)
      {Serial.print(int(loopcount));
      Serial.println();
      udppacketcount=0;}
   
    yield();
}
