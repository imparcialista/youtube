import requests

# código de exemplo, você pode utilizar ele para gerar um novo refresh token

client_id = 'SEU_CLIENT_ID_AQUI'
client_secret = 'SEU_CLIENT_SECRET_AQUI'
refresh_token = 'SEU_REFRESH_TOKEN_AQUI'

url = "https://api.mercadolibre.com/oauth/token"

payload = f'grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}'
headers = {
  'accept': 'application/json',
  'content-type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

