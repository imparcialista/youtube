import json
import requests
from chaves import access_token


def ler_json(arquivo):
    arquivo_json = open(arquivo, encoding='UTF-8')
    data = json.load(arquivo_json)
    # Exemplo: ler_json('./arquivos/lista.json')
    return data


def fazer_reqs(url):
    payload = { }
    headers = { 'Authorization': f'Bearer {access_token}' }

    resposta = requests.request('GET', url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    return resposta


def atualizar_estoque(produto, quantidade):
    url = f"https://api.mercadolibre.com/items/{produto}"

    if quantidade > 0:
        payload = json.dumps({ 'available_quantity': quantidade, 'status': 'active' })
    else:
        payload = json.dumps({ 'available_quantity': quantidade })

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
        }

    resposta = requests.request("PUT", url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print(f'{produto} | falha na requisição')
        # resposta.raise_for_status()
    else:
        print(f'{produto} estoque alterado para {quantidade}')

    resposta = resposta.json()

    return resposta