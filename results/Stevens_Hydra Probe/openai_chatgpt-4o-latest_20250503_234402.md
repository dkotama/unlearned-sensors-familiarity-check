```markdown
# Stevens Hydra Probe Datasheet (Unofficial)

---

## Disclaimer

This datasheet has been generated based on publicly available information and general technical knowledge up to the 2024 knowledge cut-off date. It has not been authored or endorsed by Stevens Water Monitoring Systems, Inc. and should not be treated as an official manufacturer document. All specifications, parameters, and electrical details presented herein are indicative and provided for informational purposes only. For critical applications, precise electrical designs, and guaranteed operational performance, always refer to the official datasheet and documentation provided by the sensor manufacturer.

---

## General Description

The Stevens Hydra Probe is a high-precision soil sensor designed to measure key soil parameters including volumetric water content (VWC), soil temperature, electrical conductivity (EC), and dielectric permittivity. It is widely used in environmental monitoring, precision agriculture, hydrology research, and climate studies.

The sensor supports digital communication and provides highly accurate and repeatable measurements. The rugged, field-proven design allows for long-term deployment in a variety of harsh outdoor conditions.

---

## Theory of Operation / Sensing Principle

The Hydra Probe employs a coaxial impedance reflectometry technique operating at a fixed frequency (typically around 50 MHz). This technique involves sending an electromagnetic signal into the soil and analyzing its interaction with the soil's dielectric medium.

Soil volumetric water content is derived from the real component of the complex dielectric permittivity. Salinity (EC) and temperature-compensated effects are derived from the imaginary component and temperature readings respectively. This frequency-domain sensing technique allows for better performance in saline and varied soil types when compared to time-domain or resistive sensors.

---

## Features

- Simultaneous measurement of:
  - Volumetric Water Content (VWC)
  - Soil Temperature
  - Electrical Conductivity (EC)
  - Real and Imaginary Dielectric Permittivity
- High accuracy and stability across soil types and moisture levels
- Embedded digital output (SDI-12 or RS-485, depending on model)
- Robust epoxy-sealed stainless steel construction
- Factory-calibrated for mineral soils
- Fully potted for long-term field reliability
- Models compatible with Campbell Scientific, Stevens/SDI-12, or MODBUS systems

---

## Potential Applications

- Precision agriculture and irrigation optimization
- Hydrological and watershed modeling
- Environmental monitoring stations
- Remote weather and soil stations
- Academic and industrial soil research
- Landfill and stormwater leachate monitoring

---

## Pin Configuration and Description

| Wire Color | Pin Number | Signal              | Function Description                    |
|------------|-------------|---------------------|------------------------------------------|
| Red        | 1           | V+ / Power In       | Supply voltage input (9–20 VDC)          |
| Black      | 2           | Ground              | Power and signal ground                  |
| White      | 3           | SDI-12 / RS-485     | Digital communication line (depends on model) |
| Green      | 4           | Data Out / TX (modbus) | Optional - Dependent on configuration     |
| Yellow     | -           | Shield (if present) | Cable shielding for EMI protection       |

Note: Specific wire colors may vary depending on the model and cable configuration. Always refer to model-specific wiring guide.

---

## Absolute Maximum Ratings

| Parameter               | Rating                      |
|------------------------|-----------------------------|
| Supply Voltage          | -0.3 V to 24 VDC            |
| Operating Temperature   | -40°C to +60°C              |
| Storage Temperature     | -40°C to +85°C              |
| Max Input Current       | 150 mA                      |
| ESD Susceptibility      | ±4 kV (contact)             |

Exceeding these ratings may cause permanent damage to the device.

---

## Electrical Characteristics

| Parameter                      | Typical Value     | Notes                                           |
|-------------------------------|-------------------|-------------------------------------------------|
| Supply Voltage                 | 9 V to 20 V DC     | Recommended nominal: 12 V DC                   |
| Input Current (Measurement)   | 10–14 mA           | Active measurement mode                        |
| Input Current (Idle)          | ≤ 0.3 mA           | Quiescent when idle in sleep mode (SDI-12)     |
| Warm-up Time                  | 1 second typ.      | Time from power-up to readiness                 |
| Measurement Time              | < 1 second         | For full sensor read                            |
| SDI-12 Protocol Level         | CMOS logic         | Uses standard SDI-12 signal levels              |

### Power Consumption Breakdown

| Mode             | Current Draw | Duration        | Notes                               |
|------------------|--------------|------------------|-------------------------------------|
| Idle/Sleep       | < 0.3 mA     | Continuous       | Very low power mode (SDI-12)        |
| Active Measure   | 10–14 mA     | < 1 sec per poll | During measurement cycle            |
| RS-485 Comm      | 10–15 mA     | During transmit  | Varies with transmission frequency  |

---

## Operating Conditions

| Parameter                     | Minimum   | Typical | Maximum   | Units     |
|------------------------------|-----------|---------|-----------|-----------|
| Operating Temperature         | -40       |         | +60       | °C        |
| Soil Temperature Range        | -40       |         | +60       | °C        |
| Humidity (non-condensing)     | 0         |         | 100       | % RH      |
| Ingress Protection (IP)       | IP68      |         |           | Submersible (fully potted) |

---

## Sensor Performance / Specifications

| Parameter                        | Typical Value            | Notes                                      |
|---------------------------------|---------------------------|--------------------------------------------|
| Volumetric Water Content Range   | 0 – 0.5 m³/m³ or higher   | May vary based on soil conditions          |
| Water Content Accuracy           | ±0.01–0.03 m³/m³          | Better in calibrated soils                 |
| Electrical Conductivity (EC)     | 0 – 10 dS/m               | Solution EC                                |
| EC Accuracy                      | ± 5%                      | In temperature-compensated mode            |
| Dielectric Permittivity (Real)   | 1–80                      |                        |
| Soil Temperature Accuracy        | ±0.1 °C                   | Over full range                            |
| Response Time                    | <1 second                 | Per measurement                            |
| Long-term Drift                  | Negligible                | Over 1 year                                |

Note: Sensor precision and accuracy can depend on calibration, depth, and soil texture.

---

## Communication Protocol / Interface

Hydra Probe sensors are typically available in two versions:

- SDI-12 (standard sensor protocol for environmental monitoring)
- RS-485 with MODBUS RTU protocol (industrial usage)

### SDI-12 Details:

- Voltage levels: CMOS compatible
- Baud rate: 1200 bps (fixed)
- Compatible with multiple devices on one bus
- Supports standard SDI-12 commands for measurement and identification

### MODBUS Details:

- RS-485 differential signaling
- Standard MODBUS RTU protocol
- 9600/19200 bps typical
- Holding registers contain measurement results
- Address configurable per device

For complete protocol reference, consult Hydra Probe SDI-12 or MODBUS implementation guides.

---

## Register Map (MODBUS Models)

| Register Address | Parameter                     | Format        | Units           |
|------------------|-------------------------------|---------------|-----------------|
| 0x0000           | Real Dielectric Permittivity  | Float32       | Unitless        |
| 0x0002           | Imaginary Dielectric Permittivity | Float32   | Unitless        |
| 0x0004           | Volumetric Water Content       | Float32       | m³/m³           |
| 0x0006           | EC (Salinity)                  | Float32       | dS/m            |
| 0x0008           | Soil Temperature               | Float32       | °C              |

Note: Addresses and parameter mappings may vary between firmware versions.

---

## Package Information / Mechanical Dimensions

Typical sensor probe includes:

- 4 stainless steel tines (pins) for soil insertion
- Epoxy-sealed electronics
- Weather-resistant cable pigtail (typically 4–10 meters standard)

| Dimension          | Value             |
|--------------------|------------------|
| Length             | 17.8 cm (7 in)   |
| Width              | 4.4 cm (1.75 in) |
| Tine Length        | ~6.4 cm (2.5 in) |
| Cable Exit         | Top (potted)     |
| Weight             | ~500 g           |

---

## Basic Usage / Application Information

### Example Connection Diagram (SDI-12)

```text
   [SDI-12 Logger or Data Acquisition Device]
             |
     --------------------
    |      |      |      |
  V+     GND  Data   Shield (optional)
   |       |     |
  Red   Black  White
         |
    [Hydra Probe]
```

### Application Notes

1. Install tines fully in contact with soil, avoiding air pockets.
2. Use consistent orientation and depth for multiple sensors.
3. Use dielectric grease or sealant for cable connections in field.
4. Regularly verify data integrity via logger output.

### Example SDI-12 Command Usage

```text
Command Sent: 0M!
(Device measurement command, where 0 is sensor address)

Response: 00013
(Indicates data is ready in 13 seconds)

Command Sent: 0D0!
(Device data read command)

Response: +0.276+23.5+1.23+15.4...
(VWC, Temp, EC, etc.)
```

---

## Compliance and Certifications

The Stevens Hydra Probe is known to be compliant with typical environmental and industrial standards; however, users should verify certification on a per-device basis.

- RoHS Compliant
- CE Marked
- FCC Part 15 Class A (digital emission limits)
- Water resistance: IP68

Always check directly with Stevens Water Monitoring Systems for the most up-to-date certifications and declarations of conformity.

---
```