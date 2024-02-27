import easywebdav
import string
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
try:
    basestring
except NameError:
    basestring = str


# Configura tu cliente WebDAV
webdav = easywebdav.connect(
    host='cloud.growintegration.es',
    username='GI_Azure',
    password='Tinorra1972',
    protocol='https',
    port=443
)





# Lista todos los archivos en tu directorio Nextcloud
files = webdav.ls('/remote.php/dav/files/GI_Azure/Marcas/TMALL/01 Kpis')

# Configura tu cliente Azure Blob Storage
connection_string = "DefaultEndpointsProtocol=https;AccountName=storegrowint;AccountKey=ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "growint"
container_client = blob_service_client.get_container_client(container_name)

# Descarga cada archivo y súbelo a Azure Blob Storage
for file in files:
    if not file.name.endswith('/'):  # Ignora los directorios
        # Descarga el archivo de Nextcloud
        

        webdav.download(file.name, '/remote.php/dav/files/GI_Azure/Marcas/TMALL/01 Kpis')

        # Crea un BlobClient
        blob_client = blob_service_client.get_blob_client(container_name, file.name)

        # Sube el archivo a Azure Blob Storage
        with open('/local/path/to/download/file', 'rb') as data:
            blob_client.upload_blob(data)
