/* Audio streamer with ESP32 and Adafruit elected microphone board. 
 * Created by Julian Schroeter.
*/
#include <Arduino.h>
#include <WiFi.h>
#include <driver/adc.h>
#include "secrets.h"
//#define AUDIO_BUFFER_MAX 800
#define AUDIO_BUFFER_MAX 1024
//#define SINGLE_PACKET_MAX 1024

uint8_t audioBuffer[AUDIO_BUFFER_MAX];
uint8_t transmitBuffer[AUDIO_BUFFER_MAX];
//uint8_t transmitBuffer[SINGLE_PACKET_MAX];
uint32_t bufferPointer = 0;
uint32_t j = 0;

char ssid[] = SECRET_SSID;   // your network SSID (name) 
char password[] = SECRET_PASS;   // your network password
char host[] = SECRET_HOST;   // your network password

bool transmitNow = false;

WiFiClient client;

hw_timer_t * timer = NULL; // our timer
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED; 

void IRAM_ATTR onTimer() {
  portENTER_CRITICAL_ISR(&timerMux); // says that we want to run critical code and don't want to be interrupted
  int adcVal = adc1_get_voltage(ADC1_CHANNEL_6); // reads the ADC
  //uint8_t value = map(adcVal, 0 , 4096, 0, 255);  // converts the value to 0..255 (8bit)
  //uint16_t value = map(adcVal, 0 , 4096, 0, 4096);  // converts the value to 0..255 (8bit)
  byte firstByte = adcVal / 256;
  // modulo by 256 to get the second byte:
  byte secondByte = adcVal % 256;
  
  audioBuffer[bufferPointer] = firstByte; // stores the value
  bufferPointer++;
  audioBuffer[bufferPointer] = secondByte; // stores the value
  bufferPointer++;
  if (bufferPointer == AUDIO_BUFFER_MAX) { // when the buffer is full
    bufferPointer = 0;
    memcpy(transmitBuffer, audioBuffer, AUDIO_BUFFER_MAX); // copy buffer into a second buffer
    transmitNow = true; // sets the value true so we know that we can transmit now
  }
  portEXIT_CRITICAL_ISR(&timerMux); // says that we have run our critical code
}


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
  
  adc1_config_width(ADC_WIDTH_12Bit); // configure the analogue to digital converter
  //adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_0db); // connects the ADC 1 with channel 0 (GPIO 36)
  //ADC_ATTEN_MAX
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_0);
  
  const int port = 5010;
  while (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(1000);
  }

  Serial.println("connected to server");
  int SamplingRate = 20000; 
  //timer = timerBegin(0, 80, true); // 80 Prescaler
  timer = timerBegin(0, 80, true); 
  timerAttachInterrupt(timer, &onTimer, true); // binds the handling function to our timer 
  //timerAlarmWrite(timer, 125, true);
  //timerAlarmWrite(timer, 45, true);
   unsigned int timerFactor = 1000000/SamplingRate; //Calculate the time interval between two readings, or more accurately, the number of cycles between two readings

  timerAlarmWrite(timer,timerFactor, true);
  //timerAlarmWrite(timer, 22, true); //not work
  timerAlarmEnable(timer);

}

void loop() {
  if (transmitNow) { // checks if the buffer is full
    transmitNow = false;
    client.write((const uint8_t *)audioBuffer, sizeof(audioBuffer)); // sending the buffer to our server
    //for (int i = 0; i < sizeof(audioBuffer); i++)
    ///    { j = int (audioBuffer[i]);
    //      Serial.print(j);
     //   Serial.println();}
     client.flush();
  }
}
