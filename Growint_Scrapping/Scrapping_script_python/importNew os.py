import os
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Configuration
nextcloud_url = 'https://cloud.growintegration.es'
nextcloud_auth = ('GI_Azure', 'Tinorra1972')
blob_connection_string = 'DefaultEndpointsProtocol=https;AccountName=dicstoregrow;AccountKey=YOUR_ACCOUNT_KEY;EndpointSuffix=core.windows.net'
container_name = 'diccont'
directory_path='/remote.php/dav/files/GI_Azure/Marcas/TMALL/Diccionario Productos/'


#def copy_directory(directory_path):
"""
Copies files from the specified directory to the blob storage container.
    """
try:
        # Connect to Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # List files and subdirectories
        response = requests.request('PROPFIND', f'{nextcloud_url}{directory_path}', auth=nextcloud_auth, headers={'Depth': '1'})
        if response.status_code == 207:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)
            for href in root.findall('{DAV:}response/{DAV:}href'):
                file_path = href.text[len(directory_path) + 1:].replace('%20', ' ')

                # Skip directories and empty files
                if file_path.endswith('/') or os.path.getsize(f'{nextcloud_url}{file_path}') == 0:
                    continue

                # Upload file to Azure Blob Storage
                blob_client = container_client.get_blob_client(os.path.basename(file_path))
                blob_client.upload_blob(requests.get(f'{nextcloud_url}{file_path}', auth=nextcloud_auth).content)
        else:
            print(f'Error listing directory: {directory_path}, status: {response.status_code}')
except Exception as e:
        print(f'Error copying directory {directory_path}: {e}')


