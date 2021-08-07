unsigned int udppacketcount=0;
int loopcount=0;
unsigned int adcvalue=0;


#include <Arduino.h>
#include <WiFi.h>
#include <driver/adc.h>
#include "secrets.h"
//#define AUDIO_BUFFER_MAX 800
#define AUDIO_BUFFER_MAX 2048
//#define SINGLE_PACKET_MAX 1024

uint8_t audioBuffer[AUDIO_BUFFER_MAX];
uint8_t transmitBuffer[AUDIO_BUFFER_MAX];
uint8_t ADCBuffer[AUDIO_BUFFER_MAX];
//uint8_t transmitBuffer[SINGLE_PACKET_MAX];
unsigned int  bufferPointer = 0;
unsigned int  j = 0;

char ssid[] = SECRET_SSID;   // your network SSID (name) 
char password[] = SECRET_PASS;   // your network password
char host[] = SECRET_HOST;   // your network password

bool transmitNow = false;

WiFiClient client;

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("MY IP address: ");
  Serial.println(WiFi.localIP());
  
  const int port = 5010;
  while (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(1000);
  }

  Serial.println("connected to server");
}

void loop() {
    //adcvalue=analogRead(34)/16;
    adcvalue=analogRead(34);
    // get a 10-bit ADC value:
     // divide by 256 to get the first byte:
     // (result is an integer):
     byte firstByte = adcvalue / 256;
     // modulo by 256 to get the second byte:
     byte secondByte = adcvalue % 256;
     // send the first of the two bytes:
     //Serial.print(adcvalue);
     //Serial.print("->");
     //Serial.print(firstByte);
     //Serial.print(':');
     // send the second of the two bytes:
     //Serial.print(secondByte);
     //Serial.println();
     //delay(500);
        //Serial.print(adcvalue);
    //Serial.println();
    
    ADCBuffer[udppacketcount] = firstByte;
    udppacketcount++;
    ADCBuffer[udppacketcount] = secondByte;
    udppacketcount++;
    if(udppacketcount == AUDIO_BUFFER_MAX)
      {
    Serial.print(int(loopcount));
    Serial.println();
    udppacketcount=0;
      transmitNow = true;}

     if (transmitNow) { // checks if the buffer is full
        transmitNow = false;
        //client.write((const uint8_t *) ADCBuffer, sizeof(ADCBuffer)); // sending the buffer to our server
        client.write((const byte *) &ADCBuffer, sizeof(ADCBuffer));
       //for (int i = 0; i < sizeof(ADCBuffer); i++)
        //    { j = int (ADCBuffer[i]);
            //Serial.print(j);
            //Serial.println();}
     }
    //yield();
}
