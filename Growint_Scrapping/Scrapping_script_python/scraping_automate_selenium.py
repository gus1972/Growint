import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import schedule

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def scrape_url(url, output_directory):
    # Configuración del navegador (ajusta según el navegador que estés utilizando)
    driver = webdriver.Firefox(executable_path='/path/to/geckodriver')

    try:
        # Cargar la URL en el navegador
        driver.get(url)
        time.sleep(2)  # Esperar a que la página se cargue completamente (ajusta según sea necesario)

        # Aquí puedes agregar código para interactuar con la página utilizando Selenium
        # Ejemplo: Obtener el texto de un elemento
        text_element = driver.find_element_by_css_selector('selector_del_elemento_de_texto')
        texto = text_element.text
        print(f'Texto: {texto}')

        # Ejemplo: Obtener la cantidad de likes
        likes_element = driver.find_element_by_css_selector('selector_del_elemento_de_likes')
        likes = likes_element.text
        print(f'Likes: {likes}')

        # Ejemplo: Obtener la cantidad de fotos
        fotos_element = driver.find_element_by_css_selector('selector_del_elemento_de_fotos')
        fotos = fotos_element.text
        print(f'Fotos: {fotos}')

        # Ejemplo: Obtener la cantidad de videos
        videos_element = driver.find_element_by_css_selector('selector_del_elemento_de_videos')
        videos = videos_element.text
        print(f'Videos: {videos}')

        # Puedes agregar más lógica aquí para interactuar con otros elementos de la página

        # Guardar el resultado en un archivo en el directorio de salida
        filename = f'{url.replace("https://", "").replace("http://", "").replace("/", "_")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        filepath = os.path.join(output_directory, filename)
        with open(filepath, 'w') as file:
            file.write(f'Texto: {texto}\nLikes: {likes}\nFotos: {fotos}\nVideos: {videos}\n')

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Cerrar el navegador al finalizar
        driver.quit()

def scrape_all_urls(output_directory):
    # Lista de URLs a scrapear
    urls = ['https://www.ejemplo1.com', 'https://www.ejemplo2.com', 'https://www.ejemplo3.com']

    for url in urls:
        scrape_url(url, output_directory)

# Crear un directorio para almacenar los resultados
output_directory = 'resultados_scraping'
create_directory(output_directory)

# Programar el scraping cada dos meses (ajusta según tus necesidades)
schedule.every(2).months.do(scrape_all_urls, output_directory)

while True:
    schedule.run_pending()
    time.sleep(1)
