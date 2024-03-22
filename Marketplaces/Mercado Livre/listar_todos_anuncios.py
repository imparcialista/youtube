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
deletar_existentes = True
gerar_arquivos = False
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
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    return resposta


def pegar_scroll_id():
    url = f'{base}/users/{id_do_vendedor}/items/search?search_type=scan&limit=100'
    resposta = fazer_reqs(url)
    return resposta


def proxima_pagina(scroll):
    url = f'{base}/users/{id_do_vendedor}/items/search?search_type=scan&scroll_id={scroll}&limit=100'
    resposta = fazer_reqs(url)
    return resposta


def pegar_todos_produtos():
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
        print(f'IDs coletados: {len(primeiro_scroll["results"])}')

        lista_scroll.append(primeiro_scroll['scroll_id'])
        for produto in primeiro_scroll['results']:
            lista.append(produto)


        def gerar_scroll(scroll_anterior):
            scroll = proxima_pagina(scroll_anterior)
            print(f'IDs coletados: {len(scroll["results"])}')

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

        # time.sleep(3)

        for pagina in range(paginas):
            url = f'{base}/users/{id_do_vendedor}/items/search?{filtro}&offset={pagina * 50}'

            print(f'Página: {pagina + 1} | Offset {pagina * 50}')

            resposta = fazer_reqs(url)

            # Aqui vem um resultado de 50 produtos
            # Então vamos adicionar item por item na lista
            for produto in resposta['results']:
                lista.append(produto)

            # Eu recomendo colocar um tempo entre uma execução e outra
            # Fazer muitas requisições em um curto período não é legal

    if gerar_arquivos:
        # Se a pasta arquivos não existir, ela será criada aqui
        if not os.path.exists(f'./arquivos/{id_do_vendedor}'):
            os.makedirs(f'./arquivos/{id_do_vendedor}')
            mensagem('Pasta arquivos criada')

        if not os.path.exists(f'./arquivos/backup'):
            os.makedirs(f'./arquivos/backup')
            mensagem('Pasta backup criada')

        # Aqui ele deleta os arquivos existentes
        # Caso o valor da variável seja True

        # Apagar arquivos
        if deletar_existentes:
            if os.path.exists(f'./arquivos/{id_do_vendedor}/lista-{id_do_vendedor}.json'):
                os.remove(f'./arquivos/{id_do_vendedor}/lista-{id_do_vendedor}.json')

            if os.path.exists(f'./arquivos/backup-{id_do_vendedor}.txt'):
                os.remove(f'./arquivos/backup-{id_do_vendedor}.txt')
            mensagem('Arquivos antigos deletados')
        else:
            mensagem('Os arquivos serão substituídos')

        # Gerar arquivos
        with open(f'./arquivos/{id_do_vendedor}/lista-{id_do_vendedor}.json', 'w') as outfile:
            json.dump(lista, outfile)
            mensagem('Arquivo JSON gerado')

        with open(f'./arquivos/backup/backup-{id_do_vendedor}.txt', 'w') as documento:
            for produto in lista:
                documento.write(f'{produto}\n')
            mensagem('Arquivo TXT gerado')

    fim_timer = time.time()
    mensagem(f"Programa: Pegar produtos finalizado | Tempo de execução: {fim_timer - inicio_timer} segundos")
    return lista
