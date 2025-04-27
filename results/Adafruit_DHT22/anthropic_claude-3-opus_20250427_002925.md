# Adafruit DHT22 Temperature and Humidity Sensor Datasheet

**Disclaimer:** This datasheet is generated based on general knowledge up to my last training data cut-off (September 2021), and is not an official manufacturer document. Accuracy cannot be guaranteed. Always consult the official manufacturer datasheet for critical applications and final design decisions.

## General Description

The Adafruit DHT22 is a low-cost, digital temperature and humidity sensor. It uses a capacitive humidity sensor and a thermistor to measure the surrounding air, and outputs a digital signal on the data pin.

## Theory of Operation / Sensing Principle

The DHT22 uses a capacitive humidity sensor and a negative temperature coefficient (NTC) thermistor. The capacitive humidity sensor has two electrodes with a moisture-holding substrate between them. As humidity varies, the substrate's conductivity changes, altering the capacitance. The NTC thermistor exhibits a decrease in resistance with an increase in temperature. The sensor's microcontroller measures these changes and calculates the relative humidity and temperature.

## Features

- Relative humidity and temperature measurement
- Low power consumption
- 3 to 5V power and I/O
- Good for 0-100% humidity readings with 2-5% accuracy
- Good for -40 to 80°C temperature readings ±0.5°C accuracy

## Potential Applications

- Environmental monitoring
- Weather stations
- HVAC systems
- Automatic climate control

## Pin Configuration and Description

The DHT22 has four pins:

1. VCC: Power supply (3.3V to 5V)
2. Data: Serial data output
3. NC: Not connected
4. GND: Ground

## Absolute Maximum Ratings

| Parameter            | Min  | Typ  | Max  | Unit |
|---------------------|------|------|------|------|
| Supply Voltage (VCC) | -0.3 |      | 6.0  | V    |
| Storage Temperature  | -40  |      | 80   | °C   |

## Electrical Characteristics

| Parameter                      | Min  | Typ  | Max  | Unit |
|-------------------------------|------|------|------|------|
| Supply Voltage (VCC)           | 3.3  | 5.0  | 6.0  | V    |
| Measuring Current Supply (IDD) | 1.0  | 1.5  | 2.0  | mA   |
| Average Current Supply (IDD)   | 0.7  | 1.0  | 1.5  | mA   |
| Data Output Voltage (Logic 0)  | 0    |      | 0.3  | V    |
| Data Output Voltage (Logic 1)  | 3.0  |      | VCC  | V    |

### Power Consumption Breakdown

- Measuring: 1.5 mA
- Idle: 40-50 µA

## Operating Conditions

| Parameter                     | Min | Typ | Max | Unit |
|------------------------------|-----|-----|-----|------|
| Operating Temperature (T_OP) | -40 |     | 80  | °C   |
| Operating Humidity           | 0   |     | 100 | %RH  |

## Sensor Performance / Specifications

| Parameter                        | Condition    | Min | Typ | Max | Unit  |
|---------------------------------|--------------|-----|-----|-----|-------|
| Humidity Measuring Range         |              | 0   |     | 100 | %RH   |
| Humidity Accuracy                | 25°C, 20-80% |     | ±2  | ±5  | %RH   |
| Temperature Measuring Range      |              | -40 |     | 80  | °C    |
| Temperature Accuracy             | 25°C         |     | ±0.2| ±0.5| °C    |
| Resolution                       |              |     | 0.1 |     | %RH/°C|
| Response Time (Humidity)         | 1/e (63%)    |     | 10  |     | s     |
| Long-term Stability (Humidity)   |              |     | ±1  |     | %RH/yr|

## Communication Protocol / Interface

The DHT22 uses a proprietary 1-wire protocol for communication:

1. The microcontroller pulls the data line low for at least 1ms to request data.
2. The DHT22 responds by pulling the line low for 80µs, followed by a high for 80µs.
3. The DHT22 then sends 40 bits of data, high bit first, with each bit encoded as:
   - Logic 0: 50µs low followed by 26-28µs high
   - Logic 1: 50µs low followed by 70µs high

Data consists of 16 bits of relative humidity data, 16 bits of temperature data, and an 8-bit checksum.

## Package Information / Mechanical Dimensions

The DHT22 comes in a 4-pin single row package with 0.1" (2.54mm) header spacing. Dimensions are approximately:

- Width: 15.5mm
- Height: 12mm
- Depth: 5.5mm

## Basic Usage / Application Information

1. Connect VCC to a 3.3-5V power supply, GND to ground, and the data pin to a microcontroller GPIO.
2. Pull the data pin low for >1ms to start communication.
3. Read the 40-bit data stream from the sensor.
4. Convert the received data:
   - Humidity = Humidity_High * 256 + Humidity_Low
   - Temperature = Temperature_High * 256 + Temperature_Low
   - If Temperature_High's MSB is 1, it's a negative value, subtract 2^16.
5. Verify the checksum: Checksum should equal the last 8 bits of the sum of Humidity_High, Humidity_Low, Temperature_High, and Temperature_Low.

## Compliance and Certifications

The DHT22 is expected to be compliant with common standards such as RoHS, CE, and FCC. However, specific compliance should be verified with the manufacturer.