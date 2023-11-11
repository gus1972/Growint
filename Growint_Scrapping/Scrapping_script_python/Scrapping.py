import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL de la página web a raspar
url = 'https://www.ejemplo.com'

# Realiza una solicitud HTTP GET a la URL
response = requests.get(url)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    # Analiza el contenido de la página con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra todos los enlaces en la página
    links = []
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url:
            # Convierte las URLs relativas en URLs absolutas
            absolute_url = urljoin(url, link_url)
            links.append(absolute_url)

    # Encuentra todas las imágenes en la página
    images = []
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            # Convierte las URLs relativas en URLs absolutas
            absolute_url = urljoin(url, img_url)
            images.append(absolute_url)

    # Encuentra el texto en la página
    text = soup.get_text()

    # Puedes imprimir o guardar los enlaces, imágenes y texto como desees
    print("Enlaces:")
    for link in links:
        print(link)

    print("\nImágenes:")
    for image in images:
        print(image)

    print("\nTexto:")
    print(text)
else:
    print(f"No se pudo acceder a la página {url}. Código de estado: {response.status_code}")
