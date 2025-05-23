from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient

# === Returns a BlobServiceClient using the given connection string ===
def get_blob_service_client(connection_string):
    return BlobServiceClient.from_connection_string(connection_string)

# === Returns a TableClient and creates the table if it doesn't exist ===
def get_table_client(connection_string, table_name):
    table_service = TableServiceClient.from_connection_string(connection_string)
    table_client = table_service.get_table_client(table_name)
    try:
        table_client.create_table()
    except:
        pass
    return table_client

# === Creates a container if it doesn't already exist ===
def create_container_if_not_exists(blob_service_client, container_name):
    try:
        blob_service_client.create_container(container_name)
    except Exception as e:
        print(f"Container may already exist or there was an error: {e}")
