import pandas as pd
import json
import time
from ferramentas import fazer_reqs

inicio_timer = time.time()

lista = []
lista_geral = []
gap_vinte = 0
paginas = 0

# defina qual o json de retorno você vai utilizar
df = pd.read_json('Arquivos/227116770/lista-227116770.json')
quantidade_de_an = len(df)

print(f'Quantidade de anúncios: {quantidade_de_an}')

while quantidade_de_an > 0:
    quantidade_de_an -= 20
    paginas += 1

print(f'Páginas para percorrer: {paginas}')

for pagina in range(paginas):
    inicio = gap_vinte
    fim = gap_vinte + 20
    itens = df[inicio:fim]
    lista_concatenada = ','.join(itens[0])
    lista_geral.append(lista_concatenada)
    gap_vinte += 20

for i, pack in enumerate(lista_geral):
    # print(f'Indice: {i} | Conteúdo: {pack}')
    url = f'https://api.mercadolibre.com/items?ids={pack}'
    retorno = fazer_reqs(url)

    for item in retorno:
        body = item['body']
        lista.append(body)
        # sku = item['body']['attributes'][9]
        # print('-' * 15)
        # print(item['body'])
        '''
        print(item['body']['attributes'][0])  # ['value_name'])
        print(item['body']['attributes'][1])  # ['value_name'])
        print(item['body']['attributes'][2])  # ['value_name'])
        print(item['body']['attributes'][3])  # ['value_name'])
        print(item['body']['attributes'][4])  # ['value_name'])
        print(item['body']['attributes'][5])  # ['value_name'])
        '''
        # print('-' * 15)
        # print(sku)

retorno = lista

with open(f'teste.json', 'w') as outfile:
    json.dump(retorno, outfile)

df = pd.read_json('teste.json')
# print(df)
drops = [
    'site_id', 'official_store_id', 'user_product_id', 'seller_id', 'category_id', 'inventory_id', 'currency_id',
    'sale_terms', 'buying_mode', 'listing_type_id', 'start_time', 'stop_time', 'end_time', 'expiration_time',
    'thumbnail_id', 'pictures', 'video_id', 'descriptions', 'accepts_mercadopago', 'non_mercado_pago_payment_methods',
    'international_delivery_mode', 'seller_address', 'seller_contact', 'location', 'geolocation', 'coverage_areas',
    'warnings', 'listing_source', 'variations', 'sub_status', 'warranty', 'parent_item_id', 'differential_pricing',
    'deal_ids', 'automatic_relist', 'start_time', 'stop_time', 'end_time', 'expiration_time']

df = df.drop(drops, axis=1, errors='ignore')

df.to_excel(f'teste.xlsx', index=False)

fim_timer = time.time()
tempo_total = fim_timer - inicio_timer
print(f"Tempo de execução: {tempo_total} segundos")