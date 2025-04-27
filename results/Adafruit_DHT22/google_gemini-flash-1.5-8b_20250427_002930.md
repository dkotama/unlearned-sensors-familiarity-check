# Adafruit DHT22 Sensor Datasheet

**Disclaimer:** This datasheet is generated from general knowledge up to the last training data cut-off.  It is not an official manufacturer document and accuracy is not guaranteed. For critical applications and final design decisions, consult the official Adafruit DHT22 datasheet from the manufacturer.


**General Description:**

The DHT22 is a digital temperature and humidity sensor that provides both temperature and relative humidity measurements. It is a common, relatively inexpensive sensor available in various form factors.


**Theory of Operation / Sensing Principle:**

The sensor utilizes a capacitive sensing technique for measuring changes in humidity and temperature.  These changes in capacitance, correlated with known values, allow for a calculation of humidity and temperature.


**Features:**

*   Digital output for ease of interfacing
*   Measures both temperature and humidity
*   High precision and accuracy relative to competitor sensors.
*   Compact and convenient form factor


**Potential Applications:**

*   Environmental monitoring systems
*   Home automation and smart home devices
*   Agricultural applications for monitoring environmental conditions
*   Industrial process control


**Pin Configuration and Description:**

| Pin Number | Pin Name | Description |
|---|---|---|
| 1 | VCC | Power supply (3.3V or 5V) |
| 2 | DATA | Digital output pin; carries the data transmitted by the sensor. |
| 3 | GND | Ground |


**Absolute Maximum Ratings:**

| Parameter           | Value       | Unit    |
|----------------------|-------------|----------|
| Supply voltage (VCC) | 5.5         | Volts   |
| Operating temperature | -40 to 85 | °C      |


**Electrical Characteristics:**

*   **Supply Voltage (VDD):** 3.3V to 5.5V DC
*   **Output Mode:** Digital, typically a 800us pulse to signal data ready + 40us to signal response (check datasheet for details).

**Power Consumption Breakdown:**

*   **Active/Measurement:** Unknown. Detail needs information from the datasheet.
*   **Idle/Sleep:** Unknown. Detail needs information from the datasheet.
*   **Communication Active:** Unknown.  Detail needs information from the datasheet.


**Operating Conditions:**

*   **Supply Voltage:** 3.3V or 5V
*   **Operating Temperature:** -40°C to +85°C
*   **Humidity:** 0% to 100% RH


**Sensor Performance / Specifications:**

| Parameter             | Value        | Unit      |
|------------------------|---------------|------------|
| Temperature Accuracy   | +/- 0.5°C     | °C        |
| Humidity Accuracy      | +/- 2%        | %RH       |
| Temperature Range    | -40°C to +80°C| °C        |
| Relative Humidity Range| 0% to 100% RH | %RH       |
| Resolution          |  0.1°C      | °C        |
| Resolution (Humidity) | 0.1%RH     | %RH       |
| Response Time         | ≈ 0.5 seconds  | sec        |




**Communication Protocol / Interface:**

The DHT22 sensor uses a single-wire, or I2C-like digital output protocol.


**Register Map:**

This sensor does not have a conventional register map in the sense that an I2C device would. It signals data ready via a pulse.


**Package Information / Mechanical Dimensions:**

Details on package types and dimensions are unavailable without access to a more complete datasheet.


**Basic Usage / Application Information:**

*   **Connection Diagram:** A simple connection to a microcontroller (such as Arduino) is common.
*   **External Components:** A pull-up resistor might be needed on the data line depending on the microcontroller.
*   **Initialization:**  The sensor needs to stabilize prior to sampling.  Various libraries/interfacing methods deal with this.
*   **Data Reading:**  A delay is followed by reading the data bits transmitted by the sensor.

```C++
//Pseudo-code (example)
// ... include necessary headers ...

// Initialize I/O pins (e.g. digital pin 2 for data)

//Wait a predetermined period of time (e.g., 1s) for sensor to stabilize.


//Read data from the sensor, likely using a function in library

//Parse/decode the received data to temperature and humidity values.

// ... further processing ...
```

**Compliance and Certifications:**

Typical certifications (RoHS, CE, FCC) are often applicable, contact the manufacturer for specifics.
