import time
import requests
import json
import os
from chaves import access_token

# TODO Criar uma interface visual para gerenciamento dos anúncios

# Dica!
# Para pegar o id do vendedor de um access token
# Utilize: id_do_vendedor = access_token[-9:]
id_do_vendedor = access_token[-9:]

# Recomendo que deixe esse como True
gerar_arquivos = True
apenas_itens_ativos = False
base = 'https://api.mercadolibre.com'

lista = []


def mensagem(texto):
    print(f'{'-' * (len(texto) + 4)}\n| {texto} |')


def ler_json(arquivo):
    arquivo_json = open(arquivo, encoding='UTF-8')
    data = json.load(arquivo_json)
    return data


def fazer_reqs(url):
    headers = {'Authorization': f'Bearer {access_token}'}
    resposta = requests.get(f'{url}', headers=headers)

    if resposta.status_code != 200:
        mensagem('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    return resposta


nome = fazer_reqs(f'{base}/users/me')
nome_da_conta = nome['nickname']


def pegar_scroll_id():
    url = f'{base}/users/{id_do_vendedor}/items/search?search_type=scan&limit=100'
    resposta = fazer_reqs(url)
    return resposta


def proxima_pagina(scroll):
    url = f'{base}/users/{id_do_vendedor}/items/search?search_type=scan&scroll_id={scroll}&limit=100'
    resposta = fazer_reqs(url)
    return resposta


def pegar_todos_produtos():
    mensagem(f'Conta conectada: {nome_da_conta}')
    inicio_timer = time.time()
    paginas = 0

    if apenas_itens_ativos:
        filtro = 'include_filters=true&status=active'
    else:
        filtro = ''

    # Primeira requisição
    url = f'{base}/users/{id_do_vendedor}/items/search?{filtro}&offset={0}'
    resposta = fazer_reqs(url)

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
        primeiro_scroll = pegar_scroll_id()
        mensagem(f'IDs coletados: {len(primeiro_scroll["results"])}')

        lista_scroll.append(primeiro_scroll['scroll_id'])
        for produto in primeiro_scroll['results']:
            lista.append(produto)


        def gerar_scroll(scroll_anterior):
            scroll = proxima_pagina(scroll_anterior)
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

            resposta = fazer_reqs(url)

            # Aqui vem um resultado de 50 produtos
            # Então vamos adicionar item por item na lista
            for produto in resposta['results']:
                lista.append(produto)

            # Eu recomendo colocar um tempo entre uma execução e outra
            # Fazer muitas requisições em um curto período não é legal

    if gerar_arquivos:
        # Se a pasta arquivos não existir, ela será criada aqui
        if not os.path.exists(f'Arquivos/{nome_da_conta}'):
            os.makedirs(f'Arquivos/{nome_da_conta}')
            mensagem(f'Pasta {nome_da_conta} criada')

        # Aqui ele deleta os arquivos existentes
        # Caso o valor da variável seja True

        arquivo_json = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-ids_mlb.json'
        arquivo_txt = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-ids_mlb.txt'

        # Apagar arquivos
        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)

        if os.path.exists(arquivo_txt):
            os.remove(arquivo_txt)

        # mensagem('Arquivos antigos deletados')

        # Gerar arquivos
        with open(arquivo_json, 'w') as outfile:
            json.dump(lista, outfile)
            # mensagem(f'Arquivo JSON com todos os IDS da conta {id_do_vendedor} gerado')

        with open(arquivo_txt, 'w') as documento:
            for produto in lista:
                documento.write(f'{produto}\n')
            # mensagem(f'Arquivo TXT com todos os IDS da conta {id_do_vendedor} gerado')

    fim_timer = time.time()
    mensagem(f'{nome_da_conta}: Todos os IDS foram coletados ')
    mensagem(f'Tempo de execução: {fim_timer - inicio_timer} segundos')
    return lista
