# Decagon 10HS Soil Moisture Sensor

This document provides an overview of the Decagon 10HS Soil Moisture Sensor, based on information from the provided PDF datasheet.

## Manufacturer Info

* **Manufacturer:** Decagon (Sensor is sold by ICT International) [Page 1]
* **Model Name/Number:** 10HS [Page 1]
* **Website:** www.ictinternational.com [Page 3]

## General Description

The Decagon 10HS is a soil moisture sensor used to measure the volumetric water content (VWC) of soils and other materials. It is designed for scientific research and agricultural applications. The sensor uses capacitance technology to measure the dielectric constant of the soil, which is then used to determine VWC. [Page 1]

## Theory of Operation / Sensing Principle

The 10HS measures volumetric water content by determining the dielectric constant of the soil. It uses a 70 MHz frequency, which minimizes salinity and textural effects on the measurement. The sensor outputs a voltage proportional to the water content. [Page 1]

## Features

* High resolution for daily or hourly tracking of water use. [Page 1]
* Voltage output proportional to water content. [Page 1]
* Low cost. [Page 1]
* Low sensitivity to salt and temperature. [Page 1]
* Very low power requirement. [Page 1, 3]
* Large volume of influence (1 liter) [Page 1]
* Accurate in most soils. [Page 1]
* Compatible with Campbell Scientific data loggers. [Page 1]

## Potential Applications

* Irrigation scheduling [Page 1]
* Vadose zone monitoring [Page 1]
* Plant-soil-water interaction studies [Page 1]
* Scientific research [Page 1]
* Agricultural applications [Page 1]

## Pin Configuration and Description

The document states that the 10HS has an analog signal output, enabling integration with systems from other manufacturers, such as Campbell Scientific. [Page 1] However, the specific pin configuration is not detailed in this document. The sensor has a 3.5 mm stereo plug or stripped and tinned lead wires. [Page 3]

## Absolute Maximum Ratings

The document does not provide a section on absolute maximum ratings. However, the power requirements section indicates that the sensor can handle a voltage range of 3 VDC to 15 VDC. [Page 3]

## Electrical Characteristics

* **Power Requirements:** 3 VDC @ 12 mA to 15 VDC @ 15 mA [Page 3]
* **Output:** 300 mV (dry soil) to 1250 mV (saturated soil), independent of excitation voltage [Page 3]
* **Frequency:** 70 MHz [Page 3]

## Operating Conditions

* **Operating Temperature:** 0 to 50°C [Page 3]

## Sensor Performance / Specifications

* **Volumetric Water Content (VWC) Range:** 0 to 0.57 m³/m³ (0-57%) [Page 3]
* **VWC Accuracy:**
    * ±0.05 m³/m³ (±5% VWC) typical in mineral soils using standard calibration. [Page 3]
    * ±0.02 m³/m³ (±2% VWC) using soil-specific calibration. [Page 3]
* **VWC Resolution:** 0.0008 m³/m³ (0.08% VWC) in mineral soils from 0 to 0.50 m³/m³ (0-50% VWC) [Page 3]
* **Apparent Dielectric Permittivity (εa) Range:** 1 (air) to 50 [Page 3]
* **εa Accuracy:**
    * ±0.5 from εa of 2 to 10
    * ±2.5 from εa of 10 to 50 [Page 3]
* **εa Resolution:**
    * 0.1 from εa of 1 to 30
    * 0.2 from εa of 30 to 50 [Page 3]
* **Measurement Time:** 10 ms [Page 3]

## Communication Protocol / Interface

* **Output:** Analog voltage [Page 1]

## Register Map

The document does not provide a register map, as the sensor provides an analog voltage output.

## Package Information / Mechanical Dimensions

* **Dimensions:** 14.5 cm x 3.3 cm x 0.7 cm [Page 3]
* **Cable Length:** 5 m standard [Page 3]
* **Connector Type:** 3.5 mm stereo plug or stripped and tinned lead wires [Page 3]

## Basic Usage / Application Information

The 10HS sensor is inserted into the soil, and its analog voltage output is read by a data logger or other measurement device. The voltage output is then converted to volumetric water content using a calibration equation. The document mentions compatibility with Campbell Scientific data loggers and the use of the Topp equation for converting dielectric permittivity to VWC. [Page 1]

## Compliance and Certifications

The datasheet does not contain compliance and certifications information.
