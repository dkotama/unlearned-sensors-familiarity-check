# Omega EWSA-PT100 Temperature Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Omega Engineering, Inc.
**Sensor Model:** EWSA-Pt100 (and EWSA-Pt100-TX)
**Production Date:** Not explicitly stated; document ID M5732/0119, indicating January 2019
**Manufacturer Website:** [www.omega.com](http://www.omega.com)
**Support Email:** [info@omega.com](mailto:info@omega.com)
\[page 1, 3]

---

## General Description

The EWSA series consists of rugged, weatherproof air temperature sensors designed for wall or pipe mounting in both indoor and outdoor harsh environments. It features a sheathed RTD probe housed within a protective aluminum enclosure rated to IP65. The sensor is ideal for ambient air monitoring and features options for integrated transmitters.

\[page 1]

---

## Theory of Operation / Sensing Principle

The EWSA-Pt100 operates using a platinum resistance temperature detector (RTD), specifically a Pt100 class A 4-wire element. The resistance of the RTD changes with temperature, which is measured and interpreted by either direct connection (sensor-only model) or via a loop-powered transmitter that scales the output to 4–20 mA.

\[page 1, 2]

---

## Features

* Rugged aluminum alloy housing (IP65 rated)
* 6 mm diameter sheathed Pt100 sensor
* Protection tube: 12.7 mm diameter
* M20 cable gland (2.5–6.5 mm cable compatibility)
* Optional 2-wire transmitter with 4–20 mA scaling
* Designed for wall or pipe mounting
  \[page 1]

---

## Potential Applications

* Outdoor environmental air monitoring
* HVAC and building control systems
* Industrial process monitoring
* Temperature surveillance in rugged locations
  \[page 1]

---

## Pin Configuration and Description

**EWSA-Pt100 (sensor only):**

* Screw terminal block for 4-wire Pt100 RTD connection

**EWSA-Pt100-TX (with transmitter):**

* Screw terminals for 2-wire current loop connection

\[page 2]

---

## Absolute Maximum Ratings

Not explicitly listed in the datasheet. General limitations include the specified ambient operating ranges and cable gland size limits (2.5 mm to 6.5 mm diameter).

---

## Electrical Characteristics

**EWSA-Pt100-TX (transmitter model):**

* **Power Supply:** 10 to 30 VDC, loop-powered
* **Output Signal:** 4–20 mA (scaled: 4 mA at -25°C, 20 mA at 75°C)
* **Load Resistance Formula:** Rload = (Vsupply - 10 V) / 0.02 A

  * e.g., 700 Ω at 24 V

\[page 2]

---

## Operating Conditions

* **EWSA-Pt100:** -50 to 100°C ambient
* **EWSA-Pt100-TX:** -40 to 85°C ambient at 10–90% RH (non-condensing)
  \[page 2]

---

## Sensor Performance / Specifications

* **Sensor Type:** Pt100 Class A 4-wire (Pt1000 available upon request)
* **Sensor Protection Tube:** 75 mm long, 12.7 mm diameter
* **Box Dimensions:** 80 mm W × 75 mm H × 58 mm D
  \[page 2]

---

## Communication Protocol / Interface

* **EWSA-Pt100:** Passive sensor with direct resistance output via 4-wire RTD connection
* **EWSA-Pt100-TX:** Analog 4–20 mA loop-powered output (scaled temperature)

\[page 2]

---

## Register Map

Not applicable — analog and passive resistance-based interface only.

---

## Package Information / Mechanical Dimensions

* **Sensor Length:** 75 mm
* **Sensor Diameter:** 12.7 mm
* **Enclosure Dimensions:** 80 × 75 × 58 mm (W×H×D)
* **Cable Entry:** M20 gland for 2.5–6.5 mm OD cables
  \[page 2]

---

## Basic Usage / Application Information

* Mount the sensor on a wall or pipe using provided enclosure base dimensions
* Connect sensor to a 4-wire Pt100 circuit (EWSA-Pt100) or 2-wire current loop (EWSA-Pt100-TX)
* For transmitter-equipped models, refer to transmitter manual M4561 for wiring and scaling

\[page 2]

---

## Compliance and Certifications

* **Ingress Protection:** IP65-rated aluminum housing
* **Warranty:** 13-month limited warranty by Omega Engineering
  \[page 1, 3]
