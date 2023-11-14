import requests

url = 'https://cloud.growintegration.es/remote.php/dav/files/Jing'
username = 'gustavo.anton@dataglobalservice.es'
password = 'PdJr3Fc2KBDA'

response = requests.get(url, auth=(username, password))

if response.status_code == 200:
    # Procesar la respuesta exitosa
    print(response.text)
else:
    # Manejar el error
    print(f"Error: {response.status_code} - {response.text}")
