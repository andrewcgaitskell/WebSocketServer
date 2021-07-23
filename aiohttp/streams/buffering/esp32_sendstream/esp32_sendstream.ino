//esp32_pickle

#include <WiFi.h>

//////////////////////////////////////

#include <driver/i2s.h>
#define ADC_INPUT ADC1_CHANNEL_6 //pin 34
#define ARRAYSIZE(a)    (sizeof(a)/sizeof(a[0]))
const int numBands =8;

const double samplingFrequency = 40000;
const int SAMPLEBLOCK = 8;
const i2s_port_t I2S_PORT = I2S_NUM_0;
uint16_t offset = (int)ADC_INPUT * 0x1000 + 0xFFF;
uint16_t samples[SAMPLEBLOCK];

///////////////////////////////////////
const char* ssid     = "acg34rg_orbi";
const char* password = "Time4Tea";

const char* host  = "acgtest.info";

void setup()
{
    Serial.begin(115200);
    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    Serial.println("Setting up Audio Input I2S");
    setupI2S();
    Serial.println("Audio input setup completed");
    delay(1000);
}

int value = 0;

void loop()
{
    Serial.print("connecting to ");
    Serial.println(host);

    // Use WiFiClient class to create TCP connections
    WiFiClient client;
    const int httpPort = 5010;
    if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
    }

    size_t bytesRead = 0;
    i2s_read(I2S_PORT, 
            (void*)samples, 
            sizeof(samples),
            &bytesRead,
            portMAX_DELAY); // no timeout
    if (bytesRead != sizeof(samples))
          {
              Serial.printf("Could only read %u bytes of %u in FillBufferI2S()\n", bytesRead, sizeof(samples));
             // return;
          }
                                      
    for (uint16_t i = 0; i < ARRAYSIZE(samples); i++) {
         // samples[i] &FFF
          Serial.printf("%7d,",offset-samples[i]); 
        
  }
    }


void setupI2S() {
  Serial.println("Configuring I2S...");
  esp_err_t err;
  // The I2S config as per the example
  const i2s_config_t i2s_config = { 
      .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX | I2S_MODE_ADC_BUILT_IN),
      .sample_rate = samplingFrequency,                        
      .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT, // could only get it to work with 32bits
      .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT, // although the SEL config should be left, it seems to transmit on right
      .communication_format = I2S_COMM_FORMAT_I2S_MSB,
      .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,     // Interrupt level 1
      .dma_buf_count = 4,                           // number of buffers
      .dma_buf_len = SAMPLEBLOCK,                     // samples per buffer
      .use_apll = false//,
     // .tx_desc_auto_clear = false,
     // .fixed_mclk = 1
  };

 err = adc_gpio_init(ADC_UNIT_1, ADC_CHANNEL_0); //step 1
  if (err != ESP_OK) {
    Serial.printf("Failed setting up adc channel: %d\n", err);
    while (true);
  }
 
  err = i2s_driver_install(I2S_NUM_0, &i2s_config,  0, NULL);  //step 2
  if (err != ESP_OK) {
    Serial.printf("Failed installing driver: %d\n", err);
    while (true);
  }

  err = i2s_set_adc_mode(ADC_UNIT_1, ADC_INPUT);
    if (err != ESP_OK) {
    Serial.printf("Failed setting up adc mode: %d\n", err);
    while (true);
  }
  

  
  Serial.println("I2S driver installed.");
}
