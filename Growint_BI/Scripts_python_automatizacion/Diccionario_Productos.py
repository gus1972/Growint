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
dir_path = '/remote.php/dav/files/GI_Azure/ES%20GD/Marcas/TMALL/Diccionario%20Productos/'
print(dir_path)

# Conexión al Blob Storage de Azure
connection_string = 'DefaultEndpointsProtocol=https;AccountName=dicstoregrow;AccountKey=UpXPqFLwWuruIXBDaIuuH0ypYI/axnzJ5PkCSwp7monNKVyt9d8++B6jqYhc8qgqvqIAWto2zFqC+AStB6s5JQ==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = 'diccont'
container_client = blob_service_client.get_container_client(container_name)

# Borrar todos los blobs en el contenedor
#print("Borrando blobs existentes...")
#blob_list = container_client.list_blobs()
#for blob in blob_list:
 #   print(f"Borrando blob {blob.name}...")
  #  blob_client = container_client.get_blob_client(blob.name)
   # blob_client.delete_blob()

# Listar los archivos en el directorio
response = requests.request('PROPFIND', url + dir_path, auth=auth, headers={'Depth': '1'})
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
            # Reemplazar %20 por un espacio en blanco
            file_path = file_path.replace('%20', ' ')
            print(file_path)
            # Leer el archivo desde Nextcloud
            response = requests.get(url + href, auth=auth)
            print(response)
            if response.status_code == 200:
                # Comprobar si es un archivo (no termina en '/')
                print(file_path)
                if not file_path.endswith('/'):
                    # Subir el archivo a Azure Blob Storage
                    # Solo usar el nombre del archivo, no la estructura de directorios
                    blob_name = os.path.basename(file_path)
                    blob_client = container_client.get_blob_client(blob_name)
                    blob_client.upload_blob(response.content, overwrite=True)
            else:
                print(f'Error al leer el archivo {file_path}: {response.status_code}')
else:
    print(f'Error al listar el directorio {dir_path}: {response.status_code}')
