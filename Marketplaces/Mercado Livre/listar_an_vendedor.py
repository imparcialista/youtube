import time
import requests
import json
import os
from chaves import access_token

# TODO Criar uma interface visual para gerenciamento dos anúncios

# Dica!
# Para pegar o id do vendedor de um access token
# Utilize: id_do_vendedor = access_token[-9:]

inicio_timer = time.time()

id_do_vendedor = access_token[-9:]
offset = 0
lista = []
separador = '-' * 30
deletar_existentes = True
apenas_itens_ativos = False


def ler_json(arquivo):
    arquivo_json = open(arquivo, encoding='UTF-8')
    data = json.load(arquivo_json)
    # Exemplo: ler_json('./arquivos/lista.json')
    return data


def fazer_reqs(pagina):
    if apenas_itens_ativos:
        filtro = 'include_filters=true&status=active'
    else:
        filtro = ''

    url = (f'https://api.mercadolibre.com/users/'
           f'{id_do_vendedor}/items/search?{filtro}&offset='
           f'{pagina}')

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
        }

    resposta = requests.request('GET', url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    return resposta


def pegar_scroll_id():
    url = (f'https://api.mercadolibre.com/users/'
           f'{id_do_vendedor}/items/search?search_type=scan&limit=100')

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
        }

    resposta = requests.request('GET', url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    # print(resposta)     # teste
    return resposta


def proxima_pagina(scroll):
    url = (f'https://api.mercadolibre.com/users/'
           f'{id_do_vendedor}/items/search?search_type=scan&scroll_id={scroll}&limit=100')

    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
        }

    resposta = requests.request('GET', url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    # print(resposta)     # teste
    return resposta


def pegar_todos_produtos():
    paginas = 0
    resposta = fazer_reqs(0)
    quantidade_de_an = resposta['paging']['total']

    if quantidade_de_an == 0:
        print(separador)
        print('Nenhum anúncio ativo')
        print('Programa finalizado')
        print(separador)
        return

    if quantidade_de_an > 1000:
        print(separador)
        print(f'Quantidade de anúncios: {quantidade_de_an}')

        while quantidade_de_an > 0:
            quantidade_de_an -= 100
            paginas += 1

        print(f'Páginas para percorrer: {paginas}')
        print(separador)
        paginas = paginas - 1

        lista_scroll = []

        primeiro_scroll = pegar_scroll_id()
        print(f'Produtos coletados: {len(primeiro_scroll["results"])}')

        lista_scroll.append(primeiro_scroll['scroll_id'])
        for produto in primeiro_scroll['results']:
            lista.append(produto)


        def gerar_scroll(scroll_anterior):
            scroll = proxima_pagina(scroll_anterior)
            print(f'Produtos coletados: {len(scroll["results"])}')

            for produto in scroll['results']:
                lista.append(produto)

            lista_scroll.append(scroll['scroll_id'])


        for pagina in range(paginas):
            gerar_scroll(lista_scroll[pagina])


    else:
        resposta = fazer_reqs(0)
        quantidade_de_an = resposta['paging']['total']

        print(separador)
        print(f'Quantidade de anúncios: {quantidade_de_an}')

        while quantidade_de_an > 0:
            quantidade_de_an -= 50
            paginas += 1

        print(f'Páginas para percorrer: {paginas}')
        print(separador)

        time.sleep(3)

        for pagina in range(paginas):
            print(f'Página: {pagina + 1} | Offset {pagina * 50}')
            resposta = fazer_reqs(pagina * 50)

            # Aqui vem um resultado de 50 produtos
            # Então vamos adicionar item por item na lista
            for produto in resposta['results']:
                lista.append(produto)

            # Eu recomendo colocar um tempo entre uma execução e outra
            # Fazer muitas requisições em um curto período não é legal
            # time.sleep(1)

    print(separador)
    # time.sleep(1)

    # Se a pasta arquivos não existir, ela será criada aqui
    if not os.path.exists(f'./arquivos/{id_do_vendedor}'):
        os.makedirs(f'./arquivos/{id_do_vendedor}')
        print('Pasta arquivos criada')
        print(separador)
        # time.sleep(1)

    if not os.path.exists(f'./arquivos/backup'):
        os.makedirs(f'./arquivos/backup')
        print('Pasta backup criada')
        print(separador)
        # time.sleep(1)

    # Aqui ele deleta os arquivos existentes
    # Caso o valor da variável seja True

    if deletar_existentes:
        if os.path.exists(f'./arquivos/{id_do_vendedor}/lista-{id_do_vendedor}.json'):
            os.remove(f'./arquivos/{id_do_vendedor}/lista-{id_do_vendedor}.json')

        if os.path.exists(f'./arquivos/backup-{id_do_vendedor}.txt'):
            os.remove(f'./arquivos/backup-{id_do_vendedor}.txt')
        print('Arquivos antigos deletados')
    else:
        print('Os arquivos serão substituídos')

    print(separador)

    with open(f'./arquivos/{id_do_vendedor}/lista-{id_do_vendedor}.json', 'w') as outfile:
        json.dump(lista, outfile)

    with open(f'./arquivos/backup/backup-{id_do_vendedor}.txt', 'w') as documento:
        for produto in lista:
            documento.write(f'{produto}\n')

    print('Programa finalizado')
    print(separador)


pegar_todos_produtos()

fim_timer = time.time()
tempo_total = fim_timer - inicio_timer
print(f"Tempo de execução: {tempo_total} segundos")
