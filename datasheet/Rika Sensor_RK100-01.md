# Rika WM-RK100-01 Wind Speed Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Rika Sensors
**Sensor Model:** WM-RK100-01 Wind Speed Sensor
**Document Code:** WM-RK100-01DB1500
**Manufacturer Website:** Not listed in this document; typical manufacturer site: [https://www.rikasensor.com](https://www.rikasensor.com)

---

## General Description

The WM-RK100-01 Wind Speed Sensor is built for accurate and reliable wind velocity measurement in harsh environments. It features digital circuitry with strong resistance to RFI/EMI, automatic temperature compensation, and multiple output formats. Its robust construction includes a 304 stainless steel wind cup and aluminum alloy body with IP65 ingress protection, making it ideal for outdoor and industrial applications.

\[page 1]

---

## Theory of Operation / Sensing Principle

The sensor operates via electromagnetic induction. As wind turns the stainless-steel cups, rotation speed correlates linearly with wind velocity. Internal electronics convert this into electrical output (pulse, voltage, current, or RS485). Temperature compensation ensures consistent readings across environments.

\[page 1]

---

## Features

* Low starting threshold (<0.5 m/s)
* All-metal construction (aluminum and stainless steel)
* Strong resistance to corrosion
* Wind cup load capacity up to 70 m/s
* Double bearing design for durability
* Surge protection
* Easy to install flange-mounted base

\[page 1]

---

## Potential Applications

* Weather monitoring stations
* High-altitude safety monitoring
* Solar and wind energy systems
* Ports and marine applications
* Mobile weather stations
* Remote airports and helipads
* Tunnel monitoring (road and rail)

\[page 1]

---

## Pin Configuration and Description

Wiring and pin definitions are not explicitly provided in this document. Standard configurations based on output type (pulse, voltage, current, RS485) apply; reference to specific device wiring manual recommended.

---

## Absolute Maximum Ratings

* **Wind Load Limit:** 70 m/s
* **Operating Temperature Range:** -30°C to +70°C
* **Storage Conditions:** 10°C to 60°C @ 20%–90% RH

\[page 1]

---

## Electrical Characteristics

| Output Type     | Supply Voltage | Load Capacity     | Accuracy                             |
| --------------- | -------------- | ----------------- | ------------------------------------ |
| Pulses          | 5–24 VDC       | >2kΩ              | ±0.5 m/s (<5 m/s), ±3% FS (≥5 m/s)   |
| 4–20 mA         | 12–24 VDC      | <500Ω (typ. 250Ω) | ±0.5 m/s (<5 m/s), ±3% FS (≥5 m/s)   |
| 0–5V/0–10V/1–5V | 12–24 VDC      | >2kΩ              | ±0.5 m/s (<5 m/s), ±2–3% FS (≥5 m/s) |
| RS485           | 12–24 VDC      | —                 | ±0.5 m/s (<5 m/s), ±3% FS (≥5 m/s)   |

**Power Requirements:** Depends on output signal type
**Starting Threshold:** <0.5 m/s

\[page 1]

---

## Operating Conditions

* **Temperature:** -30°C to +70°C
* **Humidity:** 20% to 90% RH (storage)
* **Ingress Protection:** IP65

\[page 1]

---

## Sensor Performance / Specifications

* **Wind Speed Range:** 0–30 m/s or 0–60 m/s (depending on model)
* **Accuracy:** ±0.5 m/s (<5 m/s), ±2–3% FS (≥5 m/s)
* **Response Type:** Linear
* **Dimensions:**

  * Cup Rotor Diameter: 200 mm
  * Height: 150 mm
  * Weight: 240 g (unpacked)
* **Materials:**

  * Wind Cup: 304 Stainless Steel
  * Main Body: Aluminum Alloy with polyester powder coating

\[page 1]

---

## Communication Protocol / Interface

* **Pulses Output Transfer Function:**

  * For 0–30 m/s: V = 0.667 × F
  * For 0–60 m/s: V = 1.333 × F
    (Where V = wind speed in m/s, F = frequency in Hz)

* **Voltage Output Transfer Function:**

  * V = U / (FS voltage – zero voltage) × 30 (for 0–30 m/s)
  * V = U / (FS voltage – zero voltage) × 60 (for 0–60 m/s)
    (Where U = measured voltage)

* **RS485 Output:** Uses standard Modbus protocol. For cable lengths >100m, use 120Ω termination resistors at each end.

\[page 1]

---

## Register Map

Not provided in this document. RS485/Modbus devices typically require a separate protocol specification from the manufacturer.

---

## Package Information / Mechanical Dimensions

* **Cup Rotor Diameter:** 200 mm
* **Height:** 150 mm
* **Weight:** 240 g
* **Mounting:** Flange mount with 4-point screw bracket; sensor must be kept horizontal

\[page 1]

---

## Basic Usage / Application Information

* Mount the sensor using 4 screws and ensure it is horizontal.
* Choose appropriate output type (pulse, voltage, current, or RS485) depending on your data acquisition system.
* For RS485 applications over long distances, install termination resistors (120Ω) at both ends.

\[page 1]

---

## Compliance and Certifications

Not explicitly listed in this document. IP65 ingress protection and industrial-grade build quality imply suitability for harsh and outdoor conditions.

\[page 1]
