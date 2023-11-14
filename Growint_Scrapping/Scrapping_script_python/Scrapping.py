import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def descargar_imagen(url, directorio):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        nombre_archivo = os.path.join(directorio, os.path.basename(url))
        with open(nombre_archivo, 'wb') as archivo:
            for chunk in response.iter_content(chunk_size=128):
                archivo.write(chunk)
        print(f"Imagen descargada: {nombre_archivo}")

##def scrape_web(url):
    # Realizar la solicitud HTTP
  ##  response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
  ##  if response.status_code == 200:
        # Crear el objeto BeautifulSoup
     ##   soup = BeautifulSoup(response.text, 'html.parser')

        # Crear un directorio para almacenar las imágenes
     ##   directorio_imagenes = 'imagenes_descargadas'
     ##   os.makedirs(directorio_imagenes, exist_ok=True)

        # Extraer enlaces, imágenes y texto
      ##  for enlace in soup.find_all('a', href=True):
      ##      enlace_absoluto = urljoin(url, enlace['href'])
       ##     print(f"Enlace: {enlace_absoluto}")
##
       # for imagen in soup.find_all('img', src=True):
        #    imagen_absoluta = urljoin(url, imagen['src'])
         #   descargar_imagen(imagen_absoluta, directorio_imagenes)

        #texto = soup.get_text()
        #print(f"Texto: {texto}")

#if __name__ == "__main__":
    # URL de ejemplo
    url_ejemplo = "https://www.xiaohongshu.com/explore/64420138000000000800c6a5"

    # Llamada a la función para hacer scraping
   ## scrape_web(url_ejemplo)
