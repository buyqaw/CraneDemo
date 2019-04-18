#include <Arduino.h>            // Standard Arduino library
#include <Wire.h>               // Library to use I2C to display
#include "SSD1306Wire.h"        // Display library
#include <BLEDevice.h>          // Library to create BLE device
#include <BLEServer.h>          // Library to create BLE server
#include <BLEUtils.h>           // Library to communicate in BLE
#include <BLEScan.h>            // Library to scan BLE devices
#include <BLEAdvertisedDevice.h>// Library to advertize BLE
#include <WiFi.h>               // Library to use WiFi
#include <HTTPClient.h>         // Library to GET/POST in HTTP
#include <BLE2902.h>            // Characteristics of standard BLE device


// Display and Scan activities
SSD1306Wire  display(0x3c, 5, 4);
BLEScan* pBLEScan = NULL;
const char* ssid     = "Beeline_EE13";
const char* password = "00002362";

String msg = "0";

String name = "2";

int scanTime = 5;


class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
    }
};


void send_signal(String msg1){
  HTTPClient http;
  Serial.print("Requset is: ");
  Serial.println("http://35.204.205.60:7777/buynode/" + msg1 + name);
  http.begin("http://35.204.205.60:7777/buynode/" + msg1 + name); //Specify destination for HTTP request
  http.addHeader("Content-Type", "text/plain"); //Specify content-type header
  int httpResponseCode = http.GET(); //Send the actual POST request
  Serial.print("Responce is: ");
  Serial.println(httpResponseCode);
  http.end(); //Free resources
}

void scanBLE(){
  BLEScanResults foundDevices = pBLEScan->start(scanTime);
  pBLEScan->setActiveScan(true);
  int count = foundDevices.getCount(); // Define number of found devices
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
  for (int i = 0; i < count; i++)
  {
    BLEAdvertisedDevice d = foundDevices.getDevice(i); // Define found device
      Serial.printf("Address is: %s \n", d.getAddress().toString().c_str());
      char mac2[18] = "24:0a:64:43:77:df";
      for (int b = 0; b < 17; b++){
        mac2[b] = d.getAddress().toString()[b];
      }
      String UUID = String(mac2);
      if(UUID == "12:3b:6a:1b:50:b6" || UUID == "12:3b:6a:1b:4f:74"){
        Serial.println("Found our!");
        msg = String(mac2[16]);
        Serial.print("MAC is: ");
        Serial.println(msg);
        send_signal(msg);
      }
  }
}


void showit(String text){
  display.clear();
  // display.flipScreenVertically();
  display.setFont(ArialMT_Plain_24);
    // clear the display
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(10, 20, text);
  display.display();
}

void setup() {
  Serial.begin(115200);

  display.init();
  showit("KRAN 2");

  BLEDevice::init("Node"); // Initialize BLE device
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
  scanBLE();
  ESP.restart();
}

void loop() {
}
