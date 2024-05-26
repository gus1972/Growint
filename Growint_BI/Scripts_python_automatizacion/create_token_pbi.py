import requests

# Reemplaza estos valores con los tuyos
tenant_id = "70d01e02-bce4-44b1-b646-fbf6cbb33d61"
client_id = "d27ad9f2-9415-4a3e-affc-964d232da685"
client_secret = "g4s8Q~zOM1Dh-kjV_sACTyukO8Ls7_-5NS-pZbqK"
resource = "https://analysis.windows.net/powerbi/api"  # Cambia esto si estás accediendo a otra API

# Construye la URL del punto final del token
url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

# Define los parámetros de la solicitud
payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': resource
}

# Realiza la solicitud HTTP POST para obtener el token
response = requests.post(url, data=payload)
print(response)

# Extrae el token de acceso de la respuesta
token = response.json().get('access_token')

print("Token de acceso: ", token)
