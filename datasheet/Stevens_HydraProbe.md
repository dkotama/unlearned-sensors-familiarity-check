# Stevens HydraProbe Soil Sensor Datasheet

## Manufacturer Info
*   **Manufacturer:** Stevens Water Monitoring Systems, Inc.
*   **Sensor Model Name:** HydraProbe Soil Sensor
*   **Production Date:** The provided manual is dated January 2018, Rev. VI, Firmware version 2.9. The sensor has been available for over 25 years.
*   **Manufacturer's Website:** www.stevenswater.com
*   **Address:** 12067 NE Glenn Widing Dr. #106, Portland, Oregon 97220 USA [213, page 3 bottom, page 6 bottom]

## General Description
The Stevens HydraProbe is a **rugged soil sensor** designed to measure the **three most significant soil parameters: moisture, electrical conductivity, and temperature**. It also measures the **complex dielectric permittivity** of the soil. The HydraProbe is described as the **most scientifically researched soil sensor** available, having been used by organizations like the USDA, NOAA, farmers, leading irrigation companies, and universities for over 25 years. Engineered to handle various terrains, it provides reliable data year after year. It is known for its **continuous long-term data without calibration drift** and **consistent research-grade accuracy**.

## Theory of Operation / Sensing Principle
The HydraProbe measures soil properties based on the physics and behavior of a **reflected electromagnetic radio wave** within the soil. It operates at a frequency of **50 MHz**. The sensor is specifically characterized as a **Ratiometric Coaxial Impedance Dielectric Reflectometer**. It works by calculating the **ratio of the amplitudes of reflected radio waves** using a coaxial wave guide formed by its tines.

From the reflected signal, the sensor first calculates the **complex impedance** of the soil using a numerical solution to Maxwell's equations. The **complex dielectric permittivity** (K*) is then determined from this impedance. This complex value has both **real (εr)** and **imaginary (εi)** components.

1.  **Soil Moisture:** The **real dielectric permittivity (εr)** is the primary indicator of soil water content. Water has a significantly higher dielectric constant (around 78.54 at 25°C) than dry soil (typically 4-5). When exposed to the oscillating electric field from the radio wave, polar water molecules reorient, causing changes in εr that directly correlate to soil moisture levels. The HydraProbe's soil moisture calibration is based on the real dielectric permittivity. By separating the real component from the imaginary component, the HydraProbe's moisture measurements are **less affected by factors like soil salinity, temperature, soil variability, and inter-sensor variability** compared to sensors that rely on apparent permittivity (a combination of real and imaginary parts). The soil moisture value is calculated from a mathematical equation that includes the real dielectric permittivity.
2.  **Electrical Conductivity (EC):** The **imaginary dielectric permittivity (εi)** is related to energy loss within the soil matrix. In most soils, especially sandy or silty types where molecular relaxations are minimal, the imaginary component provides a good estimation of electrical conductivity (EC). The HydraProbe calculates EC by measuring the imaginary permittivity, assuming negligible molecular relaxations. It measures **bulk electrical conductivity** (σb), which is the EC of the entire soil/water/air matrix. This EC is primarily influenced by dissolved salts in the soil water. The sensor provides a temperature correction for EC, as EC is sensitive to temperature.
3.  **Temperature:** The sensor also measures soil temperature. Both real and imaginary dielectric permittivities are affected by temperature. The imaginary component is significantly more sensitive to temperature changes than the real component. Although the sensor has internal temperature corrections for its electronics, the standard factory soil moisture calibrations do not apply a temperature correction to the measured moisture values. This is because the temperature dependency of water's dielectric properties in soil is complex and varies depending on the specific soil type.

## Features
*   Measures soil moisture (water fraction by volume), bulk electrical conductivity (temperature corrected and uncorrected), soil temperature (Celsius and Fahrenheit), and complex dielectric permittivity (real and imaginary, temperature corrected and uncorrected).
*   **Patented technology**.
*   Operates using a **ratiometric coaxial impedance dielectric reflectometer** at 50 MHz.
*   **High accuracy and precision**:
    *   Temperature: ± 0.3°C (-30° to 60°C).
    *   Soil Moisture: ± 0.01 to 0.03 wfv (typical, soil dependent). Precision: ± 0.001 wfv.
    *   Bulk Electrical Conductivity: ± 0.0014 S/m or ± 1% (typical, uncorrected), ± 0.0014 S/m or ± 5% (typical, corrected).
    *   Real/Imaginary Dielectric Constant: ± 0.1 to 0.2 or ± 1% FS.
*   **Low inter-sensor variability**.
*   Rugged construction: Marine grade stainless steel tines, ABS housing, internal electronics permanently potted with epoxy resin.
*   Designed for **long-term burial** and many sensors installed over a decade ago are still in service.
*   **Fully potted electronics** are submersible.
*   Durable, direct burial cable.
*   **Reliable and stable** with zero maintenance required.
*   Less sensitive to temperature, soil type, and mineralogy effects on soil moisture measurements compared to sensors using apparent permittivity.
*   Soil moisture calibration based on **real dielectric permittivity**, which is less affected by salinity and temperature.
*   EC calculation based on **imaginary dielectric permittivity**, assuming negligible molecular relaxations.
*   Can measure dielectric constant accurately even in soils with EC up to 1.5 S/m.
*   Easy to install and use; calibration is not necessary for most soils, with default settings suitable for many applications.
*   Available in **SDI-12, RS-485, and analog** configurations. All versions provide the same measurements and accuracy.
*   SDI-12 version has low power consumption (<1 mA idle, 10 mA active). RS-485 version can have longer cable lengths (up to 1219m) but draws more power (<10 mA idle, 30 mA active).
*   Has three built-in factory soil moisture calibrations (GENERAL, Organic, Rockwool) and supports custom calibrations.
*   Can be used to **determine if soil is frozen**.

## Potential Applications
The HydraProbe is a versatile sensor trusted in various fields, including:
*   Agriculture and Irrigation
*   Viticulture and Sports Turf
*   General Research and Soil Phytoremediation
*   Water Shed Modeling and Evapotranspiration Studies
*   Land Reclamation and Land Slide Studies
*   Studies of Shrink/Swell Clays
*   Flood Forecasting
*   Satellite Ground Truthing and Wetland Delineation
*   Predicting Weather and Precision Agriculture
*   Used by major networks like the USDA Soil Climate Analysis Network (SCAN), the Bureau of Reclamation's Agrimet Network, and NOAA.
*   Optimizing irrigation systems to prevent runoff, conserve water, and reduce pumping costs.
*   Studying microclimates or small hydrological anomalies.
*   Monitoring the root zone depth for agricultural crops, often with multiple sensors at different depths.
*   Studying distinct soil horizons for soil scientists and groundwater hydrologists.
*   Assessing soil salinity via electrical conductivity measurements.
*   Monitoring soil moisture during freezing and thawing cycles.

## Pin Configuration and Description
The Stevens HydraProbe sensor is available in different configurations: SDI-12, RS-485, and analog, each with a specific pin configuration [1, 2]. The cable contains power, ground, and data wires soldered to the internal electronics [3].

*   **SDI-12 Version:** Uses a 3-wire cable [1].
    *   **Red Wire:** +Volts Power Input [4, 5] (Typically 9-20 VDC, 12VDC Ideal) [5, 6].
    *   **Black Wire:** Ground [4, 5].
    *   **Blue Wire:** SDI-12 Data Signal [4, 5].

*   **RS-485 Version:** Uses a 4-wire cable [1, 7].
    *   **Red Wire:** +Volts Power Input [6, 8] (Typically 9-20 VDC, 12VDC Ideal) [6, 8].
    *   **Black Wire:** Ground [6, 8].
    *   **Green Wire:** Data Signal A (inverting signal (-)) [6, 8].
    *   **White Wire:** Data Signal B (non-inverting signal (+)) [6, 8].

*   **Analog Version:** Uses a 7-conductor cable [1]. Requires an attached instrument to measure voltages [9]. Specific wire functions are not detailed in the provided sources beyond it carrying power, ground, and data wires [3].

The sensor performs a measurement duty cycle of 2 seconds [4, 6].

## Absolute Maximum Ratings
While a comprehensive list of absolute maximum stress ratings is not explicitly provided as a single table, the sources include several precautions and limits:

*   **Extreme Heat:** Do not subject the probe to **extreme heat over 70 degrees Celsius (160 degrees Fahrenheit)** [10]. The Storage Temperature Range is specified as **-40 to 75°C** [11].
*   **Fluids:** Do not subject the probe to **fluids with a pH less than 4** [10].
*   **Chemicals:** Do not subject the probe to **strong oxidizers** like bleach, or **strong reducing agents** [10]. Do not subject the probe to **polar solvents** such as acetone or **chlorinated solvents** such as dichloromethane [10].
*   **Magnetic Fields:** Do not subject the probe to **strong magnetic fields** [10].
*   **Mechanical Stress:** Do not use **excessive force** to drive the probe into the soil as the tines could bend [10]. If difficulty is encountered due to rocks, relocate the probe [10]. Do not remove the HydraProbe from the soil by **pulling on the cable** [12]. Avoid **foot traffic and vehicular traffic** in the vicinity of the probes after installation to prevent compaction and dislodging [13].
*   **Electrical:** Avoid placing more than one probe in a bucket of wet sand while logging data; this may create an **electrolysis effect that may damage the probe** [14]. Lightning strikes will cause damage or failure; surge protection and/or base station grounding is recommended in lightning-prone areas [13].

## Electrical Characteristics
The sensor operates within a specified power range and has different power consumption profiles depending on the configuration and state.

*   **Power Requirements:**
    *   Nominal/Operational Voltage: **9 to 20 VDC** (12VDC Ideal) [6, 8]. Source [11] lists the requirement as 7 to 20 VDC (12 VDC typical).
    *   Recommended Connection: Connect the red wire to a +12 volt DC power supply and the black wire to ground for all models [4].

*   **Power Consumption Breakdown:**
    *   SDI-12 Version:
        *   **Idle:** **<1 mA** [1, 5, 6].
        *   **Active/Measurement:** **10 mA for 2 seconds** [1, 5, 6].
    *   RS-485 Version:
        *   **Idle:** **<10 mA** [1, 6, 8].
        *   **Active/Measurement:** **30 mA Active for 2 seconds** [1, 6, 8].

## Operating Conditions
The HydraProbe is designed for long-term burial and operation in various environmental conditions.

*   **Operational Temperature Range:** **-10 to +60°C** [1]. Source [11] also lists -10 to 65°C as the standard range. Extended temperature range models are available [15, 16]. Avoid extreme heat over 70°C [10].
*   **Storage Temperature Range:** **-40 to +65°C** [1]. Source [11] lists -40 to 75°C.
*   **Humidity/Water Resistance:** **Tolerates continuous full immersion** [1]. The fully potted electronics are submersible [17].
*   **Soil Conditions:** Designed to measure in various terrains [18]. Installation is critical for accurate data, requiring undisturbed soil in the sensing volume [19, 20]. Factors like shrink/swell clays, rocks, pebbles, and bioturbation can affect measurements [21-24]. Salinity can influence measurements, particularly EC, but the sensor performs relatively well in salt-affected soils [25, 26]. The sensor can also indicate if soil is frozen [27].
*   **Cable:** The cable is a **direct burial cable** [17]. While durable, it is susceptible to abrasion and cuts; use caution during excavation [12].

## Sensor Performance / Specifications
The HydraProbe provides research-grade accuracy and precision for its measurements [17, 28].

| Parameter                         | Accuracy / Precision                                    | Range                 | Resolution      |
| :-------------------------------- | :------------------------------------------------------ | :-------------------- | :-------------- |
| Temperature (C)                   | ± 0.3°C (From -30° to 60°C) [3]                        | -10 to +60°C [1]      | 0.1°C [1]       |
| Soil Moisture wfv (m³ m⁻³)        | ± 0.01 to 0.03 wfv (Typical, soil dependent) [1, 3]    | 0 to 1 WFV (0 to 100% | 0.001 wfv [1]   |
| Soil Moisture wfv (m³ m⁻³)        | ± 0.001 wfv Precision [1, 3]                           | Full Saturation) [1]  |                 |
| Bulk Electrical Conductivity (TUC) | ± 0.0014 S/m or ± 1% (Typical) [1, 29]                  | 0 to 1.5 S/m [1, 25]  | 0.001 S/m [1]   |
| Bulk Electrical Conductivity (TC)  | ± 0.0014 S/m or ± 5% (Typical) [1, 29]                  | 0 to 1.5 S/m [1, 25]  |                 |
| Real Dielectric Permittivity      | ± 0.1 to 0.2 or ± 1% FS [1, 29]                         | 1 to 80 (Water = 78.54 at 25°C) [1, 30] | 0.001 [1]       |
| Imaginary Dielectric Permittivity | ± 0.1 to 0.2 or ± 1% FS [1, 29]                         | 0 to 1.5 S/m [26]     | 0.001 [1]       |
| Inter-sensor variability          | ± 0.012 WFV (0 m³ m⁻³) [1]                              |                       |                 |

*   **Stability:** Designed for **continuous long-term data without calibration drift** [17]. Many sensors installed over a decade ago are still in service [17, 28]. Known for **consistent research-grade accuracy year after year** [17]. Zero maintenance required [17].
*   **Response Time:** The measurement duty cycle is 2 seconds [4, 6], which includes warm-up time, signal processing, and mathematical operations [31].

## Communication Protocol / Interface
The HydraProbe offers three communication interfaces: SDI-12, RS-485, and Analog [1, 2]. All versions provide the same measurements and accuracy [9].

*   **SDI-12:**
    *   Protocol: **SDI-12 Standard Version 1.2** compliant serial data interface [1, 32, 33].
    *   Baud Rate: **1200** [1, 32].
    *   Addressing: Serial; allows multiple sensors to be connected via a single cable [1, 32]. Default address is "0" [32]. Address is the first character of any command or response [34].
    *   Commands: Uses standard and extended SDI-12 commands (e.g., aI!, aAb!, aM!, aC!, aD0!, aD1!, aD2!, aXS!, aXM!, aXY!) [5, 35-40]. Data is in printable ASCII characters [34].
    *   Power: Low power consumption compared to RS-485 [1, 6].

*   **RS-485:**
    *   Protocol: RS-485 serial communication [1, 7].
    *   Baud Rate: **9600** [1, 8, 41].
    *   Settings: 8 Data bits, No Parity, 1 Stop bit, No Flow control [41].
    *   Addressing: 3-byte address (0-9, A-Z, a-z), Wildcard "/" and Broadcast "///" supported [42].
    *   Commands: Command format is AAACC<CR><LF> [42]. Commands include TR, T<set>, SN=?, FV=?, AD=?, LO=?, DS=?, PE=? [43, 43-46]. Send line ends with Carriage Return + Line Feed (<CR><LF>) [42, 47].
    *   Power: Draws more power than SDI-12 [7].
    *   Cable Length: Can use longer cable lengths, over 3000 feet (1219m) [1, 7].

*   **Analog:**
    *   Protocol: Transmits data as voltages [9].
    *   Requires external instrument (e.g., data logger) to measure voltages and process the information [9].

## Register Map
The HydraProbe does not use a traditional register map like I2C or SPI devices. Instead, measurement data is accessed via predefined parameter sets or transmit sets triggered by specific commands on the SDI-12 or RS-485 interfaces. Calibration coefficients and some settings are also modified using specific commands rather than writing to registers.

Parameters available via commands include [33, 48-52]:
*   Soil Moisture (Water fraction by volume) (H)
*   Bulk Electrical Conductivity (Temperature Corrected) (S/m) (J)
*   Temperature (C) (F)
*   Temperature (F) (G)
*   Bulk Electrical Conductivity (S/m) (O)
*   Real Dielectric Permittivity (Unitless) (K)
*   Imaginary Dielectric Permittivity (Unitless) (M)
*   Real Dielectric Permittivity (Temperature Corrected) (Unitless) (L) [50]
*   Imaginary Dielectric Permittivity (Temperature Corrected) (Unitless) (N) [50]
*   Dielectric Loss Tangent (I) [33]
*   Diode temperature (Celsius) (P) [50]
*   Various Voltage and ADC readings (A, B, C, D, E, R, S, T, U, V) [33, 50].

Calibration coefficients (A, B, C, D) for custom calibrations are set using specific commands (e.g., SDI-12 aXYA<value>!, aXYB<value>!, etc.; RS485 <addr>XA=<value>, <addr>XB=<value>, etc.) [40, 53].

## Package Information / Mechanical Dimensions
The sensor consists of a stainless steel tine assembly (the wave guide), a base plate, and a head/body containing the electronics [54].

*   **Probe Length:** 4.9 inches (124 mm) [1, 11].
*   **Diameter:** 1.6 inches (42 mm) [1, 11]. An optional slim housing version is 1.5 inches (38.8 mm) [1, 11].
*   **Weight:** 7 oz (200 g) [1, 11]. Optional slim housing version is 6.5 oz (184 g) [1, 11]. Cable weight is 0.86 oz/ft (80 g/m) [1, 11].
*   **Tine Assembly:** Four metal rods, 45 mm long by 3 mm wide [54].
*   **Base Plate:** 25 mm in diameter [54].
*   **Sensing Volume (Cylindrical Measurement Region):** The soil between the stainless steel tine assembly [11]. Length 2.2 inches (5.7 cm), Diameter 1.2 inches (3.0 cm) [1, 11]. The probe signal averages the soil in this volume [15].
*   **Head/Body:** Outer casing is ABS, internal electronics are permanently potted with a rock-hard epoxy resin [54].
*   **Cable Lengths:** Available in various standard lengths: 25'/50'/100' (7.5m/15m/30m) for SDI-12 and RS485 versions [1, 11, 16]. Analog cable is available on a 1000' spool [55]. RS485 cable is available on a 1000' spool [55]. SDI-12 cable is available on a 2500' spool [55].

## Basic Usage / Application Information
The HydraProbe is designed to be easy to use [56]. For most applications, calibration is not necessary, and default settings are suitable [56, 57].

*   **Installation:** Requires digging a hole and inserting the probe tines into **undisturbed soil** until the base plate is **flush with the soil surface** [19]. The tines should be **horizontal** with the ground, particularly near the surface [4, 20]. **Avoid rocking the probe** as it disturbs the soil and creates void spaces [20]. Proper backfilling and compacting the soil is important after installation to maintain representative bulk density [58-60]. A drain loop can be put in the cable to prevent water runoff to the sensing area [4]. Running the cable through a metal conduit is recommended for extra protection [6, 61].
*   **Pre-Installation Test:** It is recommended to **setup the logger with the sensors in the office and test the system** before field installation [62]. Probes can be placed in **water to test functionality** [62, 63]. An example test in distilled water with expected readings is provided [63, 64].
*   **Wiring:** Connect the red wire to power (+VDC), black wire to ground. Blue wire for SDI-12 data, Green/White wires for RS-485 data [4-6, 8]. Ensure proper wire connections [65].
*   **Communication Test:** **Test communication between the logger and all probes** after wiring and before backfilling [57, 66]. This can be done via the logger's current reading feature or in SDI-12 transparent mode [57, 66]. The SDI-12 "aI!" command gets the serial number, and "aM!; aD0!, aD1!, aD2!" takes a reading [35]. For RS485, Appendix B commands are used [57, 66]. A Stevens Xplorer SDI-12 to USB adapter can be used for independent SDI-12 testing [35, 66].
*   **Default Settings:** Use the **default factory settings** and the **GENERAL factory soil moisture calibration** for most soil types [57]. The GEN calibration is the default [67-69].
*   **Reading Data:**
    *   **SDI-12:** Use "aM!" or "aC!" commands followed by "aD0!", "aD1!", "aD2!" to retrieve measurement sets [5, 32, 35, 49, 70].
    *   **RS-485:** Use "addrTR"<CR><LF> followed by "addrT0"<CR><LF> to take a reading and retrieve data [41]. Other Transmit Sets (T1-T5) are available [51, 52, 71].
*   **Calibration:** The default GENERAL calibration is suitable for most mineral soils [67, 69, 72]. Other factory calibrations exist for organic soil (O) and rockwool (R) [67, 69, 73]. Custom calibrations are possible and involve empirically solving a polynomial equation based on real dielectric permittivity and gravimetric soil moisture data [68, 69, 74, 75]. Procedures for programming custom calibrations via RS485 and SDI-12 commands are detailed [39, 40, 53, 76-81]. It is recommended to log the real dielectric permittivity (Parameter K or #6) to allow recalibration of historical data if needed [72, 73, 77, 79, 82].

## Compliance and Certifications
The Stevens HydraProbe has demonstrated conformity with relevant electromagnetic compatibility (EMC) standards.

*   **CE Compliance:** The manufacturer, Stevens Water Monitoring Systems, Inc., declares conformity with the **2004/108/EC Electromagnetic Compatibility directive** [83, 84]. The basis for this declaration is compliance with **EN61326-1:2006**, the standard for electrical requirements for measurement, control and laboratory use EMC requirements, specifically for **Class A equipment** regarding Conducted Emissions and Radiated Emissions [85]. Technical documentation supporting this is available [85].
*   **FCC Compliance:** The equipment generates, uses, and can radiate radio frequency energy [86]. It has been tested and found to comply with the limits for a **Class A computing device pursuant to Subpart J of Part 15 of FCC Rules** [86]. These rules are designed to provide reasonable protection against interference in a commercial environment [87]. Operation in a residential area is likely to cause interference, and the user may be required to correct it at their own expense [87]. The sensor meets non-intentional radiator emissions specified by FCC 15.109(g) except at 50 MHz when **NOT buried as specified** [88].