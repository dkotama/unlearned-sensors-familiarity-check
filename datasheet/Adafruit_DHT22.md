# DHT22 Sensor Information

This document provides a detailed overview of the DHT22 temperature and humidity sensor, based on information from the provided PDF datasheets.

## Manufacturer Info

* **Manufacturer:** Aosong (Guangzhou) Electronics Co., Ltd.
* **Model Name/Number:** AM2303 (The DHT22 and AM2302 are the same, the AM2302 is the wired version) [page 4]
* **Website:** http://www.aosong.com [page 1, 2]

## General Description

The DHT22 is a basic, low-cost temperature and humidity sensor. It's suitable for hobbyists and basic data logging applications. The sensor integrates a capacitive humidity sensor, a thermistor, and an internal chip to provide a digital signal output. [page 3]

## Theory of Operation / Sensing Principle

* The DHT22 uses a capacitive humidity sensor to measure relative humidity.
* A thermistor is used to measure temperature.
* An internal chip performs analog-to-digital conversion and outputs a digital signal. [page 3]

## Features

* Low cost [page 3, 4]
* Calibrated digital signal output. [page 1]
* Relative humidity and temperature measurement. [page 1]
* No extra components needed. [page 1]
* 4-pin package, fully interchangeable. [page 1]
* Outstanding long-term stability. [page 1]
* Long transmission distance (up to 20m). [page 1]
* Low power consumption. [page 1]
* Full range temperature compensated. [page 1]

## Potential Applications

* Basic data logging [page 3]
* Hobbyist projects [page 3]
* Environmental monitoring
* Home automation
* Weather stations

## Pin Configuration and Description

The DHT22 has four pins: [page 2, 4, 5]

| Pin | Function           | Description                                    |
| --- | ------------------ | ---------------------------------------------- |
| 1   | VDD                | Power supply (3.3-6V DC)                         |
| 2   | DATA               | Digital signal output                          |
| 3   | NULL               | Not connected                                  |
| 4   | GND                | Ground                                         |

## Absolute Maximum Ratings

The provided documents do not specify absolute maximum ratings in a consolidated section. However, exceeding the operating conditions may damage the sensor or reduce its lifespan.

## Electrical Characteristics

* **Power Supply:** 3.3-6V DC [page 1, 2, 3]
* **Current Draw:** 2.5mA max during conversion (while requesting data) [page 3, 4]
* **Output signal:** Digital signal via single-bus [page 1]

### Power Consumption Breakdown

* **Active/Measurement:** 2.5mA max during data request [page 3, 4]
* **Idle/Sleep:** Not specified in the document.

## Operating Conditions

* **Supply Voltage:** 3.3-6V DC [page 1, 2, 3]
* **Temperature Range:** -40 to 80°C [page 3, 4]
* **Humidity Range:** 0-100% RH [page 3, 4]
* **Sensing Period:** 2 seconds (average) [page 2]
* **Additional Considerations:**
    * A 100nF capacitor is recommended between VDD and GND for wave filtering. [page 2]
    * Avoid sending instructions to the sensor within the first second of power-up. [page 2]
    * Shielded wires are recommended for longer connections. [page 7]
    * Welding temperature should be below 260°C. [page 7]
    * Avoid using the sensor in dew conditions. [page 7]
    * Long-term exposure to strong light and UV may degrade performance. [page 7]
    * Mount the sensor away from heat-generating components. [page 7]
    * Chemical vapors may interfere with the sensor's sensitive elements. [page 7]

## Sensor Performance / Specifications

* **Temperature Range:** -40 to 80°C [page 3, 4]
* **Temperature Accuracy:** ±0.5°C [page 3, 4]
* **Temperature Resolution:** 0.1°C [page 2]
* **Humidity Range:** 0-100% RH [page 3, 4]
* **Humidity Accuracy:** ±2% RH (max ±5% RH) [page 2, 4]
* **Humidity Resolution:** 0.1% RH [page 2]
* **Repeatability (Humidity):** +-1%RH [page 2]
* **Repeatability (Temperature):** +- 0.2Celsius [page 2]
* **Humidity Hysteresis:** +-0.3%RH [page 2]
* **Long-term Stability:** ±0.5% RH/year [page 2]
* **Interchangeability:** fully interchangeable [page 2]
* **Sampling Rate:** 0.5 Hz (one reading every 2 seconds) [page 4]

## Communication Protocol / Interface

* **Communication Method:** Single-bus digital signal [page 1, 2]
* **Data Transmission:**
    * Data consists of integral and decimal parts for both humidity and temperature. [page 2]
    * The sensor sends the higher data bits first. [page 2]
    * Data format: 8-bit integral RH data + 8-bit decimal RH data + 8-bit integral T data + 8-bit decimal T data + 8-bit checksum. [page 2]
    * Checksum is the sum of the preceding 8-bit data values. [page 2]
    * Communication takes 5ms. [page 2]

## Register Map

The document does not provide a register map. The DHT22 uses a single-bus protocol, and data is read as a stream of digital values rather than from specific registers.

## Package Information / Mechanical Dimensions

* **Package Type:** Single-row, 4-pin [page 1]
* **Dimensions:** 15.1mm x 25mm x 7.7mm [page 4]
* See page 2 of the "DHT22.pdf" document for a detailed dimensional drawing.

## Basic Usage / Application Information

1.  **Connection Diagram:**
    * Connect VDD (Pin 1) to 3.3-6V power.
    * Connect DATA (Pin 2) to a digital input pin on the microcontroller.
    * Leave Pin 3 unconnected.
    * Connect GND (Pin 4) to ground.
    * A 10kΩ pull-up resistor is recommended between the DATA pin and VDD. [page 4, 5]

2.  **Initialization and Reading Data (Conceptual Steps):**
    * Power up the sensor and wait at least one second before sending any commands. [page 2, 5]
    * The microcontroller sends a start signal to the DHT22. [page 2]
    * The DHT22 responds with a digital signal containing humidity and temperature data. [page 2]
    * The microcontroller reads the digital signal and calculates the humidity and temperature values using the provided formula. [page 2]
    * Verify the data integrity using the checksum. [page 2]

## Compliance and Certifications

The provided documents do not list specific certifications. Contact the manufacturer for detailed compliance and certification information.
