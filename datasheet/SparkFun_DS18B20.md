# SparkFun DS18B20 Waterproof Temperature Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Maxim Integrated (Chip), SparkFun Electronics (Probe Assembly)
**Sensor Model:** DS18B20 Waterproof Digital Temperature Sensor (SparkFun SEN-11050)
**Production Info:** Sensor datasheet and SparkFun assembly page reference
**Manufacturer Websites:**

* [https://www.sparkfun.com/products/11050](https://www.sparkfun.com/products/11050)
* [https://www.maximintegrated.com](https://www.maximintegrated.com) (now part of Analog Devices)

---

## General Description

The SparkFun DS18B20 is a waterproof digital temperature sensor based on the Maxim DS18B20 chip. It provides accurate temperature measurements in wet or submerged environments. With a 1-Wire interface, only one data line (plus ground) is needed for communication, making it ideal for distributed sensing setups.

\[Source: 85, 86]

---

## Theory of Operation / Sensing Principle

The DS18B20 operates using a silicon-based bandgap temperature sensor with a 12-bit ADC, outputting digital data via a 1-Wire bus. It uses parasitic power or external power and stores measurement data in scratchpad memory accessible via specific commands. Each unit includes a unique 64-bit serial code enabling multi-device support on a single bus.

\[Source: 86]

---

## Features

* Waterproof stainless steel probe design
* 1-Wire digital communication protocol
* ±0.5°C accuracy from -10°C to +85°C
* Configurable resolution (9–12 bits)
* Measurement range: -55°C to +125°C
* Each sensor has a unique 64-bit address
* Probe dimensions: 7 mm diameter, 26 mm length, 6-foot cable
* Can be powered via data line (parasitic power)

\[Source: 85, 86]

---

## Potential Applications

* Aquatic and hydroponic temperature monitoring
* Environmental monitoring in harsh conditions
* Home automation and HVAC systems
* Industrial temperature logging
* Lab instrumentation

\[Source: 85, 86]

---

## Pin Configuration and Description

**Cable Wire Colors:**

* Red: Vcc (3.0–5.5V)
* Black: GND
* White: Data (1-Wire signal)

**Sensor Package:** TO-92 inside waterproof housing
\[Source: 85]

---

## Absolute Maximum Ratings

* **Voltage on any pin:** -0.5V to +6.0V
* **Operating Temperature:** -55°C to +125°C
* **Storage Temperature:** -55°C to +125°C

\[Source: 86, page 24]

---

## Electrical Characteristics

* **Operating Voltage:** 3.0 to 5.5V
* **Operating Current:**

  * Standby: \~1 µA
  * Active: \~1.5 mA
* **Conversion Time:** 93.75 ms to 750 ms (based on resolution)
* **Resolution:** 9 to 12 bits
* **Accuracy:** ±0.5°C (-10°C to +85°C), ±2°C full range
* **Power Modes:** External or Parasite (data line only)

\[Source: 86, pages 2, 24–25]

---

## Operating Conditions

* **Temperature:** -55°C to +125°C
* **Waterproof rating:** Not officially rated, but probe is sealed for submersion
* **Power Supply:** 3.0V to 5.5V

\[Source: 85, 86]

---

## Sensor Performance / Specifications

* **Resolution:** 0.5°C (9-bit) to 0.0625°C (12-bit)
* **Response Time:** \~750 ms (12-bit mode)
* **Drift/Stability:** < ±0.2°C/year typical
* **ROM Addressing:** 64-bit laser-etched unique ID per sensor

\[Source: 86, pages 2–3, 24–25]

---

## Communication Protocol / Interface

* **Interface:** 1-Wire digital protocol
* **Commands:**

  * Convert T \[0x44]
  * Read Scratchpad \[0xBE]
  * Write Scratchpad \[0x4E]
  * Copy Scratchpad \[0x48]
  * Recall E2 \[0xB8]
  * Read Power Supply \[0xB4]
* **ROM Functions:**

  * Read ROM \[0x33]
  * Match ROM \[0x55]
  * Skip ROM \[0xCC]
  * Alarm Search \[0xEC]
* **Bus Speed:** Standard (15.3 kbps) to Overdrive (125 kbps)

\[Source: 86, pages 10–18]

---

## Register Map

* **Scratchpad Memory (9 bytes):**

  * Byte 0–1: Temperature (LSB, MSB)
  * Byte 2–4: TH, TL, Configuration register
  * Byte 5–7: Reserved
  * Byte 8: CRC
* **EEPROM:** Stores TH, TL, config via Copy Scratchpad command

\[Source: 86, pages 8–10]

---

## Package Information / Mechanical Dimensions

* **Sensor Package:** TO-92 inside stainless steel probe
* **Probe Diameter:** \~7 mm
* **Probe Length:** \~26 mm
* **Cable Length:** 6 feet (1.8 meters)
* **Connector:** Bare wire leads (Red, Black, White)

\[Source: 85]

---

## Basic Usage / Application Information

**Wiring Example (with pull-up):**

* Red → Vcc (3.3V or 5V)
* Black → GND
* White → Digital I/O (with 4.7kΩ pull-up to Vcc)

**Initialization Sequence:**

* Reset → Presence Pulse → ROM Command → Function Command

**Data Reading Process:**

1. Issue Reset + ROM command (Match/Skip)
2. Send Convert T (0x44) command
3. Wait for conversion (up to 750 ms)
4. Issue Reset → ROM command → Read Scratchpad (0xBE)
5. Read 9 bytes and verify CRC

\[Source: 86, pages 10–18, 22–23]

---

## Compliance and Certifications

* **RoHS Compliant:** Yes (per SparkFun SEN-11050)
* **Waterproofing:** Probe assembly is sealed, though no IP rating declared

\[Source: 85]
