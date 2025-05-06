# Delta-T Devices WET150 Sensor Information

This document provides an overview of the Delta-T Devices WET150 Sensor, based on the provided PDF programmer's guide. The WET150 is a sensor that measures soil moisture, conductivity, and temperature. [Page 1]

## Manufacturer Info

* **Manufacturer:** Delta-T Devices Ltd [Page 1, 24]
* **Model Name/Number:** WET150 [Page 1]
* **Website:** Not Available in document.

## General Description

The WET150 is a sensor that measures three parameters: soil moisture (volumetric water content), electrical conductivity (EC), and soil temperature. It is designed for use in soil and other porous materials. [Page 1]

## Theory of Operation / Sensing Principle

The WET150 measures:

* **Volumetric Water Content (VWC):** By measuring the dielectric permittivity of the soil.
* **Electrical Conductivity (EC):** Using an alternating current (AC) to measure the soil's resistance to electrical flow.
* **Temperature:** With an internal temperature sensor. [Page 1]

## Features

* Measures soil moisture, electrical conductivity, and temperature. [Page 1]
* SDI-12 interface for communication. [Page 1]
* Low power consumption.
* Robust design for long-term use in the field.
* Various measurement sets and customization options. [Page 5]
* Factory calibration, with options for soil-specific calibration. [Page 12, 14]

## Potential Applications

* Soil science research
* Hydrology studies
* Agriculture and irrigation management
* Environmental monitoring

## Pin Configuration and Description

The WET150 uses the SDI-12 protocol for communication, which typically involves three wires:

* Power (+V)
* Ground (GND)
* Data (SDI-12)

The specific pin configuration may vary depending on the cable and connector used.  Refer to the cable wiring diagram. [page 2]

## Absolute Maximum Ratings

The document does not provide a section on absolute maximum ratings.

## Electrical Characteristics

* **Power Supply Voltage:** 7 V to 16 V DC [Page 2]
* **Current Consumption:**
    * <6 mA (during measurement)
    * <100 μA (in standby) [Page 2]

## Operating Conditions

The WET150 is designed to operate in typical soil conditions, but specific operating temperature and humidity ranges are not provided in this document.  The operating temperature is -20C to +60C.

## Sensor Performance / Specifications

* **Volumetric Water Content (VWC) Range:** 0 to 100% [Page 6]
* **VWC Accuracy:** ± 0.03 m³/m³ (mineral soils), ± 0.02 m³/m³ (with soil-specific calibration) [Page 6]
* **VWC Resolution:** 0.001 m³/m³ [Page 6]
* **Electrical Conductivity (EC) Range:** 0 to 2000 mS/m [Page 6]
* **EC Accuracy:**
    * ± 0.05 dS/m + 5% of reading (0 to 1000 mS/m)
    * ± 10% of reading (1000 to 2000 mS/m) [Page 6]
* **EC Resolution:** 0.01 mS/m (0 to 200 mS/m), 0.1 mS/m (200 to 2000 mS/m) [Page 6]
* **Temperature Range:** -20 to +60 °C [Page 6]
* **Temperature Accuracy**: ± 0.5 °C [Page 6]
* **Temperature Resolution:** 0.1 °C
* **Measurement Time:** 0.3 seconds [Page 6]

## Communication Protocol / Interface

* SDI-12 [Page 1]

## Register Map

The WET150 does not have a traditional register map in the sense of addressable memory locations. Instead, it uses the SDI-12 protocol, which involves sending commands and receiving responses. The document details various SDI-12 commands for taking measurements, configuring the sensor, and performing other operations. [Page 9]

## Package Information / Mechanical Dimensions

The document provides the following dimensions:
* **Sensor Head Length:** 80 mm
* **Sensor Head Diameter:** 19 mm
* **Needle Length: 50 mm
* **Cable Length:** 5m [Page 2]

## Basic Usage / Application Information

The WET150 is designed to be inserted into the soil or other material of interest. It is then connected to an SDI-12 data logger, which sends commands to the sensor and records the measured data. The document provides detailed information on:

* SDI-12 communication
* Measurement commands
* Customizing measurement sets
* Performing soil calibrations
* Configuring EC parameters [Page 7-20]

## Compliance and Certifications

The document does not provide information on compliance and certifications.
