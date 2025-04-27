# Adafruit DHT22 Datasheet

## Disclaimer
This datasheet is generated based on general knowledge up to the last training data cut-off of the AI assistant (2023) and is not an official manufacturer document. Accuracy cannot be guaranteed. Users are advised to consult the official manufacturer datasheet for critical applications and final design decisions.

## General Description

The Adafruit DHT22 is a high-quality digital temperature and humidity sensor. It integrates a capacitive humidity sensor and a thermistor into a single module and provides a calibrated digital signal on the data pin. This sensor is designed to be highly reliable and accurate for a wide range of applications, including HVAC systems, data centers, and weather stations.

## Theory of Operation / Sensing Principle

The DHT22 uses a thermistor and a capacitive sensor to measure temperature and humidity, respectively. The thermistor changes its resistance based on the surrounding temperature, while the capacitive sensor attracts water molecules from the air, changing its capacitance in proportion to the relative humidity.

These two sensors work in tandem with an integrated microcontroller, which processes the raw signals and provides a calibrated digital signal through the data pin. The microcontroller also controls the timing of the measurements, ensuring accurate and stable readouts.

## Features

* High-precision temperature and humidity measurement
* Digital output signal with calibration
* Wide operating range: -40°C to 80°C temperature and 0-100% RH humidity
*General DescriptionBrief overview of the sensor's function and technology.;
* Low power consumption
* Small form factor with integrated sensors
* Easy to use with a single data pin interface

## Potential Applications

* HVAC systems for controlling temperature and humidity
* Weather stations for monitoring environmental conditions
* Data centers for maintaining optimal server operating conditions
* Home automation systems for controlling smart thermostats and humidifiers

## Pin Configuration and Description

| Pin Number | Pin Name | Function |
|------------|-----------------|-------------------|
| 1 | VCC/3.3-5V | Power supply input |
| 2 | Data | Digital signal output |
| 3 | NC | Not Connected |
| 4 | GND | Ground connection |

## Absolute Maximum Ratings

| Parameter | Symbol | Absolute Maximum |
|--------|------|----------|
| Power Supply Voltage | VCC | 6V |
| Operating Temperature | Temp | -40°C to 80°C |

Stress ratings beyond these values may cause permanent damage to the sensor. These limits are stress ratings only and functional operation of the sensor is not guaranteed beyond its operating range.

## Electrical Characteristics

| Parameter | Symbol | Typical | Min | Max | Units |
|--------------------|--------------------------------------|-----------|---|-----|-----|
| Supply Voltage | VCC | 3.3V | 3.3V | 5V | V |
| Output Voltage (High) | | 5V | -   | 5V | V |
| Output Voltage (Low)  | | 0V | -   | 0V | V |
  
### Power Consumption Breakdown

| Mode            | Current Draw |
|-----------------|--------------|
| Active/Measurement | 2.5mA        |
| Idle/Sleep       | 0.5mA        |
| Communication Active | 1mA         |

## Operating Conditions

| Parameter | Min | Typical | Max | Units |
|----------|---|-------|---|----------|
| Supply Voltage | 3.3V | 3.5V | 5V | V |
| Operating Temperature | -40 | - | 80 | °C |
| Operating Humidity | | 0 | 100 | % RH |

## Sensor Performance / Specifications

| Parameter | Symbol | Range | Accuracy | Resolution |
|--------------------------------|---|------|-----|-----------|
| Temperature | Temp | -40°C to 80°C | ±0.5°C | 0.1°C |
| Humidity    | RH   | 0% to 100% RH | ±2% RH | 0.1% RH |

| Response Time | National Standard | Recovery Time |
|--------------|-------------|------------|
|Humidity | 6-7s  (90% Rh) | 1-2s |
|Temperature | | - |

## Communication Protocol / Interface

The DHT22 uses a single-wire interface for communication. The sensor communicates with the microcontroller through the data pin using a timing-based protocol. The microcontroller must pull the data pin low for at least 18ms to initiate a measurement cycle, after which the sensor will respond with the temperature and humidity data.

## Register Map

The DHT22 does not use a register-based configuration/data access method. All data is transmitted directly through the data pin using the single-wire protocol.

## Package Information / Mechanical Dimensions

The DHT22 is typically housed in a small plastic package with four pins (VCC, Data, NC, GND). Its typical dimensions are around 15.2 x 10.2 x 6.2 mm.

## Basic Usage / Application Information

A typical connection diagram would involve connecting the VCC pin to a 3.3V to 5V power supply, the Data pin to a microcontroller's digital input pin, the GND pin to the power supply ground, and the NC pin can be left disconnected.

Pseudo-code for initialization, configuration, and data reading:

```
// Initialize sensor
void initializeSensor() {
  pinMode(dataPin, INPUT_PULLUP); // Set data pin as input
  digitalWrite(dataPin, LOW); // Pull data pin low for at least 18ms
  delay(18);
  digitalWrite(dataPin, HIGH); // Release data pin and wait for sensor response
}

// Read temperature and humidity data
void readSensorData() {
  // Wait for sensor response
  while(digitalRead(dataPin) == HIGH);
  
  // Read 40-bit data from the sensor
  int data[5];
  for(int i = 0; i < 5; i++) {
    data[i] = 0;
    for(int j = 0; j < 8; j++) {
      while(digitalRead(dataPin) == LOW); // Wait for start bit
      delayMicroseconds(30); // Wait for data bit
      if(digitalRead(dataPin) == HIGH) { // Check data bit
        data[i] |= (1 << (7 - j)); // Set corresponding bit in data array
      }
      while(digitalRead(dataPin) == HIGH); // Wait for stop bit
    }
  }
  
  // Calculate temperature and humidity
  int humidity = data[0];
  int temperature = data[2];
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("% RH, Temperature: ");
  Serial.print(temperature);
  Serial.println("°C");
}
```

## Compliance and Certifications

The DHT22 complies with the following standards:

* RoHS: The sensor is manufactured without the use of hazardous materials.
* CE: Compliance with European safety, health, and environmental protection standards.
* FCC: Compliance with US electromagnetic interference regulations.

Please note that specific compliance should be verified with the manufacturer for the most up-to-date information.