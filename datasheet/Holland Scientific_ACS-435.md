# Crop Circle ACS-435 Sensor Documentation

## Manufacturer Info

**Manufacturer Name:** Holland Scientific
**Sensor Model:** Crop Circle ACS-435
**Production Date:** Not explicitly stated; datasheet version dated February 2021.
**Manufacturer Website:** [www.hollandscientific.com](http://www.hollandscientific.com)
**Contact Info:** 6001 South 58th Street, Suite D, Lincoln, NE 68516
**Tel/Fax:** (402) 488-1226
**Email:** [sales@hollandscientific.com](mailto:sales@hollandscientific.com)
\[page 1]

---

## General Description

The Crop Circle ACS-435 is an active crop canopy sensor designed to measure vegetation indices and reflectance data from plant canopies and soil. Unlike passive sensors, it operates independently of ambient lighting, allowing measurements both day and night. It is suitable for vehicle, pole-mounted, or handheld applications and provides insight into biomass, nutrients, water, disease, and other growing conditions.

\[page 1]

---

## Theory of Operation / Sensing Principle

The ACS-435 uses a modulated polychromatic LED light source and a three-channel silicon photodiode array to actively illuminate and measure crop/soil reflectance at 670 nm, 730 nm, and 780 nm. Its unique technology allows for height-independent reflectance measurement, ensuring accuracy regardless of distance from the target within the specified range.

\[page 1]

---

## Features

* Three optical measurement channels
* Measures NDVI (Normalized Difference Vegetation Index) and NDRE (Normalized Difference Red Edge)
* Day or night operation
* Immune to AC and fluorescent lighting interference
* Wide sensor-to-canopy range: 0.25 m to 2.5 m
* Rugged, dust and water resistant (IP68)
* Low noise and fast data output
* Low power consumption
  \[page 1]

---

## Potential Applications

* Remote sensing and mapping of crop canopy biomass
* Nutrient management and crop health assessment
* Precision agriculture and variable-rate application systems
* Plant stress analysis and research
  \[page 1]

---

## Pin Configuration and Description

**Connector Type:** 12-pin Deutsch, O-ring sealed
Specific pinout is not detailed in the datasheet. Further documentation from the manufacturer may be required for full pin mapping.

\[page 1]

---

## Absolute Maximum Ratings

Not explicitly listed in the datasheet. Use operating limits with caution and consult the manufacturer for exact absolute maximum ratings.

---

## Electrical Characteristics

* **Power Supply:** 11 to 16.5V DC
* **Current Draw:** \~180 mA
* **Sample Output Rate:** Up to 10 samples/sec (in autosend mode)
* **Communication Interface:** RS-485 (bidirectional), RS-232 (output only)
* **RS-232 Settings:** 38400 baud, no parity, 8 data bits, 1 stop bit

### Power Consumption Breakdown

Only total draw (\~180 mA) is provided; breakdown by operational mode not included in the datasheet.

\[page 1]

---

## Operating Conditions

* **Operating Temperature Range:** 0 to 50 ºC
* **Environmental Protection:** IP68 (dust and water resistant)
  \[page 1]

---

## Sensor Performance / Specifications

* **Sensor-to-Canopy Range:** 10 in (25 cm) to 98 in (250 cm)
* **Field-of-View:** \~40 degrees by \~10 degrees
* **Measurement Bands:** 670 nm, 730 nm, 780 nm
* **Height-independent spectral reflectance**
* **Photodetection:** Three-channel silicon photodiode array
  \[page 1]

---

## Communication Protocol / Interface

* **RS-485:** Multi-drop, bidirectional communication
* **RS-232:** Autosend, output only
* **RS-232 Configuration:** 38400 baud, 8 data bits, 1 stop bit, no parity
  \[page 1]

---

## Register Map

Not provided in the datasheet. Access to the register map may require additional technical documentation or developer access from Holland Scientific.

---

## Package Information / Mechanical Dimensions

* **Enclosure:** Injection-molded polycarbonate
* **Weight:** 0.9 lb (435 g)
* **Mounting:** (2) M6 x 1 threaded holes, 1.25 in (3.18 cm) apart
* **Dimensions:**

  * Width: 3.5 in (8.9 cm)
  * Length: 7.9 in (20.1 cm)
  * Height: 1.9 in (4.8 cm)
    \[page 1]

---

## Basic Usage / Application Information

* Compatible with **GeoSCOUT X** datalogger
* Data stored on internal SD card in CSV format
* Ready-to-use packages available:

  * **Handheld System:** Sensor, GeoSCOUT X, pole, cables, charger, case, and guide
  * **Mapping System:** Sensor, GeoSCOUT X, cables, mounting plate, case, and guide

Further usage details (e.g., initialization and pseudocode) are not included in this document.

\[page 1]

---

## Compliance and Certifications

* **EMC Certification:** CE compliant
  \[page 1]
