from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Connection to Azurite (local Azure Blob Storage emulator)
connection_string = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

# Container and blob names
container_name = 'mio-container'
blob_name = 'log.txt'
local_file_path = 'log.txt'

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Create the container if it doesn't exist
try:
    container_client = blob_service_client.create_container(container_name)
    print(f"Container '{container_name}' created.")
except Exception as e:
    container_client = blob_service_client.get_container_client(container_name)
    print(f"Container '{container_name}' already exists.")

# Get the blob client
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

# Check if the file exists before uploading
if os.path.exists(local_file_path):
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"File '{blob_name}' uploaded to container '{container_name}'.")
else:
    print(f"File '{local_file_path}' does not exist.")

