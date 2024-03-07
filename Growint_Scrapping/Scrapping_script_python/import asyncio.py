import asyncio
import requests

from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient
async def copiar_archivo_desde_nextcloud_a_azure():
    # URL del servidor Nextcloud
    url = 'https://cloud.growintegration.es'

    # Credenciales de Nextcloud (usuario y contraseña)
    auth = ('GI_Azure', 'Tinorra1972')

    # Ruta del directorio que quieres copiar desde Nextcloud
    dir_path = '/remote.php/dav/files/GI_Azure/ES%20GD/Marcas/'

    # Conexión al Blob Storage de Azure
    connection_string = 'DefaultEndpointsProtocol=https;AccountName=storegrowint;AccountKey=ymX1a2/tP2E1gUytPoSoJOjiIJr6S3oEGxA1mxi1B/Ml9lHKoV4pQvaRRbKYv3dhfeNa3BivHIeG+AStiQJOVQ==;EndpointSuffix=core.windows.net'
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_name = 'growint'
    container_client = blob_service_client.get_container_client(container_name)

    # Borrar todos los blobs existentes en el contenedor (opcional)
    #async for blob in container_client.list_blobs():
     #   await container_client.delete_blob(blob.name)

    # Listar los archivos en el directorio de Nextcloud
    response = requests.request('PROPFIND', url + dir_path, auth=auth, headers={'Depth': 'infinity'})
    if response.status_code == 207:
        # Parsear la respuesta XML
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)
        for response in root.findall('{DAV:}response'):
            href = response.find('{DAV:}href').text
            if href != dir_path:  # Ignorar el directorio en sí
                file_path = href[len(dir_path):]  # Quitar la ruta del directorio
                # Copiar el archivo a Azure Blob Storage
                blob_client = container_client.get_blob_client(file_path)
                print(url)
                print(href)
                await blob_client.upload_blob_from_url(source_url=url + href, overwrite=True)

# Ejecutar la función
asyncio.run(copiar_archivo_desde_nextcloud_a_azure())
