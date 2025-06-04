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

## Costs

So, what we need to start with it?

1. **Azure IoT Hub: For device-to-cloud communication.**
2. **Azure Functions: To process incoming data.**
3. **Azure Blob Storage: For storing sensor data.**
4. **Azure Table Storage: For structured data storage.**
5. **Azure Logic Apps: For automating workflows and notifications.​**

Estimated monthly cost: $11.86

Why we chose these options?

1. **IoT Hub** (Free/Basic tier) – Ideal for low-frequency sensor data; scalable later.
2. **Functions** – Serverless logic with cost per execution; it means that no idle charges.
3. **Blob Storage** (Hot/Standard) – Stores frequent sensor readings at low cost.
4. **Table Storage** – it's just efficient, enough and (it's important in small projects like this) **cheap** for time-series data like temperature logs.
5. **Logic Apps** – we configured it with low daily execution limits to stay cheap.



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

5. Install git
      ```sh
      apt install git 
      ```

6. Clone the repository
      ```sh
      git clone https://github.com/KacperSzczesny/projectcdv
      ```
7. Install backend dependencies
      ```sh
      sudo apt update && apt upgrade -y
      sudo apt-get install python3-pip
      pip install Flask
      pip install -r requirements.txt
      ```
8. Create an .env file - edit a name of "env file" to ".env", edit the file (fill it with your Azure's data). 
   It's for your safety - you don't have to worry about your Azure's data because it will be in the other than app.py file!
      ```
      AZURE_BLOB_CONN_STR=CONNECTION_STRING_FROM_AZURE
      AZURE_TABLE_CONN_STR=CONNECTION_STRING_FROM_AZURE
      BLOB_CONTAINER=sensordata
      TABLE_NAME=readings
      ```


9. Start the backend server
      ```sh
      python3 app.py
      ```

# IF YOU WANT TO TEST THIS SCRIPT WITHOUT DEVICE, RUN VIRTUAL ENVIRONMENT
**Type below commands after step 7**
```sh
   python3 -m venv venv
   source venv/bin/activate
   python3 app.py
```

