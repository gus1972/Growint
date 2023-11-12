import requests
import bs4
import pandas as pd

def extract_data(url):
    # Descarga la página web
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    # Extrae las imágenes
    imagenes = []
    for img in soup.find_all('img'):
        imagenes.append({
            'src': img['src'],
            'alt': img['alt']
        })

    # Extrae los enlaces
    enlaces = []
    for a in soup.find_all('a'):
        enlaces.append({
            'href': a['href'],
            'text': a.text
        })

    # Extrae los me gusta
    likes = []
    for div in soup.find_all('div', class_='likes'):
        likes.append(int(div.text))

    # Extrae el texto
    texto = soup.find_all(text=True)

    # Crea un dataframe con los datos extraídos
    data = {
        'imagenes': imagenes,
        'enlaces': enlaces,
        'likes': likes,
        'texto': texto
    }
    df = pd.DataFrame(data)

    # Exporta el dataframe a un archivo Excel
    df.to_excel('data.xlsx')


if __name__ == '__main__':
    # Introduce la URL de la página web
    url = 'https://www.xiaohongshu.com/explore/64391ea00000000012031c65?app_platform=ios&app_version=7.83.1&share_from_user_hidden=true&type=video&xhsshare=CopyLink&appuid=56d68073aed75832340b430a&apptime=1681533592'

    # Extrae los datos
    extract_data(url)
