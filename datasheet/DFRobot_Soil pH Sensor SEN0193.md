# Capacitive Soil Moisture Sensor SEN0193

## Manufacturer Info

* **Manufacturer:** DFRobot
* **Model:** SEN0193
* The document "Characterization of Low-Cost Capacitive Soil Moisture Sensors for IoT Networks" mentions the sensor with the identifier SKU:SEN0193. [pg. 2]
* **Website:** (Inferred: www.dfrobot.com, based on the forum link in "3216156.pdf" [pg. 2] and the product link in "3216156.pdf" [pg. 9])

## General Description

* The document "Characterization of Low-Cost Capacitive Soil Moisture Sensors for IoT Networks" describes the SEN0193 as a low-cost "capacitive" soil moisture sensor designed for use in distributed nodes for IoT applications. It's used for experimental determination of soil moisture. [pg. 1, 2]
* The sensor is a capacitive soil moisture sensor that addresses the corrosion issues of resistive sensors. It can be inserted into the soil for extended periods. [3216156.pdf, pg. 2]

## Theory of Operation / Sensing Principle

* The sensor operates on the principle of capacitive measurement. The output of capacitive moisture sensors depends on the complex relative permittivity of the soil, which is affected by the soil's dielectric properties. [sensors-20-03585.pdf, pg. 4]
* The sensor measures changes in capacitance caused by the moisture content of the soil. [3216156.pdf, pg. 2]

## Features

* Low-cost [sensors-20-03585.pdf, pg. 2]
* Capacitive sensor technology [3216156.pdf, pg. 2]
* Waterproof & anti-corrosion [3216156.pdf, pg. 3]
* Suitable for 3.3V/5V main control board [3216156.pdf, pg. 3]
* Increased waterproof performance [3216156.pdf, pg. 2]
* Optimized corrosion resistance [3216156.pdf, pg. 2]
* Increased plate length and optimized circuit performance [3216156.pdf, pg. 2]
* Wide input voltage range [3216156.pdf, pg. 2]

## Potential Applications

* IoT applications in agriculture [sensors-20-03585.pdf, pg. 1]
* Irrigation management [sensors-20-03585.pdf, pg. 2]
* Soil moisture determination in geotechnical applications [sensors-20-03585.pdf, pg. 2]
* Smart farming [sensors-20-03585.pdf, pg. 1]
* Greenhouse technology [sensors-20-03585.pdf, pg. 1]
* Agriculture in general [sensors-20-03585.pdf, pg. 1]

## Pin Configuration and Description

* The "3216156.pdf" document provides the following pinout information:
    * Red: VCC [3216156.pdf, pg. 4]
    * Black: GND [3216156.pdf, pg. 4]
    * Yellow: Signal [3216156.pdf, pg. 4]
    * Black: GND [3216156.pdf, pg. 4]

## Absolute Maximum Ratings

* The documents provided do not list explicit "Absolute Maximum Ratings" in the traditional format (e.g., maximum voltage, current). However, the operating voltage range provides some indication of acceptable limits.

## Electrical Characteristics

* **Operating Voltage:** 3.3 ~ 5.5 VDC [3216156.pdf, pg. 3]
* **Output Voltage:** 0 ~ 2.9 VDC [3216156.pdf, pg. 3]
* **Power Consumption Breakdown:** The documents do not provide a detailed power consumption breakdown.

## Operating Conditions

* **Operating Voltage:** 3.3 ~ 5.5 VDC [3216156.pdf, pg. 3]

* The "sensors-20-03585.pdf" document mentions that the correct operation of soil moisture sensors may require consideration of factors like soil temperature and salinity, but doesn't specify the operating ranges for the SEN0193. [pg. 2]

## Sensor Performance / Specifications

* The "sensors-20-03585.pdf" document discusses the importance of sensor performance metrics like range, accuracy, resolution, sensitivity, and response time in the context of soil moisture sensors, but it does not provide specific values for the SEN0193. [pg. 2]
* The "3216156.pdf" document mentions that the sensor's increased plate length improves the accuracy of soil moisture information, but it does not provide quantitative accuracy specifications. [pg. 2]

## Communication Protocol / Interface

* Analog output [3216156.pdf, pg. 3]

## Register Map

* The documents provided do not contain a register map for this sensor, which is typical for sensors with digital interfaces like I2C or SPI.  Since this sensor has an analog output, a register map is not applicable.

## Package Information / Mechanical Dimensions

* **Dimensions:** 6.89 x 1.18 inches or 175 x 30 mm (L x W) [3216156.pdf, pg. 3]
* **Weight:** 15g [3216156.pdf, pg. 3]

## Basic Usage / Application Information

* The "3216156.pdf" document provides a connection diagram and example code for using the sensor with an Arduino. [pg. 3, 8]
* The sensor can be connected to a variety of microcontrollers including Arduino, ESP32, micro:bit, and Raspberry Pi. A Raspberry Pi requires an external ADC module. [3216156.pdf, pg. 2-3]

## Compliance and Certifications

* The documents provided do not list specific compliance and certifications for the SEN0193 sensor.
