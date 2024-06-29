import requests

def obtener_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Error al obtener el token: {response.text}")

def obtener_detalles_cluster(access_token, group_id, report_id):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{group_id}/reports/{report_id}"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response)
        return response.json()
    else:
        raise Exception(f"Error al obtener los detalles del cluster: {response.text}")

# Configura tus credenciales y datos
tenant_id = '70d01e02-bce4-44b1-b646-fbf6cbb33d61'
client_id = 'd27ad9f2-9415-4a3e-affc-964d232da685'
client_secret = 'g4s8Q~zOM1Dh-kjV_sACTyukO8Ls7_-5NS-pZbqK'
group_id = 'f9133e48-b95a-4348-992e-2aa96e96ae9f'
report_id = '642fee4b-31c2-42e1-a3b1-5416a21445ce'

# Obtener el token de acceso
token = obtener_token(tenant_id, client_id, client_secret)
print (token)

# Obtener los detalles del cluster
detalles_cluster = obtener_detalles_cluster(token, group_id, report_id)
print(detalles_cluster)
