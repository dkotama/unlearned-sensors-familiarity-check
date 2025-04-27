# Adafruit DHT22 Datasheet

## Disclaimer
This datasheet is generated based on general knowledge up to the last training data cut-off and is not an official manufacturer document. Accuracy cannot be guaranteed. For critical applications and final design decisions, always consult the official manufacturer datasheet.

## General Description
The Adafruit DHT22 is a temperature and humidity sensor designed for applications requiring precise environmental measurements. It utilizes a digital output to provide accurate temperature and humidity readings with minimal calibration requirements.

## Theory of Operation / Sensing Principle
The DHT22 sensor is based on a capacitive humidity sensor and a thermistor. The capacitive element measures the humidity level, while the thermistor provides temperature data. The sensor converts these analog readings to digital signals, which are then processed and transmitted via a single-wire communication protocol.

## Features
- High precision and resolution
- Low cost
- Digital signal output
- Single-wire communication protocol
- Fully calibrated
- Includes both temperature and humidity sensors

## Potential Applications
- Environmental monitoring systems
- HVAC control systems
- Weather stations
- Home automation
- Agricultural monitoring

## Pin Configuration and Description
| Pin Number | Pin Name | Pin Function    |
|------------|----------|-----------------|
| 1          | VCC      | Power supply    |
| 2          | DATA     | Data output     |
| 3          | GND      | Ground          |
| 4          | NC       | Not connected   |

## Absolute Maximum Ratings
| Parameter        | Rating      |
|------------------|-------------|
| Operating Voltage| 3.3V to 5.5V |
| Max Current      | 2.5 mA      |
| Temperature Range| -40°C to 80°C |
| Humidity Range   | 0% to 99.9% RH |

## Electrical Characteristics
### Power Supply
| Parameter        | Min | Typical | Max  |
|------------------|-----|---------|------|
| VCC              | 3.0V| 5.0V    | 5.5V |

### Power Consumption Breakdown
| Parameter        | Current Draw  |
|------------------|---------------|
| Active/Measurement | 1.0 mA (Max)    |
| Idle/Sleep        | 50 µA (Max)     |
| Communication Active | 2.0 mA (Max) |

## Operating Conditions
| Parameter        | Min  | Typical | Max   |
|------------------|------|---------|-------|
| Supply Voltage   | 3.0V | 5.0V    | 5.5V  |
| Operating Temperature | -40°C | 25°C     | 80°C   |
| Operating Humidity   | 0% RH  | 50% RH   | 99.9% RH |

## Sensor Performance / Specifications
### Temperature
| Parameter        | Specification  |
|------------------|----------------|
| Range            | -40°C to 80°C  |
| Accuracy         | ±0.5°C        |
| Resolution       | 0.1°C         |

### Humidity
| Parameter        | Specification  |
|------------------|----------------|
| Range            | 0% to 99.9% RH |
| Accuracy         | ±2% RH        |
| Resolution       | 0.1% RH       |

### General
| Parameter        | Specification  |
|------------------|----------------|
| Response Time    | 2 seconds     |
| Stability        | High          |

## Communication Protocol / Interface
The DHT22 uses a single-wire digital interface for communication. The communication protocol is asynchronous, and the timing specifications must be adhered to for accurate data retrieval.

### Timing Parameters
| Parameter        | Value       |
|------------------|------------|
| Start Signal     | 18-30 ms   |
| Acknowledge Time | 80 µs      |
| Data Transmission| 40-bit serial data   |

## Register Map
The DHT22 does not utilize a register-based configuration. Data is read directly through the single-wire communication protocol.

## Package Information / Mechanical Dimensions
The DHT22 sensor is typically available in a 4-pin single inline package (SIP).

### Mechanical Dimensions
| Dimension           | Value       |
|---------------------|-------------|
| Length              | 15.1 mm     |
| Width               | 5.7 mm      |
| Height              | 3.2 mm      |

## Basic Usage / Application Information
### Connection Diagram
1. Connect VCC to the power supply (3.3V to 5.5V).
2. Connect GND to ground.
3. Connect DATA to the microcontroller's GPIO pin.
4. Leave NC (pin 4) unconnected.

### Required External Components
- Pull-up resistor (4.7kΩ) connected between VCC and DATA.

### Pseudo-Code for Initialization and Data Reading
```python
import time
import RPi.GPIO as GPIO

# Define GPIO pin
DHT_PIN = 4

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DHT_PIN, GPIO.OUT)

def read_dht22():
    # Send start signal
    GPIO.output(DHT_PIN, GPIO.LOW)
    time.sleep(0.02)  # 20 ms
    GPIO.output(DHT_PIN, GPIO.HIGH)

    # Wait for DHT22 to pull data line low
    GPIO.setup(DHT_PIN, GPIO.IN)
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        pass

    # Read 40 bits of data
    data = []
    for _ in range(40):
        while GPIO.input(DHT_PIN) == GPIO.LOW:
            pass
        start_time = time.time()
        while GPIO.input(DHT_PIN) == GPIO.HIGH:
            pass
        end_time = time.time()
        data.append(1 if (end_time - start_time) > 0.00003 else 0)

    # Convert data to integers
    humidity = data[0:16]
    temperature = data[16:32]
    checksum = data[32:40]

    humidity_value = sum([bit * (2**i) for i, bit in enumerate(reversed(humidity))]) / 10.0
    temperature_value = sum([bit * (2**i) for i, bit in enumerate(reversed(temperature))]) / 10.0

    return humidity_value, temperature_value

# Read sensor data
humidity, temperature = read_dht22()
print(f"Humidity: {humidity} %RH")
print(f"Temperature: {temperature} °C")

# Cleanup GPIO
GPIO.cleanup()
```

## Compliance and Certifications
The Adafruit DHT22 sensor typically complies with standards like RoHS, CE, and FCC. Specific compliance should be verified with the manufacturer.

---

Always refer to the official Adafruit DHT22 datasheet for the most accurate and up-to-date information.