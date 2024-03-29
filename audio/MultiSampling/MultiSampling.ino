#include "esp_system.h"
#include "esp_adc_cal.h"
#include "driver/adc.h"

#define ADC_BAT_PIN 34

#define NO_OF_SAMPLES   64          //Multisampling
#define REF_VOLTAGE 1100

#define LIN_COEFF_A_SCALE               65536
#define LIN_COEFF_A_ROUND               (LIN_COEFF_A_SCALE/2)
#define ADC_12_BIT_RES                  4096

esp_adc_cal_characteristics_t *adc_chars = new esp_adc_cal_characteristics_t;//adc_chars = calloc(1, sizeof(esp_adc_cal_characteristics_t));

adc1_channel_t get_adc1_chanel(uint8_t pin) {
  adc1_channel_t chan;
  switch (pin) {
    case 32:
      chan = ADC1_CHANNEL_4;
      break;
    case 33:
      chan = ADC1_CHANNEL_5;
      break;
    case 34:
      chan = ADC1_CHANNEL_6;
      break;
    case 35:
      chan = ADC1_CHANNEL_7;
      break;
    case 36:
      chan = ADC1_CHANNEL_0;
      break;
    case 37:
      chan = ADC1_CHANNEL_1;
      break;
    case 38:
      chan = ADC1_CHANNEL_2;
      break;
    case 39:
      chan = ADC1_CHANNEL_3;
      break;
  }
  return chan;
}

double read_bat_adc_idf() {
  uint32_t adc_reading = 0;

  //Multisampling
  for (int i = 0; i < NO_OF_SAMPLES; i++) {
    adc_reading += adc1_get_raw((adc1_channel_t)get_adc1_chanel(ADC_BAT_PIN));
  }
  adc_reading /= NO_OF_SAMPLES;
  //Convert adc_reading to voltage in mV
  double voltage = esp_adc_cal_raw_to_voltage(adc_reading, adc_chars);

  return voltage;
}

void check_efuse(void)
{
  //Check TP is burned into eFuse
  if (esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_TP) == ESP_OK) {
    Serial.print("eFuse Two Point: Supported\n");
  } else {
    Serial.print("eFuse Two Point: NOT supported\n");
  }

  //Check Vref is burned into eFuse
  if (esp_adc_cal_check_efuse(ESP_ADC_CAL_VAL_EFUSE_VREF) == ESP_OK) {
    Serial.print("eFuse Vref: Supported\n");
  } else {
    Serial.print("eFuse Vref: NOT supported\n");
  }
}
void print_char_val_type(esp_adc_cal_value_t val_type)
{
  if (val_type == ESP_ADC_CAL_VAL_EFUSE_TP) {
    Serial.print("Characterized using Two Point Value\n");
  } else if (val_type == ESP_ADC_CAL_VAL_EFUSE_VREF) {
    Serial.print("Characterized using eFuse Vref\n");
  } else {
    Serial.print("Characterized using Default Vref\n");
  }
}
void adc_setup() {
  adc1_config_width(ADC_WIDTH_12Bit);
  adc1_config_channel_atten(get_adc1_chanel(ADC_BAT_PIN), ADC_ATTEN_2_5db );
  esp_adc_cal_value_t val_type = esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_2_5db, ADC_WIDTH_12Bit, REF_VOLTAGE, adc_chars);
  print_char_val_type(val_type);
}
//

void setup() {
  Serial.begin(115200);
  adc_setup();
  double bat_test = read_bat_adc_idf();
  Serial.print(bat_test);
  Serial.println ("mV");
}

void loop() {
  // put your main code here, to run repeatedly:
double bat_test = read_bat_adc_idf();
Serial.print(bat_test);
Serial.println ();
}
