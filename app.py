from flask import Flask, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, UpdateMode
from datetime import datetime, timezone
from dateutil import parser
import os
from dotenv import load_dotenv
import json
import pytz

# Wczytaj zmienne środowiskowe z .env
load_dotenv()

AZURE_BLOB_CONN_STR = os.getenv("AZURE_BLOB_CONN_STR")
AZURE_TABLE_CONN_STR = os.getenv("AZURE_TABLE_CONN_STR")
BLOB_CONTAINER = os.getenv("BLOB_CONTAINER")
TABLE_NAME = os.getenv("TABLE_NAME")

app = Flask(__name__)

# Azure Blob i Table klienty
blob_service = BlobServiceClient.from_connection_string(AZURE_BLOB_CONN_STR)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

table_service = TableServiceClient.from_connection_string(AZURE_TABLE_CONN_STR)
table_client = table_service.get_table_client(TABLE_NAME)

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    poland_tz = pytz.timezone('Europe/Warsaw')
    local_timestamp = datetime.now(poland_tz).strftime("%Y-%m-%d, %H:%M")
    utc_rowkey = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

    print(f"\n📥 Otrzymano dane:")
    print(f"🌡️ Temperatura: {temperature}°C")
    print(f"💧 Wilgotność: {humidity}")
    print(f"⏱️  Czas lokalny (PL): {local_timestamp}")

    # Blob Storage
    blob_name = f"reading-{utc_rowkey}.json"
    blob_content = json.dumps(data)
    blob_container.upload_blob(name=blob_name, data=blob_content, overwrite=True)
    print(f"✅ Zapisano do Blob: {blob_name}")

    # Table Storage
    entity = {
        "PartitionKey": "sensor1",
        "RowKey": utc_rowkey,
        "temperature": temperature,
        "humidity": humidity,
        "timestamp": local_timestamp
    }
    table_client.upsert_entity(entity=entity, mode=UpdateMode.MERGE)
    print("✅ Zapisano do Table Storage.")

    if humidity < 50:
        print("⚠️ ALERT: Wilgotność poniżej 50!")

    return jsonify({"status": "OK"}), 200

@app.route("/readings", methods=["GET"])
def get_readings():
    print("GET /readings received")
    entities = table_client.query_entities("PartitionKey eq 'sensor1'")
    sorted_entities = sorted(entities, key=lambda x: x["RowKey"], reverse=True)
    recent = sorted_entities[:10]

    readings = []
    for r in recent:
        timestamp = r.get("timestamp", r["RowKey"])
        readings.append({
            "timestamp": timestamp,
            "temperature": r["temperature"],
            "humidity": r["humidity"]
        })

    return jsonify(readings)

@app.route('/')
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
