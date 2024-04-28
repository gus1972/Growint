import os
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from unidecode import unidecode
from urllib.parse import unquote
import schedule
import time
import datetime
from azure.core.exceptions import ResourceExistsError
from concurrent.futures import ThreadPoolExecutor

# Obtén la hora actual
now = datetime.datetime.now().time()

# Define las horas de inicio y fin
start_time = datetime.time(6, 54)  # 06:54 AM
end_time = datetime.time(18, 00)  # 18:00 PM

# Comprueba si la hora actual está dentro del rango
if start_time <= now <= end_time:
    # URL del servidor Nextcloud
    url = 'https://cloud.growintegration.es'

    # Credenciales de Nextcloud (usuario y contraseña)
    auth = ('GI_Azure', 'Tinorra1972')

    # Nombre de carpeta que se crea en el contenedor de azure
    main_folder = 'Marcas'

    # Ruta del directorio que quieres copiar
    dir_path = '/remote.php/dav/files/GI_Azure/ES%20GD/Marcas/'
    print(dir_path)

    # Conexión al Blob Storage de Azure
    connection_string = 'DefaultEndpointsProtocol=https;AccountName=storegrowint;AccountKey=ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = 'growint'
    container_client = blob_service_client.get_container_client(container_name)

    # Borrar todos los blobs en el contenedor
    print("Borrando blobs existentes...")
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print(f"Borrando blob {blob.name}...")
        blob_client = container_client.get_blob_client(blob.name)
        blob_client.delete_blob()

    # Verificar si todos los blobs se han borrado
    blob_list = container_client.list_blobs()
    if len(list(blob_list)) == 0:
        print("Todos los blobs se han borrado correctamente.")
    else:
        print("No todos los blobs se han borrado.")

    # Listar los archivos en el directorio
    response = requests.request('PROPFIND', url + dir_path, auth=auth, headers={'Depth': 'infinity'})
    print(response.status_code)

    def upload_file(href):
        if href != dir_path:  # Ignorar el directorio en sí
            print(href)
            print(dir_path)
            print(len(dir_path))
            file_path = href[len(dir_path):]  # Quitar la ruta del directorio
            print(file_path)
            # Reemplazar %20 por un espacio en blanco
            file_path = unquote(file_path.replace('%20', ' '))
            print(file_path)
            # Leer el archivo desde Nextcloud
            response = requests.get(url + href, auth=auth)
            print(response)
            if response.status_code == 200:
                today = datetime.datetime.today()
                if today.weekday() < 5:  # No es fin de semana
                    try:
                        blob_client = container_client.get_blob_client(main_folder + '/' + file_path)
                        blob_client.upload_blob(response.content)
                        print("Blob created successfully.")
                    except ResourceExistsError:
                        # Handle the case where the blob already exists
                        print("Blob already exists. You may want to update or delete it.")
                        blob_client.upload_blob(response.content, overwrite=True)
            else:
                print(f'Error al leer el archivo {file_path}: {response.status_code}')

    if response.status_code == 207:
        # Parsear la respuesta XML
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)
        hrefs = [response.find('{DAV:}href').text for response in root.findall('{DAV:}response')]
        with ThreadPoolExecutor(max_workers=30) as executor:
            executor.map(upload_file, hrefs)
    else:
        print(f'Error al listar el directorio {dir_path}: {response.status_code}')
else:
    print("La hora actual no está dentro del rango de 06:54 a 18:00.")
