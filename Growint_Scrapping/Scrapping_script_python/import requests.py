from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os

def descargar_imagen(url, nombre_archivo):
    response = requests.get(url, stream=True)
    with open(nombre_archivo, 'wb') as archivo:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                archivo.write(chunk)

def extraer_imagenes(url_pagina):
    # Configura el controlador de Selenium (reemplaza 'PATH_AL_CHROMEDRIVER' con la ubicación real de tu archivo chromedriver.exe)
    driver = webdriver.Chrome(executable_path='PATH_AL_CHROMEDRIVER')

    # Abre la página web
    driver.get(url_pagina)

    # Espera a que la página cargue completamente (puede necesitar ajustes dependiendo de la página)
    driver.implicitly_wait(10)

    # Extrae el HTML de la página después de que todos los pop-ups hayan cargado
    pagina_html = driver.page_source

    # Parsea el HTML con BeautifulSoup
    soup = BeautifulSoup(pagina_html, 'html.parser')

    # Encuentra todas las etiquetas <img>
    etiquetas_img = soup.find_all('img')

    # Crea un directorio para guardar las imágenes
    if not os.path.exists('imagenes_extraidas'):
        os.makedirs('imagenes_extraidas')

    # Descarga cada imagen encontrada
    for img_tag in etiquetas_img:
        img_src = img_tag['src']
        nombre_archivo = os.path.join('imagenes_extraidas', img_src.split('/')[-1])
        descargar_imagen(img_src, nombre_archivo)
        print(f"Imagen descargada: {nombre_archivo}")

    # Cierra el navegador
    driver.quit()

if __name__ == "__main__":
    url_pagina = 'URL_DE_LA_PAGINA'  # Reemplaza con la URL real
    extraer_imagenes(url_pagina)
