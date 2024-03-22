import pandas as pd
from listar_todos_anuncios import *

# caso aconteça o erro ao tentar gerar o arquivo excel
# pip install openpyxl

pegar_produtos = True
gerar_os_arquivos = True

if pegar_produtos:
    lista_produtos = pegar_todos_produtos()
    mensagem(lista_produtos)
else:
    referencia = open('Arquivos/backup/backup-227116770.txt', 'r')
    ids_mlb_lista = []

    for linha in referencia:
        linha = linha.replace(f'\n', "")
        ids_mlb_lista.append(linha)

    for i, id_mlb in enumerate(ids_mlb_lista):
        mensagem(f'Posição: {i} | Valor: {id_mlb}')


def gerar_arquivos():
    inicio_timer = time.time()
    lista_geral = []
    gap_vinte = 0
    paginas = 0

    # defina qual o json de retorno você vai utilizar
    df = pd.read_json('Arquivos/227116770/lista-227116770.json')
    quantidade_de_an = len(df)

    mensagem(f'Quantidade de anúncios: {quantidade_de_an}')

    while quantidade_de_an > 0:
        quantidade_de_an -= 20
        paginas += 1

    mensagem(f'Páginas para percorrer: {paginas}')

    # with open(f'teste.txt', 'w') as documento:
    for pagina in range(paginas):
        inicio = gap_vinte
        fim = gap_vinte + 20
        itens = df[inicio:fim]
        lista_concatenada = ','.join(itens[0])
        lista_geral.append(lista_concatenada)
        gap_vinte += 20
        # documento.write(f'[{lista_concatenada}]\n')

    # for linha, item in enumerate(lista_geral):
    #     print(f'{linha} | Tamanho: {len(re.findall('MLB', item))} | {item} ')

    # print(lista_geral)
    # print(len(lista_geral))

    for inx, pack in enumerate(lista_geral):
        mensagem(f'Indice: {inx} | Conteúdo: {pack}')
        url = f'https://api.mercadolibre.com/items?ids={pack}'
        retorno = fazer_reqs(url)

        for grupo_de_itens in retorno:
            body = grupo_de_itens['body']
            lista.append(body)

    retorno = lista

    with open(f'backup.txt', 'w') as documento_bkp:
        documento_bkp.write(f'{lista_geral}\n')
        mensagem('Arquivo backup.txt gerado')

    with open(f'ids_mlb.json', 'w') as outfile:
        json.dump(retorno, outfile)
        mensagem('Arquivo ids_mlb.json gerado')

    df = pd.read_json('teste.json')
    mensagem('Arquivo JSON carregado')
    # print(df)

    drops = [
        'site_id', 'official_store_id', 'user_product_id', 'seller_id', 'category_id', 'inventory_id', 'currency_id',
        'sale_terms', 'buying_mode', 'listing_type_id', 'start_time', 'stop_time', 'end_time', 'expiration_time',
        'thumbnail_id', 'pictures', 'video_id', 'descriptions', 'accepts_mercadopago',
        'non_mercado_pago_payment_methods',
        'international_delivery_mode', 'seller_address', 'seller_contact', 'location', 'geolocation', 'coverage_areas',
        'warnings', 'listing_source', 'variations', 'sub_status', 'warranty', 'parent_item_id', 'differential_pricing',
        'deal_ids', 'automatic_relist', 'start_time', 'stop_time', 'end_time', 'expiration_time']

    df = df.drop(drops, axis=1, errors='ignore')
    mensagem(f'Colunas excluídas | {drops}')

    df.to_excel(f'teste.xlsx', index=False)
    mensagem('Arquivo teste.xlsx gerado')

    # Fim do programa
    fim_timer = time.time()
    mensagem(f"Programa: Gerar arquivos finalizado | Tempo de execução: {fim_timer - inicio_timer} segundos")


if gerar_os_arquivos:
    gerar_arquivos()
