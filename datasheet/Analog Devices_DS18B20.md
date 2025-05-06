# DS18B20 Sensor Information

This document provides a detailed overview of the DS18B20 programmable resolution 1-Wire digital thermometer, based on information from the provided PDF datasheet.

## Manufacturer Info

* **Manufacturer:** Maxim Integrated [Page 1, 20]
* **Model Name/Number:** DS18B20 [Page 1]
* **Website:** https\://www.maximintegrated.com/en/storefront/storefront.html [Page 20]

## General Description

The DS18B20 is a digital thermometer that provides 9-bit to 12-bit Celsius temperature measurements. It features an alarm function with nonvolatile user-programmable upper and lower trigger points. The DS18B20 communicates over a 1-Wire bus, requiring only one data line (and ground) for communication with a central microprocessor. The sensor can derive power directly from the data line ("parasite power"), eliminating the need for an external power supply. [Page 1]

## Theory of Operation / Sensing Principle

The datasheet describes the DS18B20 as a "direct-to-digital temperature sensor." [Page 5] It measures temperature and converts it into a digital value. The specific physical principles of the temperature sensor are not detailed in this document.

## Features

* Unique 1-Wire interface requires only one port pin for communication. [Page 1]
* Reduces component count with integrated temperature sensor and EEPROM. [Page 1]
* Measures temperatures from -55°C to +125°C (-67°F to +257°F). [Page 1]
* ±0.5°C accuracy from -10°C to +85°C. [Page 1]
* Programmable resolution from 9 bits to 12 bits. [Page 1]
* No external components required. [Page 1]
* Parasite power mode requires only 2 pins for operation (DQ and GND). [Page 1]
* Simplifies distributed temperature-sensing applications with multidrop capability. [Page 1]
* Each device has a unique 64-bit serial code stored in on-board ROM. [Page 1]
* Flexible user-definable nonvolatile (NV) alarm settings. [Page 1]
* Alarm search command identifies devices with temperatures outside programmed limits. [Page 1]
* Available in 8-pin SO (150 mils), 8-pin µSOP, and 3-pin TO-92 packages. [Page 1]

## Potential Applications

* Thermostatic controls [Page 1]
* Industrial systems [Page 1]
* Consumer products [Page 1]
* Thermometers [Page 1]
* Thermally sensitive systems [Page 1]
* HVAC environmental controls [Page 1]
* Temperature monitoring systems inside buildings, equipment, or machinery [Page 1]
* Process monitoring and control systems [Page 1]

## Pin Configuration and Description

The DS18B20 is available in multiple package types, each with a specific pinout.

* **TO-92:**

    * Pin 1: GND [Page 4]
    * Pin 2: DQ (Data Input/Output) [Page 4]
    * Pin 3: VDD (Power supply, optional) [Page 4]

* **SO (150 mils) and µSOP:**

    * Pins 1, 2, 6, 7, 8: N.C. (No Connection) [Page 4]
    * Pin 3: VDD (Power supply, optional) [Page 4]
    * Pin 4: DQ (Data Input/Output) [Page 4]
    * Pin 5: GND (Ground) [Page 4]

## Absolute Maximum Ratings

* Voltage Range on Any Pin Relative to Ground: -0.5V to +6.0V [Page 2]
* Operating Temperature Range: -55°C to +125°C [Page 2]
* Storage Temperature Range: -55°C to +125°C [Page 2]
* Solder Temperature: Refer to the IPC/JEDEC J-STD-020 Specification. [Page 2]

## Electrical Characteristics

* **Supply Voltage (VDD):** 3.0V to 5.5V (local power) [Page 2]
* **Pullup Supply Voltage (VPU):** 3.0V to 5.5V (parasite power), 3.0V to VDD (local power) [Page 2]
* **Thermometer Error (tERR):**
    * ±0.5°C (-10°C to +85°C) [Page 2]
    * ±1°C (30°C to +100°C) [Page 2]
    * ±2°C (-55°C to +125°C) [Page 2]
* **Input Logic-Low (VIL):** -0.3V to +0.8V [Page 2]
* **Input Logic-High (VIH):**
    * +2.2V to the lower of 5.5V or VDD + 0.3V (local power) [Page 2]
    * +3.0V to the lower of 5.5V or VDD + 0.3V (parasite power) [Page 2]
* **Sink Current (IL):** 4.0 mA (at VIO = 0.4V) [Page 2]
* **Standby Current (IDDS):** 750 nA (typ), 1000 nA (max) [Page 2]
* **Active Current (IDD):** 1 mA (typ), 1.5 mA (max) at VDD = 5V [Page 2]
* **DQ Input Current (IDQ):** 5 μA [Page 2]
* **Drift:** ±0.2°C [Page 2]

## Operating Conditions

* **Supply Voltage (VDD):** 3.0V to 5.5V
* **Temperature Range:** -55°C to +125°C
* The device can be powered by an external supply (VDD) or by "parasite power" derived from the data line (DQ). [Page 1]

## Sensor Performance / Specifications

* **Temperature Range:** -55°C to +125°C  [Page 1]
* **Accuracy:** ±0.5°C from -10°C to +85°C [Page 1]
* **Resolution:** Programmable, 9 to 12 bits [Page 1]
    * 9-bit: 0.5°C resolution
    * 10-bit: 0.25°C resolution
    * 11-bit: 0.125°C resolution
    * 12-bit: 0.0625°C resolution
* **Temperature Conversion Time (tCONV):**
    * 9-bit: 93.75 ms
    * 10-bit: 187.5 ms
    * 11-bit: 375 ms
    * 12-bit: 750 ms [Page 3]

## Communication Protocol / Interface

* **Communication Method:** 1-Wire bus [Page 1]
    * Requires only one data line (DQ) and ground. [Page 1]
    * Each device has a unique 64-bit serial code in ROM, allowing multiple devices on the same bus. [Page 1]
    * Master/slave communication.
* **Timing Characteristics:** The datasheet provides detailed timing diagrams and specifications for 1-Wire communication, including:
    * Time Slot (tSLOT)
    * Recovery Time (tREC)
    * Write 0 Low Time (tLOW0)
    * Write 1 Low Time (tLOW1)
    * Read Data Valid (tRDV)
    * Reset Time High (tRSTH)
    * Reset Time Low (tRSTL)
    * Presence-Detect High (tPDHIGH)
    * Presence-Detect Low (tPDLOW)
    * See "AC Electrical Characteristics" and Figure 2 in the datasheet.

## Register Map

The DS18B20 includes a scratchpad memory with the following: [Page 5]

* 2-byte temperature register: Stores the digital output from the temperature sensor. [Page 5]
* 1-byte upper alarm trigger register (TH) [Page 5]
* 1-byte lower alarm trigger register (TL) [Page 5]
* 1-byte configuration register:  Allows setting the temperature resolution (9, 10, 11, or 12 bits). [Page 5]

The  TH, TL, and configuration registers are nonvolatile (EEPROM). [Page 5]

## Package Information / Mechanical Dimensions

* Available in 8-pin SO (150 mils), 8-pin µSOP, and 3-pin TO-92 packages. [Page 1]
* Detailed package dimensions are not provided in this excerpt.

## Basic Usage / Application Information

A basic application setup involves connecting the DS18B20 to a microcontroller using the 1-Wire bus.  A pull-up resistor is needed on the DQ line.  The microcontroller sends commands to the DS18B20 to initiate temperature conversions and read the resulting temperature data.  The unique 64-bit serial code of each DS18B20 allows for addressing multiple sensors on the same 1-Wire bus. [Page 1, 5]

## Compliance and Certifications

The provided document does not include information on specific compliance and certifications.
