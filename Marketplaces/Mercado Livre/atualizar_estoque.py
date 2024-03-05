import requests
import json

# código de exemplo, você pode utilizar ele para atualizar o estoque de um produto no mercado livre

access_token = 'SEU_ACCESS_TOKEN_AQUI'
produto = '1111111111'  # insira aqui o código do anúncio do Mercado Livre sem o MLB e sem a hashtag
quantidade = 0          # insira aqui a quantidade para atualizar o estoque

url = f"https://api.mercadolibre.com/items/MLB{produto}"

payload = json.dumps({
    "available_quantity": quantidade
})

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
