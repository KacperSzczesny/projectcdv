from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, UpdateMode
from datetime import datetime, timezone
datetime.now(timezone.utc).strftime("%Y%m%d, %H%M")
from dateutil import parser
import os
from dotenv import load_dotenv
import json
import sqlite3
import pytz

# .env - dane azure w innym pliku
load_dotenv()

AZURE_BLOB_CONN_STR = os.getenv("AZURE_BLOB_CONN_STR")
AZURE_TABLE_CONN_STR = os.getenv("AZURE_TABLE_CONN_STR")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
TABLE_NAME = os.getenv("TABLE_NAME")

app = Flask(__name__)

# Blob
blob_service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONN_STR)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

# Table Storage
table_service = TableServiceClient.from_connection_string(AZURE_TABLE_CONN_STR)
table_client = table_service.get_table_client(TABLE_NAME)

## DB

def init_db():
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            humidity INTEGER
        )'''
    )
    conn.commit()
    conn.close()

'''
    def save_to_db(temperature, humidity, timestamp):
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (timestamp, temperature, humidity) VALUES (?, ?, ?)",
                   (timestamp, temperature, humidity))
    conn.commit()
    conn.close() 
'''


@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    #Polska strefa czasowa (dla czytelnego wyświetlania)
    poland_tz = pytz.timezone('Europe/Warsaw')
    local_timestamp = datetime.now(poland_tz).strftime("%Y-%m-%d, %H:%M")

    utc_rowkey = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    print(f"\n📥 Otrzymano dane:")
    print(f"🌡️ Temperatura: {temperature}°C")
    print(f"💧 Wilgotność: {humidity}")
    print(f"⏱️  Czas lokalny (PL): {local_timestamp}")

    #Zapisz do Azure Blob
    blob_name = f"reading-{utc_rowkey}.json"
    blob_content = json.dumps(data)
    blob_container.upload_blob(name=blob_name, data=blob_content, overwrite=True)
    print(f"✅ Zapisano do Blob: {blob_name}")

    #Zapisz do Azure Table Storage
    entity = {
        "PartitionKey": "sensor1",
        "RowKey": utc_rowkey,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": local_timestamp
    }
    table_client.upsert_entity(entity=entity, mode=UpdateMode.MERGE)
    print("✅ Zapisano do Table Storage.")

    #Zapis do SQLite
    save_to_db(temperature, humidity, local_timestamp)
    print(f"💾 Zapisano do lokalnej bazy danych.")

    # 🔔 Alert, jeśli wilgotność < 20
    if humidity < 20:
        print("⚠️ ALERT: Wilgotność poniżej 20!")

    return jsonify({"status": "OK"}), 200

#dashboard
'''
@app.route('/readings', methods=['GET'])
def get_readings():
    conn = sqlite3.connect("soil_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, temperature, humidity FROM readings ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()

    poland_tz = pytz.timezone('Europe/Warsaw')

    readings = []
    for r in rows:
        try:
            parsed_time = parser.parse(r[0])
            local_time = parsed_time.astimezone(poland_tz).strftime("%Y-%m-%d, %H:%M")
        except:
            local_time = r[0]

        readings.append({
            "timestamp": local_time,
            "temperature": r[1],
            "humidity": r[2]
        })

    return jsonify(readings) '''

#testowy   
@app.route("/readings", methods=["GET"])
    def get_readings():
        print("GET /readings received")
        return jsonify([])  # tymczasowo pusta lista


@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


if __name__ == '__main__':
    init_db()
    print("✅ Baza SQLite została zainicjalizowana.")
    app.run(debug=True)
