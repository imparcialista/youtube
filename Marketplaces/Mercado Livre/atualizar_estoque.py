import requests
import json
from chaves import access_token

# código de exemplo, você pode utilizar ele para atualizar o estoque de um produto no mercado livre

# access_token = 'SEU_ACCESS_TOKEN_AQUI'
prd = '1111111111'  # insira aqui o código do anúncio do Mercado Livre sem o MLB e sem a hashtag
qtd = 0  # insira aqui a quantidade para atualizar o estoque


def atualizar_estoque(produto, quantidade):
    url = f"https://api.mercadolibre.com/items/MLB{produto}"

    payload = json.dumps({ "available_quantity": quantidade })

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
        }

    response = requests.request("PUT", url, headers=headers, data=payload)

    resposta = response.json()
    print(resposta)

    return resposta