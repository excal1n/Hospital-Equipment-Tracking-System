#include <sstream>
#include <string.h>
#include <stdio.h>

#include <WiFi.h>
#define MQTT_MAX_PACKET_SIZE 1844
#include <PubSubClient.h>
// Bluetooth LE
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

/* Add WiFi and MQTT credentials to credentials.h file */
#include "credentials.h"

//Scan time must be longer than beacon interval
int beaconScanTime = 4;
WiFiClient espClient;
PubSubClient client(espClient);

char Relogio_Adress[20] = "78:02:b7:45:dd:13";
char BLE_Address[20] = "f3:71:c2:3f:27:94";

// We collect each device MAC and RSSI
typedef struct {
  char address[17];   // 67:f1:d2:04:cd:5d
  int rssi;
} BeaconData;

uint8_t bufferIndex = 0;  // Found devices counter
BeaconData buffer[50];    // Buffer to store found device data
uint8_t message_char_buffer[MQTT_MAX_PACKET_SIZE];

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
public:

  void onResult(BLEAdvertisedDevice advertisedDevice) {
    extern uint8_t bufferIndex;
    extern BeaconData buffer[];
    if(bufferIndex >= 50) {
      return;
    }
    // RSSI
    if(advertisedDevice.haveRSSI()) {
      buffer[bufferIndex].rssi = advertisedDevice.getRSSI();
    } else { buffer[bufferIndex].rssi =  0; }
    
    // MAC is mandatory for BT to work
    strcpy (buffer[bufferIndex].address, advertisedDevice.getAddress().toString().c_str());
    
    bufferIndex++;
    // Print everything via serial port for debugging
    Serial.printf("MAC: %s \n", advertisedDevice.getAddress().toString().c_str());
    Serial.printf("name: %s \n", advertisedDevice.getName().c_str());
    Serial.printf("RSSI: %d \n", advertisedDevice.getRSSI());
  }
};

void setup() {
  Serial.begin(115200);
  BLEDevice::init(""); // Can only be called once
}

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
}

void connectMQTT() {
  client.setServer(mqttServer, mqttPort);
  Serial.println("Connecting to MQTT...");
  if (client.connect("ESP32Client", mqttUser, mqttPassword)) {
    Serial.println("connected");
  } else {
    Serial.print("failed with state ");
    Serial.println(client.state());
    delay(500);
  }
}

void ScanBeacons() {
  BLEScan* pBLEScan = BLEDevice::getScan(); //create new scan
  MyAdvertisedDeviceCallbacks cb;
  pBLEScan->setAdvertisedDeviceCallbacks(&cb);
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  BLEScanResults foundDevices = pBLEScan->start(beaconScanTime);
  
  // Stop BLE
  pBLEScan->stop();
  delay(100);
  Serial.println("Scan done!");
}

void loop() {
  boolean result;
  // Scan Beacons
  ScanBeacons();
  // Reconnect WiFi if not connected
  while (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }
  
  // Reconnect to MQTT if not connected
  while (!client.connected()) {
    connectMQTT();
  }
  client.loop();
  
  // SenML begins
  String payloadString = "";
  for(uint8_t i = 0; i < bufferIndex; i++) {
    if(strncmp(buffer[i].address, BLE_Address, 18) == 0)
    {
      payloadString += String(buffer[i].rssi);
      break;
    }
  }
  
  // Print and publish payload
  Serial.println(payloadString);

  payloadString.getBytes(message_char_buffer, payloadString.length()+1);
  
  Serial.print("PUB Result: ");
  Serial.println(client.publish("esp1", message_char_buffer, payloadString.length(), false));
    
  //Start over the scan loop
  bufferIndex = 0;
  // Add delay to slow down publishing frequency if needed.
  //delay(5000);
}
