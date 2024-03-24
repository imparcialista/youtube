import pandas as pd

from listar_todos_anuncios import *

# caso aconteça o erro ao tentar gerar o arquivo excel
# pip install openpyxl

# Gera uma planilha com todos os produtos da conta selecionada
gerar_os_arquivos = True
lista_retorno = []

ids_mlb = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-ids_mlb.json'
if not os.path.exists(ids_mlb):
    pegar_todos_produtos()


def exportar_para_planilha(lista_json: list, colunas_drop: list):
    arquivo_json = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-retorno-produtos.json'

    if os.path.exists(arquivo_json):
        os.remove(arquivo_json)
        mensagem('Arquivo JSON antigo deletado')

    with open(arquivo_json, 'w') as outfile:
        json.dump(lista_json, outfile)
        mensagem(f'Arquivo JSON criado')

    df = pd.read_json(arquivo_json)
    mensagem('Arquivo JSON carregado')

    df = df.drop(colunas_drop, axis=1, errors='ignore')
    mensagem(f'Colunas excluídas | {colunas_drop}')

    planilha = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'

    if os.path.exists(planilha):
        os.remove(planilha)

    df.to_excel(planilha, index=False)
    mensagem(f'Planilha gerada')


def gerar_arquivos():
    inicio_timer = time.time()
    mensagem(f'Conta conectada: {nome_da_conta}')
    lista_geral = []
    gap_vinte = 0
    paginas = 0

    # defina qual o json de retorno você vai utilizar

    df = pd.read_json(ids_mlb)
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

    for i_pack, pack in enumerate(lista_geral):
        mensagem(f'Indice: {i_pack} | Conteúdo: {pack}')
        url = f'https://api.mercadolibre.com/items?ids={pack}'
        retorno = fazer_reqs(url)

        for grupo_de_itens in retorno:
            body = grupo_de_itens['body']

            atributos = body['attributes']

            for atributo in atributos:
                if atributo['id'] == 'SELLER_SKU':
                    sku = atributo['values'][0]['name']
                    body['attributes'] = sku
                    break

                else:
                    body['attributes'] = ''

            lista_retorno.append(body)

    with open(f'Arquivos/{nome_da_conta}/{id_do_vendedor}-backup.txt', 'w') as documento_bkp:
        documento_bkp.write(f'{lista_retorno}\n')
        mensagem('Arquivo backup.txt gerado')

    drops = [
        'site_id', 'official_store_id', 'user_product_id', 'seller_id', 'category_id', 'inventory_id',
        'currency_id',
        'sale_terms', 'buying_mode', 'listing_type_id', 'start_time', 'stop_time', 'end_time', 'expiration_time',
        'thumbnail_id', 'pictures', 'video_id', 'descriptions', 'accepts_mercadopago',
        'non_mercado_pago_payment_methods',
        'international_delivery_mode', 'seller_address', 'seller_contact', 'location', 'geolocation',
        'coverage_areas',
        'warnings', 'listing_source', 'variations', 'sub_status', 'warranty', 'parent_item_id',
        'differential_pricing',
        'deal_ids', 'automatic_relist', 'start_time', 'stop_time', 'end_time', 'expiration_time']

    exportar_para_planilha(lista_retorno, drops)

    # Fim do programa
    fim_timer = time.time()
    mensagem(f"Programa: Gerar arquivos finalizado | Tempo de execução: {fim_timer - inicio_timer} segundos")


if gerar_os_arquivos:
    gerar_arquivos()
    path = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'
    path = os.path.realpath(path)
    os.startfile(path)
