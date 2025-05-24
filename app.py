from flask import Flask, request, redirect, url_for
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Dane do Azure Blob Storage — wpisz swoje
connect_str = "TWOJ_CONNECTION_STRING"
container_name = "mycontainer"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
    blob_client.upload_blob(file, overwrite=True)  # przesyła plik do Azure

    return "File uploaded to Azure Blob Storage successfully!"

if __name__ == '__main__':
    app.run(debug=True)
