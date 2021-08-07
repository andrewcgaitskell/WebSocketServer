#include <WiFi.h>

#include "secrets.h"

char ssid[] = SECRET_SSID;   // your network SSID (name) 
char password[] = SECRET_PASS;   // your network password
String myScript = SECRET_SCRIPT;   // your network password

//const char* test_root_ca = SECRET_ROOT_CA;

WiFiClient  client;

const char* host  = SECRET_HOST;

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
}

int value = 0;

void loop()
{
    delay(5000);
    ++value;

    Serial.print("connecting to ");
    Serial.println(host);

    // Use WiFiClient class to create TCP connections
    WiFiClient client;
    const int httpPort = 5010;
    if (!client.connect(host, httpPort)) {
        Serial.println("connection failed");
        return;
    }
    char message[18] = "Hello from ESP32!";
    //uint8_t myValues[] = {123, 456, 789};
    uint8_t b[]= {0x7E, 0x00, 0x1C, 0x90, 0x00, 0x13, 0XA2, 0x00, 
              0x41, 0x58, 0x1C, 0xCB, 0xFF, 0xFE, 0xC1, 0x7C, 
              0x00, 0x0F, 0x00, 0x01, 0x00, 0x00, 0x37, 0x46, 
              0x46, 0x46, 0x00, 0x00, 0x00, 0xE7};

    //client.print("Hello from ESP32!");
    //client.write(message);
    client.write(b,30);
    
    unsigned long timeout = millis();
    while (client.available() == 0) {
        if (millis() - timeout > 5000) {
            Serial.println(">>> Client Timeout !");
            client.stop();
            return;
        }
    }

    // Read all the lines of the reply from server and print them to Serial
    while(client.available()) {
        String line = client.readStringUntil('\r');
        Serial.print(line);
    }

    Serial.println();
    Serial.println("closing connection");
}
