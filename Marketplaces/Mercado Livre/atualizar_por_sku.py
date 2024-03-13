import time
import requests
from chaves import access_token
from ferramentas import atualizar_estoque

inicio_timer = time.time()

id_do_vendedor = access_token[-9:]
offset = 0
lista = []
separador = '-' * 30


def fazer_reqs(pagina, seller_sku):
    url = (f'https://api.mercadolibre.com/users/'
           f'{id_do_vendedor}/items/search?seller_sku={seller_sku}&offset='
           f'{pagina}')

    payload = { }
    headers = { 'Authorization': f'Bearer {access_token}' }

    resposta = requests.request('GET', url, headers=headers, data=payload)

    if resposta.status_code != 200:
        print('Falha na requisição')
        resposta.raise_for_status()

    resposta = resposta.json()
    return resposta


def pegar_produtos(sku):
    paginas = 0
    resposta = fazer_reqs(0, sku)
    quantidade_de_an = resposta['paging']['total']

    if quantidade_de_an == 0:
        print(separador)
        print('Nenhum anúncio ativo')
        print('Programa finalizado')
        print(separador)
        return

    else:
        qtd_estoque = input('Digite o estoque para ser atualizado: ')
        qtd_estoque = int(qtd_estoque)

        resposta = fazer_reqs(0, sku)
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
            resposta = fazer_reqs(pagina * 50, sku)

            for produto in resposta['results']:
                lista.append(produto)
                atualizar_estoque(produto, qtd_estoque)


sair = False
while not sair:
    sku_produto = input('Digite o SKU: ')
    pegar_produtos(sku_produto)

fim_timer = time.time()
tempo_total = fim_timer - inicio_timer
print(f"Tempo de execução: {tempo_total} segundos")