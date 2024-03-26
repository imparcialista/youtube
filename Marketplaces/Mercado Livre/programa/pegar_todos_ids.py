import json
import os
import time
import requests

# from access_token import access_token

# TODO Criar uma interface visual para gerenciamento dos anúncios

# access_token = input(str('Access Token = '))

# Dica!
# Para pegar o id do vendedor de um access token
# Utilize: id_do_vendedor = access_token[-9:]
# id_do_vendedor = access_token[-9:]

# Recomendo que deixe esse como True
gerar_arquivos = True
apenas_itens_ativos = False
base = 'https://api.mercadolibre.com'
lista = []


def mensagem(texto):
    print(f'{"-" * (len(texto) + 4)}\n| {texto} |')


def ler_json(arquivo):
    arquivo_json = open(arquivo, encoding='UTF-8')
    data = json.load(arquivo_json)
    return data


def fazer_reqs(url, access):
    headers = {'Authorization': f'Bearer {access}'}
    resposta = requests.get(f'{url}', headers=headers)

    tentativa = 1
    while tentativa < 12:
        if resposta.status_code != 200:
            if tentativa == 11:
                mensagem('Número máximo de tentativas excedido')
                quit()
            else:
                mensagem(f'Tentativa {tentativa} | Falha na requisição')
                tentativa += 1
                time.sleep(0.25)

        else:
            resposta = resposta.json()
            return resposta


def pegar_scroll_id(access_token_value):
    id_do_vendedor = access_token_value[-9:]
    url = f'{base}/users/{id_do_vendedor}/items/search?search_type=scan&limit=100'
    resposta = fazer_reqs(url, access_token_value)
    return resposta


def proxima_pagina(scroll, access_token_value):
    id_do_vendedor = access_token_value[-9:]
    url = f'{base}/users/{id_do_vendedor}/items/search?search_type=scan&scroll_id={scroll}&limit=100'
    resposta = fazer_reqs(url, access_token_value)
    return resposta


def pegar_todos_ids(access_token_value):
    id_do_vendedor = access_token_value[-9:]

    nome = fazer_reqs(f'{base}/users/me', access_token_value)
    nome_da_conta = nome['nickname']

    mensagem(f'Conta conectada: {nome_da_conta}')
    inicio_timer = time.time()
    paginas = 0

    if apenas_itens_ativos:
        filtro = 'include_filters=true&status=active'
    else:
        filtro = ''

    url = f'{base}/users/{id_do_vendedor}/items/search?{filtro}&offset={0}'
    resposta = fazer_reqs(url, access_token_value)

    quantidade_de_an = resposta['paging']['total']

    if quantidade_de_an == 0:
        mensagem('Nenhum anúncio ativo\nPrograma finalizado')
        return

    if quantidade_de_an > 1000:
        mensagem(f'Quantidade de anúncios: {quantidade_de_an}')

        while quantidade_de_an > 0:
            quantidade_de_an -= 100
            paginas += 1

        mensagem(f'Páginas para percorrer: {paginas}')
        paginas = paginas - 1

        lista_scroll = []
        primeiro_scroll = pegar_scroll_id(access_token_value)
        mensagem(f'IDs coletados: {len(primeiro_scroll["results"])}')

        lista_scroll.append(primeiro_scroll['scroll_id'])
        for produto in primeiro_scroll['results']:
            lista.append(produto)


        def gerar_scroll(scroll_anterior):
            scroll = proxima_pagina(scroll_anterior, access_token_value)
            mensagem(f'IDs coletados: {len(scroll["results"])}')

            for id_mlb in scroll['results']:
                lista.append(id_mlb)

            lista_scroll.append(scroll['scroll_id'])


        for pagina in range(paginas):
            gerar_scroll(lista_scroll[pagina])

    else:
        quantidade_de_an = resposta['paging']['total']

        mensagem(f'Quantidade de anúncios: {quantidade_de_an}')

        while quantidade_de_an > 0:
            quantidade_de_an -= 50
            paginas += 1

        mensagem(f'Páginas para percorrer: {paginas}')

        for pagina in range(paginas):
            url = f'{base}/users/{id_do_vendedor}/items/search?{filtro}&offset={pagina * 50}'

            mensagem(f'Página: {pagina + 1} | Offset {pagina * 50}')

            resposta = fazer_reqs(url, access_token_value)

            for produto in resposta['results']:
                lista.append(produto)

    if gerar_arquivos:
        if not os.path.exists(f'Arquivos/{nome_da_conta}'):
            os.makedirs(f'Arquivos/{nome_da_conta}')
            mensagem(f'Pasta {nome_da_conta} criada')

        arquivo_json = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-ids_mlb.json'

        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)

        with open(arquivo_json, 'w') as outfile:
            json.dump(lista, outfile)

    fim_timer = time.time()
    mensagem(f'{nome_da_conta}: Todos os IDS foram coletados ')
    mensagem(f'Tempo de execução: {fim_timer - inicio_timer} segundos')

    return lista
