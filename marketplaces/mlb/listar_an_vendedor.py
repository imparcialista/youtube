import time
import requests
import json
import os
from chaves import id_do_vendedor, access_token


offset = 0
lista = []


def ler_json(arquivo):
    arquivo_json = open(arquivo, encoding='UTF-8')
    data = json.load(arquivo_json)
    return data

def fazer_requisicao(pagina):
    url = f"https://api.mercadolibre.com/users/{id_do_vendedor}/items/search?include_filters=true&status=active&offset={pagina}"

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    resposta = requests.request("GET", url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    return resposta


def pegar_todos_produtos():
    paginas = 0
    resposta = fazer_requisicao(0)
    qtd_anuncios = resposta['paging']['total']

    print('-' * 30)
    print(f'Quantidade de anúncios: {qtd_anuncios}')

    while qtd_anuncios > 0:
        qtd_anuncios -= 50
        paginas += 1

    print(f'Páginas para percorrer: {paginas}')
    print('-' * 30)

    time.sleep(3)


    for pagina in range(paginas):
        print(f'Página: {pagina + 1} | Offset {pagina * 50}')
        resposta = fazer_requisicao(pagina * 50)
        # Aqui vem um resultado de 50 produtos
        # Então vamos adicionar item por item na lista
        for produto in resposta['results']:
            # print(i)
            lista.append(produto)

        # Eu recomendo colocar um tempo entre uma execução e outra
        # Fazer muitas requisições em um curto período não é legal
        time.sleep(1)

    time.sleep(1)

    os.remove('./arquivos/lista.json')
    os.remove('./arquivos/backup.txt')

    time.sleep(1)

    with open("./arquivos/lista.json", "w") as outfile:
        json.dump(lista, outfile)

    with open('./arquivos/backup.txt', 'w') as documento:
        for produto in lista:
            documento.write(f"{produto}\n")


pegar_todos_produtos()
