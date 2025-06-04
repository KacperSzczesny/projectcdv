from flask import Flask, request, jsonify
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, UpdateMode
from datetime import datetime
import os
from dotenv import load_dotenv
import json

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

@app.route('/sensor-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")

    print(f"\n📥 Otrzymano dane:")
    print(f"🌡️ Temperatura: {temperature}°C")
    print(f"💧 Wilgotność: {humidity}")
    print(f"⏱️  Czas: {timestamp}")

    # 1. Zapisz do Azure Blob
    blob_name = f"reading-{timestamp}.json"
    blob_content = json.dumps(data)
    blob_container.upload_blob(name=blob_name, data=blob_content, overwrite=True)
    print(f"✅ Zapisano do Blob: {blob_name}")

    # 2. Zapisz do Azure Table
    entity = {
        "PartitionKey": "sensor1",
        "RowKey": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }
    table_client.upsert_entity(entity=entity, mode=UpdateMode.MERGE)
    print("✅ Zapisano do Table Storage.")

    # 3. Alert, jeśli wilgotność < 300
    if humidity < 300:
        print("⚠️ ALERT: Wilgotność poniżej 300!")

    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
