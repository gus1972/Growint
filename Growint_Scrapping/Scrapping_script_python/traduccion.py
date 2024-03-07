import os
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from urllib.parse import unquote
from googletrans import Translator

# URL de tu servidor Nextcloud
url = 'https://cloud.growintegration.es'

# Credenciales de Nextcloud (usuario y contraseña)
auth = ('GI_Azure', 'Tinorra1972')

# Ruta del directorio que deseas copiar
dir_path = '/remote.php/dav/files/GI_Azure/ES%20GD/Marcas/TMALL/Traffic/'

# Conexión al Blob Storage de Azure
connection_string = 'DefaultEndpointsProtocol=https;AccountName=storegrowint;AccountKey=ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ==;EndpointSuffix=core.windows.net'
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = 'growint'
container_client = blob_service_client.get_container_client(container_name)

def traducir_y_copiar_archivos():
    try:
        # Crea una instancia del traductor
        traductor = Translator()

        # Lista los archivos en el directorio de Nextcloud
        response = requests.request('PROPFIND', url + dir_path, auth=auth, headers={'Depth': 'infinity'})
        if response.status_code == 207:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)
            for response in root.findall('{DAV:}response'):
                href = response.find('{DAV:}href').text
                if href != dir_path:
                    print(href)
                    print(dir_path)
                    file_path = href[len(dir_path):]
                    print(file_path)
                    file_path = unquote(file_path.replace('%20', ' '))

                    # Lee el contenido del archivo en chino
                    response = requests.get(url + href, auth=auth)
                    print(response)
                    contenido_chino = response.content.decode('big5')
                    print(contenido_chino)

                    # Traduce el contenido al castellano
                    contenido_castellano = traductor.translate(contenido_chino, src='zh-cn', dest='es').text

                    # Escribe el contenido traducido en el archivo en castellano
                    print(file_path)
                    if not file_path.endswith('/'):
                     with open(file_path, 'w', encoding='big5') as archivo_castellano:
                        archivo_castellano.write(contenido_castellano)

                    # Copia el archivo traducido al blob storage
                    blob_client = container_client.get_blob_client(file_path)
                    if not file_path.endswith('/'):
                     with open(file_path, 'rb') as archivo_blob:
                        blob_client.upload_blob(archivo_blob)

                    print(f"Traducción y copia exitosa. Archivo en castellano: {file_path}")
        else:
            print(f'Error al listar el directorio {dir_path}: {response.status_code}')
    except Exception as e:
        print(f"Error: {str(e)}")

# Ejemplo de uso
traducir_y_copiar_archivos()
