import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, output_directory):
    # Realizar la solicitud HTTP a la página web
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas las etiquetas de imágenes
        img_tags = soup.find_all('img')

        # Crear el directorio de salida si no existe
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Descargar cada imagen
        for img_tag in img_tags:
            img_url = urljoin(url, img_tag['src'])
            img_data = requests.get(img_url).content

            # Obtener el nombre del archivo de la URL
            img_filename = os.path.join(output_directory, os.path.basename(img_url))

            # Guardar la imagen en el directorio de salida
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)

            print(f"Imagen descargada y guardada: {img_filename}")

        print(f"Todas las imágenes han sido descargadas y guardadas en {output_directory}")

    else:
        print(f"Error al realizar la solicitud HTTP. Código de estado: {response.status_code}")

# URL de ejemplo (cambia a la URL que deseas analizar)
url_to_extract = 'https://www.xiaohongshu.com/explore/642411390000000014026fda'
# Directorio de salida para las imágenes descargadas
output_directory = 'C:\Users\Gusta\Documents\ficheros_exportados_scrapping'
download_images(url_to_extract, output_directory)
