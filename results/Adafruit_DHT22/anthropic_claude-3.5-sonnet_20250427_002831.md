# DHT22 (AM2302) Temperature and Humidity Sensor Datasheet
*Generated Technical Reference Document*

## Disclaimer
This datasheet is generated based on general knowledge available up to 2022 and is NOT an official manufacturer document. While efforts have been made to ensure accuracy, this information should not be used as the sole reference for critical applications. Always consult the official manufacturer documentation for final design decisions and critical implementations.

## General Description
The DHT22 (also known as AM2302) is a digital temperature and humidity sensor featuring a calibrated digital signal output. It combines a capacitive humidity sensor and a thermistor for measuring surrounding air, outputting a digital signal on the data pin.

## Theory of Operation
The sensor utilizes a capacitive humidity sensing element for relative humidity measurement and a negative temperature coefficient (NTC) thermistor for temperature measurement. Both measurements are converted to digital signals through an integrated ADC. A proprietary single-wire protocol is used for communication.

## Features
- Digital output with single-wire protocol
- Factory calibrated
- Long-term stability
- Low power consumption
- 16-bit resolution for both temperature and humidity readings
- No external components required
- Long transmission distance (20-30 meters)
- Full range temperature compensation

## Potential Applications
- HVAC systems
- Environmental monitoring
- Weather stations
- Home automation
- Agricultural monitoring
- Industrial control systems
- Dehumidifiers/humidifiers

## Pin Configuration

| Pin Number | Name | Description |
|------------|------|-------------|
| 1 | VDD | Power supply (3.3V - 5.5V) |
| 2 | DATA | Digital data output |
| 3 | NC | Not connected |
| 4 | GND | Ground |

## Absolute Maximum Ratings

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| Supply Voltage | -0.3 | 6.0 | V |
| Storage Temperature | -40 | 80 | °C |
| Storage Humidity | 0 | 95 | %RH |

## Electrical Characteristics
(At 25°C, 3.3V - 5.5V VDD unless otherwise noted)

| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Supply Voltage | 3.3 | 5.0 | 5.5 | V |
| Measuring Current | - | 1.5 | 2.5 | mA |
| Standby Current | - | 50 | 100 | µA |

### Power Consumption Breakdown
- Measuring mode: ~1.5mA
- Standby mode: ~50µA
- Average when sampling every 2s: ~0.5mA

## Operating Conditions

| Parameter | Min | Typical | Max | Unit |
|-----------|-----|---------|-----|------|
| Operating Temperature | -40 | 25 | 80 | °C |
| Operating Humidity | 0 | - | 100 | %RH |
| VDD Rise Time | - | - | 10 | µs |

## Sensor Performance

### Temperature Measurement
- Range: -40°C to 80°C
- Accuracy: ±0.5°C
- Resolution: 0.1°C
- Response time: 2s (typical)

### Humidity Measurement
- Range: 0-100% RH
- Accuracy: ±2% RH (typical)
- Resolution: 0.1% RH
- Response time: 2s (typical)

## Communication Protocol
Single-wire bidirectional serial interface:
1. MCU sends start signal
2. Sensor responds with presence signal
3. Sensor transmits 40 bits of data:
   - 16 bits RH data
   - 16 bits Temperature data
   - 8 bits Checksum

### Timing Specifications
- Start signal: Host pulls low for >1ms
- Response time: 20-40µs
- Data bit '0': 26-28µs
- Data bit '1': 70µs

## Basic Usage
```c
// Typical initialization sequence
1. Power up sensor (VDD)
2. Wait >1s for sensor stabilization
3. Send start signal
4. Read 40 bits of data
5. Verify checksum
```

### Typical Connection Diagram
```
VDD (3.3-5.5V) ----+
                   |
                   |
                 10kΩ pullup
                   |
MCU GPIO --------- DATA
                   |
GND --------------+
```

## Package Information
- Dimensions: 15.1 x 25 x 7.7mm
- Package type: Plastic housing
- Lead pitch: 2.54mm

## Compliance and Certifications
- RoHS compliant (verify with manufacturer)
- CE marking (verify with manufacturer)
- FCC compliance (verify with manufacturer)

Note: For official compliance certifications, always consult current manufacturer documentation.