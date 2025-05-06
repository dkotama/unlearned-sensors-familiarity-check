# Sensirion SHT3x-DIS Humidity and Temperature Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Sensirion AG
**Sensor Model:** SHT3x-DIS (SHT30-DIS, SHT31-DIS, SHT35-DIS)
**Production Date / Document Version:** December 2022 – Version 7
**Manufacturer Website:** [www.sensirion.com](http://www.sensirion.com)
**Headquarters Address:** Laubisruetistr. 50, CH-8712 Staefa ZH, Switzerland
**Phone:** +41 44 306 40 00
\[page 1, 22]

---

## General Description

The SHT3x-DIS is a digital humidity and temperature sensor featuring Sensirion's CMOSens® technology. It includes fully calibrated, linearized, and temperature-compensated digital output via I2C. With a wide operating voltage (2.15–5.5V), fast response, and small form factor (2.5×2.5×0.9 mm DFN), the SHT3x-DIS series suits a wide range of consumer, industrial, and scientific applications.

\[page 1]

---

## Theory of Operation / Sensing Principle

SHT3x-DIS integrates capacitive humidity sensing and bandgap temperature sensing on a single CMOS chip, with analog signal conditioning, A/D conversion, calibration data memory, and a digital interface. The factory-calibrated data is linearized and temperature-compensated before output.

\[page 1]

---

## Features

* Fully calibrated, linearized, and temperature-compensated output
* CMOSens® technology for long-term stability and reliability
* 2 user-selectable I2C addresses
* Communication speeds up to 1 MHz (I2C)
* Tiny 8-pin DFN package (2.5 × 2.5 × 0.9 mm)
* Internal heater for diagnostics
* NIST traceable calibration
  \[pages 1, 2, 8]

---

## Potential Applications

* HVAC and climate control
* Consumer electronics
* Medical devices
* Environmental monitoring
* Industrial process control
  \[page 1]

---

## Pin Configuration and Description

| Pin | Name   | Function                                    |
| --- | ------ | ------------------------------------------- |
| 1   | SDA    | Serial data (I2C input/output)              |
| 2   | ADDR   | I2C address selection input                 |
| 3   | ALERT  | Programmable alert output (float if unused) |
| 4   | SCL    | Serial clock (I2C)                          |
| 5   | VDD    | Supply voltage input                        |
| 6   | nRESET | External reset (active low, optional)       |
| 7   | R      | No electrical function (connect to GND)     |
| 8   | VSS    | Ground                                      |

\[page 8]

---

## Absolute Maximum Ratings

* **Supply Voltage:** -0.3V to 6V
* **Pin Voltage Range:** -0.3V to VDD+0.3V
* **Input Current on Any Pin:** ±100 mA
* **Operating Temperature:** -40°C to +125°C
* **Storage Temperature:** -40°C to +150°C
* **ESD Rating:** 4kV HBM, 750V CDM
  \[page 7]

---

## Electrical Characteristics

* **Supply Voltage Range:** 2.15V to 5.5V
* **Idle Current:** 0.2–45 µA (depending on mode and temperature)
* **Measuring Current:** 600–1500 µA
* **Typical Current (1 meas/sec, low repeat.):** \~1.7 µA
* **Heater Power:** 3.6–33 mW
* **Response Time (Humidity):** τ63% < 8s (ART enabled), 86s (standard)
  \[pages 6–7]

---

## Operating Conditions

* **Recommended:** 5–60°C, 20–80% RH
* **Full Operating Range:** -40°C to 125°C, 0–100% RH (non-condensing)
* **Recalibration Interval:** Recommended every 2 years
  \[pages 2, 6]

---

## Sensor Performance / Specifications

### Humidity (SHT35)

* **Accuracy:** ±1.5% RH (typical), see Figure 4
* **Repeatability:** 0.08–0.21% RH (mode dependent)
* **Resolution:** 0.01% RH
* **Hysteresis:** ±0.8% RH
* **Long-term Drift:** <0.25% RH/year

### Temperature (SHT35)

* **Accuracy:** ±0.1°C (typical, 20–60°C)
* **Repeatability:** 0.04–0.15°C
* **Resolution:** 0.01°C
* **Long-term Drift:** <0.03°C/year
  \[pages 2–3]

---

## Communication Protocol / Interface

* **Interface:** I2C with Fast Mode (up to 1 MHz)
* **Commands:** 16-bit hex (e.g., 0x2C06 for high repeatability with clock stretching)
* **Data Format:** 16-bit temperature + 16-bit humidity + CRC for each
* **Command Modes:**

  * Single Shot
  * Periodic (0.5–10 Hz)
  * ART Mode (accelerated response time)
* **Reset Options:** Soft, General Call, nRESET pin
  \[pages 9–13]

---

## Register Map

No conventional register map; uses command-based interface with 16-bit instructions:

* **Measurement Commands:** e.g., 0x2C06 (high rep., clock stretch), 0x2130 (1 mps periodic)
* **Status Register:** 0xF32D (read), 0x3041 (clear)
* **Heater Control:** 0x306D (enable), 0x3066 (disable)
* **Reset:** 0x30A2 (soft), 0x0006 (general call)
  \[pages 10–13]

---

## Package Information / Mechanical Dimensions

* **Package Type:** 8-pin DFN (dual flat no-lead)
* **Dimensions:** 2.5 × 2.5 × 0.9 mm
* **Land Pattern:** Defined in Figure 15 with NSMD recommended
* **Moisture Sensitivity Level (MSL):** 1 (per IPC/JEDEC J-STD-020)
  \[pages 16–17]

---

## Basic Usage / Application Information

* Mount sensor where airflow can reach humidity port
* Use 100 nF decoupling cap near VDD
* Implement I2C pull-up resistors (e.g., 10 kΩ)
* Use nRESET pin or command for reset
* Enable heater only for diagnostics
* Recalibrate every 2 years for best accuracy
  \[pages 8–13, 16]

---

## Compliance and Certifications

* **RoHS and WEEE Compliant**
* **ESD Protection:** 4kV HBM / 750V CDM
* **JEDEC Qualified (JESD47)**
  \[page 19]
