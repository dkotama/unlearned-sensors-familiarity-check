# Bosch BME280 Sensor Information

This document provides a detailed overview of the Bosch BME280 combined humidity, pressure, and temperature sensor, based on information from the provided PDF datasheet.

## Manufacturer Info

* **Manufacturer:** Bosch Sensortec [Page 2, 3]
* **Model Name/Number:** BME280 [Page 1, 2, 3]
* **Website:** https\://www.bosch-sensortec.com/ \[Inferred]

## General Description

The BME280 is a combined digital humidity, pressure, and temperature sensor. It is housed in a compact metal-lid LGA package. Its small size and low power consumption make it suitable for battery-driven devices such as handsets, GPS modules, and watches. The BME280 is register and performance compatible with the Bosch Sensortec BMP280 digital pressure sensor. [Page 3]

## Theory of Operation / Sensing Principle

The datasheet describes the BME280 as being based on "proven sensing principles." [Page 3] However, the document does not elaborate on the specific physical or chemical principles involved in the sensor's operation. It measures humidity, pressure, and temperature and outputs digital values.

## Features

* Compact package: 2.5 mm x 2.5 mm x 0.93 mm metal lid LGA [Page 2, 3]
* Digital interface: I2C (up to 3.4 MHz) and SPI (3 and 4 wire, up to 10 MHz) [Page 2]
* Wide supply voltage range:
    * VDD (main supply): 1.71 V to 3.6 V
    * VDDIO (interface supply): 1.2 V to 3.6 V [Page 2]
* Low power consumption:
    * 1.8 μA @ 1 Hz humidity and temperature
    * 2.8 μA @ 1 Hz pressure and temperature
    * 3.6 μA @ 1 Hz humidity, pressure, and temperature
    * 0.1 μA in sleep mode [Page 2]
* Operating range: -40°C to +85°C, 0-100% relative humidity, 300-1100 hPa [Page 2]
* Humidity and pressure sensors can be independently enabled/disabled [Page 2]
* RoHS compliant, halogen-free, MSL1 [Page 2]
* High humidity accuracy and fast response time. [Page 3]
* High pressure accuracy and low noise. [Page 3]
* Temperature sensor optimized for lowest noise and highest resolution. [Page 3]

## Potential Applications

* Context awareness (e.g., skin detection, room change detection) [Page 2]
* Fitness monitoring/well-being [Page 2]
* Warning regarding dryness or high temperatures [Page 2]
* Measurement of volume and airflow [Page 2]
* Home automation control (heating, venting, air conditioning (HVAC)) [Page 2]
* Internet of things [Page 2]
* GPS enhancement (e.g., time-to-first-fix improvement, dead reckoning, slope detection) [Page 2]
* Indoor navigation (change of floor detection, elevator detection) [Page 2]
* Outdoor navigation, leisure, and sports applications [Page 2]
* Weather forecast [Page 2]
* Vertical velocity indication (rise/sink speed) [Page 2]
* Target devices:
    * Handsets (mobile phones, tablet PCs, GPS devices)
    * Navigation systems
    * Gaming (flying toys)
    * Cameras (DSC, video)
    * Home weather stations
    * Flying toys
    * Watches [Page 2]

## Pin Configuration and Description

The BME280 is available in an 8-pin LGA package. The pinout is as follows: [Page 38]

| Pin   | Name    | I/O   | Description                                                                                             |
| :---- | :------ | :---- | :------------------------------------------------------------------------------------------------------ |
| 1     | GND     | Supply  | Ground                                                                                                  |
| 2     | CSB     | Input   | Chip select. Connect to VDDIO for I2C mode.                                                              |
| 3     | SDI     | Input/Output  | Serial data input for SPI. SDA for I2C.                                                                |
| 4     | SCK     | Input   | Serial clock input for SPI. SCL for I2C.                                                                |
| 5     | SDO     | Input/Output  | Serial data output for SPI. Leave unconnected for default I2C address. Connect to GND for alternative I2C address.   |
| 6     | VDDIO   | Supply  | Digital interface supply voltage                                                                        |
| 7     | GND     | Supply  | Ground                                                                                                  |
| 8     | VDD     | Supply  | Main analog supply voltage                                                                              |

## Absolute Maximum Ratings

| Parameter                               | Condition                     | Min    | Max     | Unit   |
| :-------------------------------------- | :---------------------------- | :----- | :------ | :----- |
| Voltage at any supply pin (VDD, VDDIO)  |                               | -0.3    | 4.25    | V      |
| Voltage at any interface pin            |                               | -0.3    | VDDIO + 0.3 | V      |
| Storage temperature                     | ≤ 65% RH                      | -45    | +85     | °C     |
| Pressure                                |                               | 0      | 20000   | hPa    |
| ESD HBM (at any pin)                    |                               | ±2     |         | kV     |
| ESD CDM                                 |                               | ±500   |         | V      |
| Machine model                           |                               | ±200   |         | V      |
[Page 13]

## Electrical Characteristics

* **Supply Voltage:**
    * VDD (main supply): 1.71 V to 3.6 V [Page 2]
    * VDDIO (interface supply): 1.2 V to 3.6 V [Page 2]
* **Current Consumption:**
    * 1.8 μA @ 1 Hz humidity and temperature [Page 2]
    * 2.8 μA @ 1 Hz pressure and temperature [Page 2]
    * 3.6 μA @ 1 Hz humidity, pressure, and temperature [Page 2]
    * 0.1 μA in sleep mode [Page 2]
* **Temperature Accuracy:**
    * ±0.5 °C (0…65 °C) [Page 12]
    * ±1.25 °C (-20 …. 0 °C) [Page 12]
    * ±1.5 °C (-40 … -20 °C) [Page 12]
* See the datasheet for detailed electrical characteristics, including input logic levels, output current, and other parameters.

## Operating Conditions

* **Temperature Range:** -40°C to +85°C [Page 2]
* **Humidity Range:** 0 to 100% relative humidity [Page 2]
* **Pressure Range:** 300 to 1100 hPa [Page 2]
* **Supply Voltage:**
    * VDD: 1.71 V to 3.6 V
    * VDDIO: 1.2 V to 3.6 V

## Sensor Performance / Specifications

* **Temperature Range:** -40°C to +85°C [Page 2]
* **Humidity Range:** 0 to 100% relative humidity [Page 2]
* **Pressure Range:** 300 to 1100 hPa [Page 2]
* **Temperature Accuracy:** ±0.5 °C (0…65 °C), ±1.25 °C (-20 …. 0 °C), ±1.5 °C (-40 … -20 °C) [Page 12]
* **Humidity Accuracy:** ±3% relative humidity [Page 2]
* **Humidity Hysteresis:** ±1% relative humidity [Page 2]
* **Pressure RMS Noise:** 0.2 Pa (equivalent to 1.7 cm) [Page 2]
* **Pressure Offset Temperature Coefficient:** ±1.5 Pa/K (equivalent to ±12.6 cm at 1°C temperature change) [Page 2]
* **Humidity Response Time:** 1 s (τ63%) [Page 2]
* **Temperature Resolution:** 0.01 °C [Page 12]

## Communication Protocol / Interface

* **Digital Interface:** I2C (up to 3.4 MHz) and SPI (3 and 4 wire, up to 10 MHz) [Page 2]
* The datasheet provides detailed timing diagrams and specifications for both I2C and SPI communication. [Page 32]

## Register Map

The BME280 has a set of registers for controlling its operation and reading measurement data. Key registers include: [Page 26]

* **0xD0 "id":** Device ID register (value: 0x60). [Page 27]
* **0xE0 "reset":** Reset register. Writing 0xB6 resets the device. [Page 27]
* **0xF2 "ctrl\_hum":** Controls humidity measurement options. [Page 27]
* **0xF3 “status":** Indicates the status of the sensor. [Page 28]
* **0xF4 "ctrl\_meas":** Controls pressure and temperature measurement options and the sensor mode. [Page 28]
* **0xF5 "config":** Configures the data rate, filter, and SPI interface options. [Page 30]
* **0xF7...0xF9 "press":** Contains the raw pressure measurement data (MSB, LSB, XLSB). [Page 30]
* **0xFA...0xFC "temp":** Contains the raw temperature measurement data (MSB, LSB, XLSB). [Page 31]
* **0xFD...0xFE "hum":** Contains the raw humidity measurement data (MSB, LSB). [Page 31]

## Package Information / Mechanical Dimensions

* **Package:** 2.5 mm x 2.5 mm x 0.93 mm metal lid LGA [Page 2, 3]
* Detailed package dimensions and a landing pattern recommendation are provided in the datasheet. [Page 42, 43]

## Basic Usage / Application Information

The datasheet provides connection diagrams for I2C and SPI interfaces. A typical application involves connecting the BME280 to a microcontroller using either I2C or SPI. The microcontroller then configures the sensor, triggers measurements, and reads the digital data. Compensation formulas are provided to convert the raw digital data into accurate temperature, pressure, and humidity values. [Page 23, 25, 39, 40, 41]

## Compliance and Certifications

* **RoHS Compliant:** Yes [Page 2]
* **Halogen-Free:** Yes [Page 2]
* **MSL Level:** 1 [Page 2]
