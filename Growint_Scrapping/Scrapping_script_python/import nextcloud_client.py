from azure.storage.blob import BlobServiceClient
import requests
from requests.auth import HTTPBasicAuth

# Configuración de Nextcloud
nextcloud_url = "https://cloud.growintegration.es/remote.php/dav/files/GI_Azure"
nextcloud_username = "GI_Azure "
nextcloud_password = "Tinorra1972"

# Configuración de Azure
connection_string = "DefaultEndpointsProtocol=https;AccountName=storegrowint;AccountKey=ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ==;EndpointSuffix=core.windows.net"
container_name = "growint"

# Inicializar el cliente de Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Función para copiar archivos de un directorio de Nextcloud a Azure Blob Storage
def copy_directory(directory):
    # Obtener la lista de archivos y subdirectorios
    print(directory)
    response = requests.request('PROPFIND', nextcloud_url + directory, auth=HTTPBasicAuth(nextcloud_username, nextcloud_password))
    print(response)
    print(nextcloud_url+directory)
    response.raise_for_status()  # Asegúrate de que la solicitud fue exitosa

    # Analizar la respuesta XML
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)

    # Espacio de nombres DAV
    ns = {'d': 'DAV:'}
    print(ns)

    # Recorrer todos los elementos 'response' en el XML
    for response in root.findall('d:response', ns):
        print(response)
        # Obtener el 'href' del elemento 'response'
        href = response.find('d:href', ns).text
        print(href)
        

        # Comprobar si el 'href' es un archivo o un subdirectorio
        if href.endswith('/'):  # Es un subdirectorio
            # Recursivamente copiar el subdirectorio
            copy_directory(href)
            print(copy_directory)
        else:  # Es un archivo
            # Descargar el archivo de Nextcloud
            file_response = requests.get(nextcloud_url + href, auth=(nextcloud_username, nextcloud_password))
            file_response.raise_for_status()  # Asegúrate de que la descarga fue exitosa

            # Subir el archivo a Azure Blob Storage
            blob_client = blob_service_client.get_blob_client(container_name, href)
            blob_client.upload_blob(file_response.content)

# Copiar el directorio y sus subdirectorios
copy_directory("/Marcas")
