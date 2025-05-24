import os
from azure.storage.blob import BlobServiceClient
from datetime import datetime

# Pobierz connection string z zmiennej środowiskowej
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    raise ValueError("Brak ustawionego AZURE_STORAGE_CONNECTION_STRING w zmiennych środowiskowych.")

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

container_name = "sensordata"

try:
    container_client = blob_service_client.create_container(container_name)
    print(f"Utworzono kontener: {container_name}")
except Exception:
    container_client = blob_service_client.get_container_client(container_name)
    print(f"Użyto istniejącego kontenera: {container_name}")

sample_data = f"Sensor reading at {datetime.utcnow().isoformat()}"
blob_name = f"reading_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"

blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(sample_data, overwrite=True)

print(f"Przesłano dane do Azure Blob Storage jako: {blob_name}")
