# Soil Nitrogen, Phosphorus, and Potassium Three-in-One Fertility Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Shandong Renke Measurement & Control Technology Co., Ltd.
**Sensor Model:** RS-NPK-N01-TR (Three-in-One Fertility Sensor Type 485)
**Document Version:** V1.0
**Manufacturer Website:** [www.renkeer.com](http://www.renkeer.com), [www.rkckth.com](http://www.rkckth.com)
**Support Phone:** 400-085-5807
**Address:** 2/F, East Block, Building 8, Shun Tai Plaza, High-tech Zone, Jinan City, Shandong Province, 250101, China
\[page 13]

---

## General Description

This sensor is designed to detect soil fertility by measuring the concentrations of nitrogen (N), phosphorus (P), and potassium (K) using a specially treated electrode. It provides real-time soil nutrient data to support precision agriculture, forestry, geological exploration, and plant cultivation. It is waterproof, corrosion-resistant, and can be buried for long-term monitoring.

\[page 4]

---

## Theory of Operation / Sensing Principle

The sensor uses electrodes made of a treated alloy that detect ion concentrations in soil, representing nitrogen, phosphorus, and potassium levels. The measurements are transmitted using the RS485 Modbus-RTU protocol. Calibration coefficients allow for fine-tuning using standard Modbus registers.

\[pages 4, 9]

---

## Features

* No reagents required, unlimited test cycles
* High measurement accuracy and fast response
* Durable alloy electrode with resistance to strong forces
* Fully sealed (IP68), acid and alkali resistant
* Suitable for long-term dynamic monitoring when buried
* Probe insertion design for accurate contact with soil
  \[page 4]

---

## Potential Applications

* Precision agriculture
* Soil fertility mapping and monitoring
* Forestry and plant cultivation
* Geological and environmental research
  \[page 4]

---

## Pin Configuration and Description

**Wiring Instructions:**

* Brown: Power supply 5–30 VDC
* Black: Ground
* Yellow: RS485-A
* Blue: RS485-B

\[page 7]

---

## Absolute Maximum Ratings

Not explicitly provided; recommended to operate within 0–55°C, 5–30 VDC supply range. Do not subject to physical abuse or prolonged unpowered operation in high RF environments.

\[pages 4, 6]

---

## Electrical Characteristics

* **Power Supply:** 5–30 VDC
* **Power Consumption:** ≤0.15 W @ 12V, 25°C
* **Output Signal:** RS485 (Modbus-RTU)
* **Response Time:** <1 second
* **Communication Parameters:** 8 data bits, no parity, 1 stop bit, CRC checking; default baud rate 4800bps

\[pages 4, 8–9]

---

## Operating Conditions

* **Operating Temperature:** 0°C to 55°C
* **Protection Rating:** IP68 (fully submersible and waterproof)
* **Environment:** Avoid direct sunlight and strong RF fields during powered operation

\[pages 4, 6]

---

## Sensor Performance / Specifications

* **Measurement Range:** 1–1999 mg/kg (for N, P, and K)
* **Resolution:** 1 mg/kg
* **Accuracy:** ±2% FS
* **Probe Material:** Stainless steel
* **Sealing Material:** Black flame-retardant epoxy resin
* **Dimensions:** 45 × 15 × 123 mm
* **Default Cable Length:** 2 meters (customizable)

\[page 4]

---

## Communication Protocol / Interface

* **Protocol:** RS485 using Modbus-RTU
* **Factory Default Address:** 0x01
* **Factory Default Baud Rate:** 4800 bps
* **Example Read Command:** To read nitrogen value:

  * Request: `01 03 00 1E 00 01 E4 0C`
  * Response: `01 03 02 00 20 B9 9C` → Nitrogen = 32 mg/kg

\[pages 9–11]

---

## Register Map

| Register Address (Hex) | Decimal     | Parameter                            | Access     | Description                      |
| ---------------------- | ----------- | ------------------------------------ | ---------- | -------------------------------- |
| 001E                   | 40031       | Nitrogen content                     | Read-only  | Real-time nitrogen level         |
| 001F                   | 40032       | Phosphorus content                   | Read-only  | Real-time phosphorus level       |
| 0020                   | 40033       | Potassium content                    | Read-only  | Real-time potassium level        |
| 03E8–03EA              | 41001–41003 | Nitrogen coefficient & calibration   | Read/Write | IEEE754 float / integer          |
| 03F2–03F4              | 41011–41013 | Phosphorus coefficient & calibration | Read/Write | IEEE754 float / integer          |
| 03FC–03FE              | 41021–41023 | Potassium coefficient & calibration  | Read/Write | IEEE754 float / integer          |
| 07D0                   | 42001       | Device address                       | Read/Write | 1–254 (default: 1)               |
| 07D1                   | 42002       | Baud rate                            | Read/Write | 0=2400, 1=4800 (default), 2=9600 |

\[pages 9–10]

---

## Package Information / Mechanical Dimensions

* **Sensor Dimensions:** 45 mm × 15 mm × 123 mm
* **Cable Length:** Default 2 meters, customizable
* **IP Rating:** IP68 — fully submersible

\[page 4, 5]

---

## Basic Usage / Application Information

**Quick Test Method:**

* Remove surface soil and insert probe vertically, ensuring full needle contact
* Avoid hard objects and repeat measurements for accuracy

**Buried Installation:**

* Horizontally insert probe into a soil pit wall >20 cm wide
* Bury tightly and allow stabilization for long-term monitoring

**Precautions:**

* Avoid bending the sensor or pulling wires
* Do not expose to direct sunlight or energize without soil contact for long durations

\[pages 5–6]

---

## Compliance and Certifications

No specific certifications listed; designed for robust field use with waterproof sealing and chemical resistance. Ensure use in non-explosive, non-corrosive gas environments.

\[page 4, 6]
