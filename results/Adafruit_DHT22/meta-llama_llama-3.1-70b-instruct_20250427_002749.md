# Adafruit DHT22 Datasheet
================================-

**Disclaimer:**
---------------

This datasheet is generated based on general knowledge up to my last training data cut-off and is not an official manufacturer document. While I strive to provide accurate information, accuracy cannot be guaranteed. For critical applications and final design decisions, please consult the official manufacturer datasheet.

**General Description:**
------------------------

The Adafruit DHT22 is a popular, low-cost, single-board digital temperature and humidity sensor. It utilizes a capacitive humidity sensor and a thermistor to measure the surrounding air, and can output calibrated digital signals for processing by a microcontroller or other external circuitry.

**Theory of Operation / Sensing Principle:**
-----------------------------------------

The DHT22 sensor works by measuring the changes in capacitance caused by variations in humidity, and changes in resistance due to temperature variations using a thermistor. These changes are then converted into digital signals, which are sent to the external circuitry.

**Features:**
-------------

*   Measures temperature and humidity
*   Low power consumption
*   Simple single-wire interface
*   Calibrated digital signal output
*   Small size and low cost

**Potential Applications:**
-------------------------

*   Weather stations
*   Home automation systems
*   Climate control systems
*   Industrial automation
*   IoT projects

**Pin Configuration and Description:**
--------------------------------------

| Pin # | Name | Function |
| --- | --- | --- |
| 1 | VCC | Power supply |
| 2 | DATA | Single-wire interface for data communication |
| 3 | NC | No connection |
| 4 | GND | Ground |

**Absolute Maximum Ratings:**
---------------------------

| Parameter | Value |
| --- | --- |
| Supply Voltage | 5.5V |
| Operating Temperature | -20°C to 80°C |
| Storage Temperature | -40°C to 125°C |
| Relative Humidity | 0% to 100% RH |

**Electrical Characteristics:**
-----------------------------

*   Supply Voltage: 3.3V to 5.5V
*   Supply Current: 2mA (max)
*   Data Pin Drive Capability: 20mA (max)

#### Power Consumption Breakdown:

| Mode | Current Draw |
| --- | --- |
| Active/M measurement | 2mA (max) |
| Idle/Sleep | 0.1mA (typ) |
| Communication Active | 1mA (typ) |

**Operating Conditions:**
-----------------------

*   Recommended Supply Voltage: 5V
*   Operating Temperature Range: -20°C to 50°C
*   Operating Humidity Range: 20% to 80% RH

**Sensor Performance / Specifications:**
--------------------------------------

*   Temperature Range: -40°C to 80°C
*   Temperature Accuracy: ±0.5°C (typ), ±2°C (max)
*   Humidity Range: 0% to 100% RH
*   Humidity Accuracy: ±2% RH (typ), ±5% RH (max)
*   Resolution: 16-bit
*   Response Time: 2 seconds (typ)

**Communication Protocol / Interface:**
--------------------------------------

*   Single-wire interface (similar to 1-wire interface)
*   Data transfer speed: 20 Kbps (max)

**Register Map:**
-----------------

| Register Address | Register Name | Description |
| --- | --- | --- |
| 0x00 | CONTROL | Control register |
| 0x01 | DATA\_H | Temperature data (MSB) |
| 0x02 | DATA\_L | Temperature data (LSB) |
| 0x03 | DATA\_H | Humidity data (MSB) |
| 0x04 | DATA\_L | Humidity data (LSB) |

**Package Information / Mechanical Dimensions:**
------------------------------------------

*   Package Type: Three-pin single-row header
*   Dimensions:
    *   Length: 27.9 mm
    *   Width: 13.8 mm
    *   Height: 4.4 mm

**Basic Usage / Application Information:**
-----------------------------------------

### Connection Diagram:

*   Connect the VCC pin to the power supply (3.3V to 5.5V).
*   Connect the GND pin to the ground.
*   Connect the DATA pin to a microcontroller or other external circuitry.

### Initialization and Data Reading:

1.  Initialize the sensor by sending a start signal (18-bit long).
2.  Wait for the response signal (40-bit long).
3.  Read the temperature and humidity data from the sensor.
4.  Convert the data to the desired format.

Pseudo-code example (in C):
```c
#include <Adafruit_DHT.h>

// Initialize the sensor
Adafruit_DHT dht(2); // Assuming the DATA pin is connected to pin 2

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);
}

void loop() {
  // Read the temperature and humidity data
  int temp = dht.getTemperature();
  int humidity = dht.getHumidity();

  // Print the data to the serial monitor
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println("°C");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println("%");

  delay(2000);
}
```

**Compliance and Certifications:**
---------------------------------

*   RoHS compliant
*   CE marked
*   FCC certified (Part 15 compliant)

Please note that the compliance and certifications may vary depending on the specific module or product.