# CDV Project - Temperature and soil moisture measurement system
## Authors: 
Kacper SZCZĘSNY, 
Sebastian KRAWCZYK
<br/>

## Description

We're happy to introduce our soil moisture and temperature monitoring system. The system requires **Raspberry Pi** as a control unit (we used model 3B+ and two sensors: **DS18B20** (digital temperature sensor) and **Grove I2C** (to measure the soil moisture). Grove I2C is used to measure the soil mosture - it's been chosen because this one doesn't require an ADC (Analog-to-digital converter) and this means that we can avoid extra costs, extra cables and extra work. DS18B20 is used to measure the temperature. It can be connected by 1-Wire. The collected information can be sent to the cloud or a local database and visualized on a dashboard.

## Components Used

* Raspberry Pi 3B+ - Control unit
* DS18B20 - Digital temperature sensor
* Grove I2C Moisture Sensor - Capacitive soil moisture sensor (I2C)
* 4.7kΩ Resistor (for DS18B20)
* Connecting wires


## Connection


### DS18B20 (Soil Temperature Sensor)

| DS18B20 Sensor  | Raspberry Pi |
|-----------------|--------------|
| VCC             | 3.3V or 5V   |
| GND             | GND          |
| DATA            | GPIO4 (Pin 7)|
| **4.7kΩ Resistor** | Between VCC and DATA |

### Grove I2C Moisture Sensor (Soil Moisture Sensor)

| Grove I2C Sensor | Raspberry Pi |
|------------------|--------------|
| VCC              | 3.3V         |
| GND              | GND          |
| SDA              | GPIO2 (Pin 3)|
| SCL              | GPIO3 (Pin 5)|


## Installation

1. **Update Raspberry Pi**
   ```sh
   sudo apt update && sudo apt upgrade -y
   ```

2. **Enable 1-Wire interface (for DS18B20)**
   ```sh
   sudo raspi-config
   ```
   * Go to Interfacing Options > 1-Wire and enable it.
   * Restart Raspberry Pi:
      ```sh
      sudo reboot
      ```
3. **Install Python libraries**
    ```sh
   sudo pip install smbus2 w1thermsensor
    ```

4. **Check connected sensors**

    **DS18B20:**
      ```sh
      ls /sys/bus/w1/devices/
      ```
      **Grove I2C:**
      ```sh
      i2cdetect -y 1
      ```
