/*
 * This is an example to read analog data at high frequency using the I2S peripheral
 * Run a wire between pins 27 & 32
 * The readings from the device will be 12bit (0-4096) 
 * https://github.com/espressif/arduino-esp32/blob/master/libraries/ESP32/examples/I2S/HiFreq_ADC/HiFreq_ADC.ino
 */

#include <Arduino.h>
#include <driver/i2s.h>


#include <WiFi.h>
#include "secrets.h"

#define I2S_SAMPLE_RATE 16384
#define ADC_INPUT ADC1_CHANNEL_6 //pin 36
#define OUTPUT_PIN 27
//#define OUTPUT_VALUE 3800
//#define READ_DELAY 9000 //microseconds

////////

#define AUDIO_BUFFER_MAX 4096

uint8_t audioBuffer[AUDIO_BUFFER_MAX];
//uint8_t transmitBuffer[AUDIO_BUFFER_MAX];
//uint8_t transmitBuffer[SINGLE_PACKET_MAX];
uint32_t bufferPointer = 0;
uint32_t bufferReading = 0;
uint32_t j = 0;

char ssid[] = SECRET_SSID;   // your network SSID (name) 
char password[] = SECRET_PASS;   // your network password
char host[] = SECRET_HOST;   // your network password

WiFiClient client;

///////

uint16_t adc_reading;

void i2sInit()
{
   i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_ADC_BUILT_IN),
    .sample_rate =  I2S_SAMPLE_RATE,              // The format of the signal using ADC_BUILT_IN
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT, // is fixed at 12bit, stereo, MSB
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    //.channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S_LSB,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 10,
    .dma_buf_len = 1024,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
   };
   i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
   //adc1_config_channel_atten(I2S_ADC_CHANNEL,ADC_ATTEN_DB_11);
   i2s_set_adc_mode(ADC_UNIT_1, ADC_INPUT);
   i2s_adc_enable(I2S_NUM_0);
}

void reader(void *pvParameters) {
  uint32_t read_counter = 0;
  uint64_t read_sum = 0;
// The 4 high bits are the channel, and the data is inverted
  uint16_t offset = (int)ADC_INPUT * 0x1000 + 0xFFF;
  size_t bytes_read;
  size_t output_loop;
  output_loop = 0;
  while(1){
    uint16_t buffer[2] = {0};
    i2s_read(I2S_NUM_0, &buffer, sizeof(buffer), &bytes_read, portMAX_DELAY);
    Serial.print(buffer[1]);
    Serial.println();
    //Serial.println((buffer[0]*256 + buffer[1]));
    //if(output_loop == 1000)
    //{Serial.print(buffer[0],DEC);
    //Serial.println();
    //output_loop = 0;}
    //output_loop++;
    //Serial.print(buffer[0],DEC);
    //Serial.println();
    //Serial.print(":");
    //int Data = 12345;
    byte Hi = offset - buffer[0] >> 8;
    byte Lo = offset - buffer[0] & 0x00FF;
    //Serial.println(Data,HEX);
    //Serial.println(Hi,HEX);
    //Serial.println(Lo,HEX);
    //Serial.println(Data,HEX);
    //Serial.print((buffer[0]));
    //Serial.println();
    //audioBuffer[bufferPointer] = buffer[0]; // stores the value
    //bufferPointer++;
    audioBuffer[bufferPointer] = Hi; // stores the value
    bufferPointer++;
    audioBuffer[bufferPointer] = Lo; // stores the value
    bufferPointer++;
    if (bufferPointer == AUDIO_BUFFER_MAX) { // when the buffer is full
        bufferPointer = 0;
        //for (int i = 0; i <= AUDIO_BUFFER_MAX; i = i + 1) {
        //bufferReading = (audioBuffer[i] * 256 + audioBuffer[i+1]);
        //Serial.print(audioBuffer[i]);
        //Serial.println();}
        client.write((const uint8_t *)audioBuffer, sizeof(audioBuffer)); // sending the buffer to our server
        //for (int i = 0; i <= sizeof(audioBuffer); i += 2) // increment with 2 in the for loop()
        //{
        //Serial.println((audioBuffer[i]*256 + audioBuffer[i+1]));
        //}
        }
    //Serial.printf("%d  %d\n", offset - buffer[0], offset - buffer[1]);
    //if (bytes_read == sizeof(buffer)) {
    //  read_sum += offset - buffer[0];
    //  read_sum += offset - buffer[1];
    //  read_counter++;
    //} else {
    //  Serial.println("buffer empty");
    //}
    //if (read_counter == I2S_SAMPLE_RATE) {      
      //////////////////////
      //adc_reading = read_sum / I2S_SAMPLE_RATE / 2;
      //Serial.printf("avg: %d millis: ", adc_reading);
      //Serial.println(millis());
      //read_counter = 0;
      //read_sum = 0;
      //i2s_adc_disable(I2S_NUM_0);
      //delay(READ_DELAY);
      //i2s_adc_enable(I2S_NUM_0);
    //}
  }
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
  adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
  
  const int port = 5010;
  while (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(1000);
  }

  //Serial.println("connected to server");
  i2sInit();
  // Create a task that will read the data
  xTaskCreatePinnedToCore(reader, "ADC_reader", 2048, NULL, 1, NULL, 1);
}

void loop() {
  //delay(1020);
  //Serial.printf("ADC reading: %d\n", adc_reading);
  // for (int i = 0; i <= sizeof(audioBuffer); i += 2) // increment with 2 in the for loop()
  //{
  //  Serial.println((audioBuffer[i]*256 + audioBuffer[i+1]));
    //delay(1000);
  //}
  //delay(READ_DELAY);
}
