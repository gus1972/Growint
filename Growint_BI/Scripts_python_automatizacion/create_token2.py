import requests

# Configuración de la aplicación registrada en Azure AD
client_id = 'd27ad9f2-9415-4a3e-affc-964d232da685'
client_secret = 'g4s8Q~zOM1Dh-kjV_sACTyukO8Ls7_-5NS-pZbqK'
tenant_id = '70d01e02-bce4-44b1-b646-fbf6cbb33d61'
group_id = 'f9133e48-b95a-4348-992e-2aa96e96ae9f'
report_id = '642fee4b-31c2-42e1-a3b1-5416a21445ce'

# URL para obtener el token de acceso
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

# Solicitud para obtener el token de acceso
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': "https://analysis.windows.net/powerbi/api/.default"
}

response = requests.post(token_url, data=token_data)
response_data = response.json()
print("Respuesta del token:", response_data)
token = response_data.get('access_token')

# Verificación del token de acceso
if not token:
    print("Error al obtener el token de acceso")
    print(response_data)
    exit()

# Configuración del encabezado de autorización
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
print("Encabezados:", headers)

# URL para obtener los detalles del clúster
cluster_details_url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}"
print (cluster_details_url)

# Realización de la solicitud
response = requests.get(cluster_details_url, headers=headers)
print(response)
# Verificación de la respuesta
if response.status_code == 200:
    print("Detalles del clúster obtenidos correctamente.")
    print(response.json())
else:
    print(f"Error al obtener los detalles del clúster: {response.status_code}")
    print(response.json())
