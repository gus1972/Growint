import os
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import schedule
import time


# URL del servidor Nextcloud
url = 'https://cloud.growintegration.es'

# Credenciales de Nextcloud (usuario y contraseña)
auth = ('GI_Azure', 'Tinorra1972')

# Ruta del directorio que quieres copiar
dir_path = '/remote.php/dav/files/GI_Azure/Marcas/TMALL'
print(dir_path)

# Conexión al Blob Storage de Azure
connection_string = 'DefaultEndpointsProtocol=https;AccountName=storegrowint;AccountKey=ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = 'growint'
container_client = blob_service_client.get_container_client(container_name)

# Listar los archivos en el directorio
response = requests.request('PROPFIND', url + dir_path, auth=auth, headers={'Depth': 'infinity'})
print(response.status_code)
if response.status_code == 207:
    # Parsear la respuesta XML
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)
    for response in root.findall('{DAV:}response'):
        href = response.find('{DAV:}href').text
        print(href)
        if href != dir_path:  # Ignorar el directorio en sí
            file_path = href[len(dir_path):]  # Quitar la ruta del directorio
            print(file_path)
            # Leer el archivo desde Nextcloud
            response = requests.get(url + href, auth=auth)
            print(response)
            if response.status_code == 200:
                # Subir el archivo a Azure Blob Storage
                blob_client = container_client.get_blob_client(file_path)
                blob_client.upload_blob(response.content)
            else:
                print(f'Error al leer el archivo {file_path}: {response.status_code}')
else:
    print(f'Error al listar el directorio {dir_path}: {response.status_code}')
