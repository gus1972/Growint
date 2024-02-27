from azure.storage.blob import BlobServiceClient, BlobClient
from webdav3.client import Client
import os

# Credenciales Nextcloud
nextcloud_url = "https://cloud.growintegration.es"
your_account_url="https://storegrowint.blob.core.windows.net/"
nextcloud_username = "GI_Azure"
nextcloud_password = "Tinorra1972"

# Credenciales Azure Blob Storage
azure_storage_account_name = "storegrowint"
azure_storage_account_key = "ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ=="
azure_container_name = "growint"

# Directorio Nextcloud
nextcloud_dir = "https://cloud.growintegration.es/remote.php/dav/files/GI_Azure/Marcas/TMALL"

# Conexión a Nextcloud
client = Client(nextcloud_url)

# Conexión a Azure Blob Storage
blob_service_client = BlobServiceClient(account_url=your_account_url, account_name=azure_storage_account_name, account_key=azure_storage_account_key)
print(blob_service_client)
blob_container = blob_service_client.get_container_client(azure_container_name)
print(blob_container)
print(os.listdir(nextcloud_dir))
# Recorrer directorio Nextcloud
for files in os.walk(nextcloud_dir):
    for file in files:
        # Obtener archivo de Nextcloud
        file_path = os.path.join(root, file)
        with client.open(file_path, "rb") as f:
            file_content = f.read()

        # Subir archivo a Azure Blob Storage
        blob_client = blob_container.get_blob_client(file)
        blob_client.upload_blob(file_content)

print("Archivos cargados correctamente en Azure Blob Storage")
