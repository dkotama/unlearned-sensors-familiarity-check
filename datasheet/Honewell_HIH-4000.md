# HIH-4000 Series Humidity Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Honeywell Sensing and Control
**Sensor Model:** HIH-4000 Series (includes HIH-4000-001, HIH-4000-002, HIH-4000-003, HIH-4000-004, HIH-4000-005)
**Production Date:** Document dated February 2010, Issue 4
**Manufacturer Website:** [www.honeywell.com/sensing](http://www.honeywell.com/sensing)
**Address:** 1985 Douglas Drive North, Golden Valley, MN 55422
\[page 3]

---

## General Description

The HIH-4000 Series are analog humidity sensors designed to measure relative humidity in non-condensing environments. These sensors offer high reliability and are suitable for applications requiring accurate humidity data. They output a ratiometric voltage that corresponds to the relative humidity.

\[page 2]

---

## Theory of Operation / Sensing Principle

The HIH-4000 uses a capacitive polymer sensor element that varies capacitance based on the ambient relative humidity. The analog voltage output is proportional to this capacitance, and therefore, to the relative humidity level. The device includes on-chip signal conditioning and temperature compensation circuitry.

\[page 2]

---

## Features

* High accuracy and reliability
* Temperature compensation
* Linear voltage output
* Fast response time (\~5 seconds)
* Compact and PCB-mountable
* Light-sensitive (needs to be shaded from intense light)
* Non-condensing operation only
  \[page 2]

---

## Potential Applications

* HVAC systems
* Medical devices
* Industrial process control
* Weather stations and environmental monitoring
* Consumer electronics with humidity sensing
  \[page 2]

---

## Pin Configuration and Description

For HIH-4000-001/003/005:

* **Pin 1:** -ve (Ground)
* **Pin 2:** +ve (Supply Voltage)
* **Pin 3:** OUT (Analog Output)

For HIH-4000-002/004:

* **Pin 1:** -ve (Ground)
* **Pin 2:** +ve (Supply Voltage)
* **Pin 3:** OUT (Analog Output)

\[page 3]

---

## Absolute Maximum Ratings

Not explicitly stated in the document. However, moisture and light exposure limitations and proper mounting/soldering guidelines are given to avoid damage.

\[page 2]

---

## Electrical Characteristics

* **Supply Voltage:** 4 to 5.8 VDC (calibrated at 5 VDC)
* **Supply Current:** 200 µA (typical), 500 µA (maximum)
* **Output Voltage Formula:** VOUT = VSUPPLY \* \[0.0062(sensor RH) + 0.16]
* **Output Voltage Temp Coefficient at 50% RH, 5V:** -4 mV/°C
* **Temperature Compensation Formula:** True RH = Sensor RH / (1.0546 - 0.00216\*T), T in °C

\[page 2]

---

## Operating Conditions

* **Operating Temperature Range:** -40°C to 85°C
* **Operating Humidity Range:** 0 to 100% RH (non-condensing)
* **Storage Temperature Range:** -50°C to 125°C
* **Storage Humidity:** 0 to 100% RH (non-condensing)
* **Recommended Operating Environment:** See Figure 1 on page 2

\[page 2]

---

## Sensor Performance / Specifications

* **Accuracy (Best Fit Straight Line):** ±3.5% RH
* **Interchangeability:** ±5% RH (0–59% RH), ±8% RH (60–100% RH)
* **Hysteresis:** 3% RH
* **Repeatability:** ±0.5% RH
* **Settling Time:** 70 ms
* **Response Time:** 5 s (1/e in slow moving air)
* **Stability (at 50% RH):** ±1.2% RH/year

\[page 2]

---

## Communication Protocol / Interface

* **Analog Voltage Output** — direct voltage proportional to relative humidity
  \[page 2]

---

## Register Map

Not applicable — sensor uses analog output only.

---

## Package Information / Mechanical Dimensions

* **Package Type:** Through-hole, PCB mountable
* **Typical Mounting Dimensions (HIH-4000-001/003/005):**

  * Height: 12.7 mm min
  * Width: 8.59 mm
  * Lead Spacing: 2.54 mm
  * Lead Diameter: 0.38 mm

Refer to Figure 3 for detailed dimensions.

\[page 3]

---

## Basic Usage / Application Information

* Mount with face exposed to atmosphere
* Avoid touching sensor surface
* Clean after soldering with isopropyl alcohol
* Use no-clean flux and maintain 250°C to 260°C soldering temp
* Shade from intense light to avoid CMOS signal distortion
* Handle using package edges or leads

\[page 1, 2]

---

## Compliance and Certifications

* **Environmental Compliance:** Must be disposed per WEEE Directive 2002/96/EC
* **Safety Note:** Housing does not provide electrical isolation; install in safe, enclosed area
  \[page 1, 3]
