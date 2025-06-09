import requests
import random
import time
import os

API_URL = os.getenv("API_URL", "https://apppy-bxdgheajcefybzcu.westeurope-01.azurewebsites.net/sensor-data")

def generate_sensor_data():
    temperature = round(random.uniform(15.0, 30.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    return {"temperature": temperature, "humidity": humidity}

def send_data():
    data = generate_sensor_data()
    try:
        response = requests.post(API_URL, json=data)
        print(f"Sent data: {data} | Response: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    while True:
        send_data()
        time.sleep(10)  
