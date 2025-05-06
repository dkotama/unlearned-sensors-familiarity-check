# Campbell Scientific 05103 Wind Monitor Information

This document provides a detailed overview of the Campbell Scientific 05103 Wind Monitor, based on information from the provided PDF product manual. The 05103 is manufactured by R.M. Young and integrated into Campbell Scientific systems. Other models in the series are also mentioned for completeness.

## Manufacturer Info

* **Manufacturer:** R. M. Young (integrated/distributed by Campbell Scientific) [Page 1, 5]
* **Model Name/Number:** 05103 Wind Monitor (and series) [Page 1]
* **Website:** www.campbellsci.com [Page 2]

## General Description

The Wind Monitor Series measures horizontal wind speed and direction. The 05103 is the standard model in the series. Other models are designed for heavy-duty or specialized applications. The sensors are designed for use with Campbell Scientific data loggers. [Page 1, 5]

## Theory of Operation / Sensing Principle

* Wind speed is measured by a four-blade propeller. The propeller's rotation produces an AC sine wave signal with a frequency proportional to wind speed. [Page 5]
* Vane position (wind direction) is measured by a 10 kΩ potentiometer. With a precision excitation voltage, the output voltage is proportional to wind direction. [Page 5]

## Features

* Rugged design for harsh environments [Page 5]
* Corrosion-resistant thermoplastic construction (sea-air and atmospheric pollutants) [Page 5]
* Suitable for wind profile studies [Page 5]
* Compatible with Campbell Scientific CRBasic data loggers [Page 5]
* Compatible with LLAC4 4-channel Low Level AC Conversion Module (increases number of anemometers measurable by a single data logger) [Page 5]

## Potential Applications

* General meteorological monitoring
* Wind profile studies

## Pin Configuration and Description

The manual describes wiring the sensor to Campbell Scientific data loggers. For example, the 05103 connects to a CR1000X as follows: [Page 4]

| Wire Color | Function           | CR1000X Terminal |
|------------|--------------------|-------------------|
| Green      | Wind Speed Signal  | 1H                |
| Black      | Ground             | ┴ (Ground)        |
| Clear      | Ground             | ┴ (Ground)        |
| White      | Ground             | ┴ (Ground)        |
| Red        | Excitation Voltage | P1                |
| Blue       | Wind Direction     | VX1               |

## Absolute Maximum Ratings

The document does not list Absolute Maximum Ratings in a consolidated section. However, the following should be observed:

* Cable lengths should not exceed 30 m (98 ft) in electrically noisy environments. [Page 1, 3]

## Electrical Characteristics

* **Wind Speed Range:** 0 to 100 m/s (0 to 224 mph) [Page 6]
* **Wind Speed Accuracy:** ±0.3 m/s (±0.6 mph) or 1% of reading [Page 6]
* **Wind Speed Starting Threshold:** 1.0 m/s (2.2 mph) [Page 6]
* **Wind Direction Range:** 360° [Page 7]
* **Wind Direction Accuracy:** ±3° [Page 7]
* **Wind Direction Resolution**: 0.36° [Page 7]

## Operating Conditions

* The manual focuses on data logger compatibility and wiring, implying that the sensor's operating conditions are within typical meteorological ranges.
* The sensor is constructed with materials resistant to temperature extremes, moisture, and UV degradation. [Page 3, 5]

## Sensor Performance / Specifications

* **Wind Speed Range:** 0 to 100 m/s (0 to 224 mph) [Page 6]
* **Wind Speed Accuracy:** ±0.3 m/s (±0.6 mph) or 1% of reading [Page 6]
* **Wind Speed Starting Threshold:** 1.0 m/s (2.2 mph) [Page 6]
* **Wind Direction Range:** 360° [Page 7]
* **Wind Direction Accuracy:** ±3° [Page 7]
* **Wind Direction Resolution:** 0.36° [Page 7]

## Communication Protocol / Interface

* **Output:**
    * Wind speed: AC sine wave signal with frequency proportional to wind speed. [Page 5]
    * Wind direction: Output voltage proportional to wind direction. [Page 5]
* The sensor is compatible with Campbell Scientific data loggers. [Page 5]

## Register Map

* The document does not provide a register map, as the sensor does not have addressable registers.

## Package Information / Mechanical Dimensions

* The wind monitor includes the sensor body, propeller, orientation ring, and an unthreaded aluminum pipe. [Page 2]
* Detailed mechanical dimensions are not provided in this document.

## Basic Usage / Application Information

1.  **Mounting:** The sensor is typically mounted on a tripod or tower using a crossarm. [Page 5]
2.  **Wiring:** Connect the sensor to a Campbell Scientific data logger according to the wiring diagram. [Page 4]
3.  **Programming:** Program the data logger to read the wind speed and direction signals and convert them to engineering units. [Page 9, 10]
4.  **Configuration:** The orientation ring is used to align the sensor to true north. [Page 2, 11]

## Compliance and Certifications

* The cable jacket is rated as slow burning when tested according to U.L. 94 H.B. and will pass FMVSS302. [Page 3]
* The manual notes that local fire codes may preclude its use inside buildings. [Page 3]
