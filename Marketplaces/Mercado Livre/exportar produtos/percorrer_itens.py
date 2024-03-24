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

    df['date_created'] = pd.to_datetime(df['date_created'], format='%d/%m/%Y %H:%M:%S')
    df['last_updated'] = pd.to_datetime(df['last_updated'], format='%d/%m/%Y %H:%M:%S')

    df = df.sort_values(by='last_updated', ascending=False)

    df.to_excel(planilha, index=False)
    mensagem(f'Planilha gerada')


def gerar_planilha():
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

            envio = body['shipping']['logistic_type']
            if envio == 'cross_docking':
                body['shipping'] = 'Normal'
            elif envio == 'fulfillment':
                body['shipping'] = 'Full'
            elif envio == 'not_specified':
                body['shipping'] = 'Não especificado'
            else:
                pass

            atributos = body['attributes']
            for atributo in atributos:
                if atributo['id'] == 'SELLER_SKU':
                    sku = atributo['values'][0]['name']
                    body['attributes'] = sku
                    break

                else:
                    body['attributes'] = ''

            if body['status'] == 'active':
                body['status'] = 'Ativo'

            elif body['status'] == 'paused':
                body['status'] = 'Pausado'

            elif body['status'] == 'closed':
                body['status'] = 'Fechado'

            elif body['status'] == 'under_review':
                body['status'] = 'Sob revisão'
            else:
                pass

            criado = body['date_created']
            atua = body['last_updated']
            '''
            criado_ano = criado[0:4]
            criado_mes = criado[5:7]
            criado_dia = criado[9:10]
            '''

            body['date_created'] = f'{criado[8:10]}/{criado[5:7]}/{criado[0:4]} {criado[11:19]}'
            body['last_updated'] = f'{atua[8:10]}/{atua[5:7]}/{atua[0:4]} {atua[11:19]}'

            porcentagem = body['health']
            try:
                float(porcentagem)
                body['health'] = f'{(float(porcentagem)) * 100}%'
            except:
                pass

            if body['catalog_listing'] == 'TRUE':
                body['catalog_listing'] = 'Verdadeiro'
            else:
                body['catalog_listing'] = 'Falso'

            if len(body['item_relations']) == 0:
                body['item_relations'] = 'Sem relação'
            else:
                body['item_relations'] = body['item_relations'][0]['id']

            if len(body['channels']) == 2:
                body['channels'] = 'Vendido em ambos canais'
            elif body['channels'][0] == 'marketplace':
                body['channels'] = 'Vendido apenas no Mercado Livre'
            elif body['channels'][0] == 'mshops':
                body['channels'] = 'Vendido apenas no Mercado Shops'
            else:
                pass

            lista_retorno.append(body)

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
        'deal_ids', 'automatic_relist', 'start_time', 'stop_time', 'end_time', 'expiration_time', 'condition',
        'seller_custom_field']

    exportar_para_planilha(lista_retorno, drops)

    # Fim do programa
    fim_timer = time.time()
    mensagem(f"Programa: Gerar arquivos finalizado | Tempo de execução: {fim_timer - inicio_timer} segundos")


if gerar_os_arquivos:
    gerar_planilha()
    path = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'
    path = os.path.realpath(path)
    os.startfile(path)
