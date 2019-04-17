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
#include <painlessMesh.h>       // Mesh network based on Wi-Fi
#include "IPAddress.h"
#include <AsyncTCP.h>


// Display and Scan activities
SSD1306Wire  display(0x3c, 5, 4);
BLEScan* pBLEScan = NULL;
const char* ssid     = "BuyQaw.TECH";
const char* password = "YouWillNeverWorkAlone";

String msg = "0";

Scheduler     userScheduler; // to control your personal task
String name = "1";

bool calc_delay = false;

int scanTime = 5;

void send_signal(String msg){
  HTTPClient http;
  http.begin("http://35.204.205.60:7777/buynode/" + msg + name); //Specify destination for HTTP request
  http.addHeader("Content-Type", "text/plain"); //Specify content-type header
  int httpResponseCode = http.GET(); //Send the actual POST request
  http.end(); //Free resources
  ESP.restart();
}

void scanBLE(){
  BLEScanResults foundDevices = pBLEScan->start(scanTime);
  pBLEScan->setActiveScan(true);
  int count = foundDevices.getCount(); // Define number of found devices
  for (int i = 0; i < count; i++)
  {
    BLEAdvertisedDevice d = foundDevices.getDevice(i); // Define found device
      String mac = d.getAddress().toString()[17]
  }
  msg = mac;
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
  showit("BUYQAW");

  BLEDevice::init("Node"); // Initialize BLE device
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setActiveScan(true);

  scanBLE();

  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }

  showit("JYBERU");
  if(msg == "0"){ESP.restart()}
  send_signal(msg);
}

void loop() {
}
