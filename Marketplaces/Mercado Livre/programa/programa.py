import json
import os
import time
import pandas as pd
from tkinter import filedialog as dlg
import requests
from termcolor import colored

os.system('color')


def main():
    os.system('CLS')
    apenas_itens_ativos = False
    base = 'https://api.mercadolibre.com'
    sair = False


    def mensagem(texto):
        texto = f'{"-" * (len(texto) + 4)}\n| {texto} |'
        print(colored(f'{texto}', 'light_cyan'))


    def mensagem_colorida(texto, cor):
        texto = f'{"-" * (len(texto) + 4)}\n| {texto} |'
        print(colored(f'{texto}', cor))


    def print_colorido(texto):
        print(colored(f'{texto}', 'light_cyan'))


    def fazer_reqs(url, access_token_value):
        headers = {'Authorization': f'Bearer {access_token_value}'}
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


    def configurar_conta():
        conta_configurada = False
        while not conta_configurada:
            access_token_value = input(str('\nInsira o Access Token = '))

            headers = {'Authorization': f'Bearer {access_token_value}'}
            resposta = requests.get(f'https://api.mercadolibre.com/users/me', headers=headers)

            if resposta.status_code == 200:
                os.system('CLS')
                return access_token_value

            else:
                print_colorido('Access Token inválido ou expirado')


    def pegar_nome_da_conta(access_token_value):
        nome_retorno = fazer_reqs(f'{base}/users/me', access_token_value)
        nome_conta = nome_retorno['nickname']
        return nome_conta


    def pegar_scroll_id(access_token_value):
        url = f'{base}/users/{(access_token_value[-9:])}/items/search?search_type=scan&limit=100'
        resposta = fazer_reqs(url, access_token_value)
        return resposta


    def proxima_pagina(scroll, access_token_value):
        url = f'{base}/users/{(access_token_value[-9:])}/items/search?search_type=scan&scroll_id={scroll}&limit=100'
        resposta = fazer_reqs(url, access_token_value)
        return resposta


    def pegar_todos_ids(access_token_value):
        mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token_value))}')
        lista = []
        inicio_timer = time.time()
        paginas = 0

        if apenas_itens_ativos:
            filtro = 'include_filters=true&status=active'
        else:
            filtro = ''

        url = f'{base}/users/{(access_token_value[-9:])}/items/search?{filtro}&offset={0}'
        resposta = fazer_reqs(url, access_token_value)

        quantidade_de_an = resposta['paging']['total']

        if quantidade_de_an == 0:
            mensagem('Nenhum anúncio ativo. Programa finalizado')
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
            mensagem('Coletando IDs, por favor aguarde...')

            lista_scroll.append(primeiro_scroll['scroll_id'])
            for produto in primeiro_scroll['results']:
                lista.append(produto)


            def gerar_scroll(scroll_anterior):
                scroll = proxima_pagina(scroll_anterior, access_token_value)

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
                url = f'{base}/users/{(access_token_value[-9:])}/items/search?{filtro}&offset={pagina * 50}'

                mensagem(f'Página: {pagina + 1} | Offset {pagina * 50}')

                resposta = fazer_reqs(url, access_token_value)

                for produto in resposta['results']:
                    lista.append(produto)

        if not os.path.exists(f'Arquivos/{pegar_nome_da_conta(access_token)}'):
            os.makedirs(f'Arquivos/{pegar_nome_da_conta(access_token)}')
            mensagem(f'Pasta {pegar_nome_da_conta(access_token)} criada')

        arquivo_json = f'Arquivos/{pegar_nome_da_conta(access_token)}/{(access_token_value[-9:])}-ids_mlb.json'

        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)

        with open(arquivo_json, 'w') as outfile:
            json.dump(lista, outfile)

        fim_timer = time.time()
        mensagem(f'{pegar_nome_da_conta(access_token)}: Todos os IDS foram coletados ')
        mensagem(f'Tempo de execução: {fim_timer - inicio_timer} segundos')

        return lista


    def exportar_para_planilha(lista_json: list, colunas_drop: list, access_token_value):
        arquivo_json = (f'Arquivos/{(pegar_nome_da_conta(access_token_value))}/{(access_token_value[-9:])}'
                        f'-retorno-produtos.json')

        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)

        with open(arquivo_json, 'w') as outfile:
            json.dump(lista_json, outfile)

        df = pd.read_json(arquivo_json)
        df = df.drop(colunas_drop, axis=1, errors='ignore')
        planilha = (f'Arquivos/{pegar_nome_da_conta(access_token_value)}/'
                    f'{(access_token_value[-9:])}-planilha-produtos.xlsx')

        if os.path.exists(planilha):
            os.remove(planilha)

        df['date_created'] = pd.to_datetime(df['date_created'], format='%d/%m/%Y %H:%M:%S')
        df['last_updated'] = pd.to_datetime(df['last_updated'], format='%d/%m/%Y %H:%M:%S')
        df = df.sort_values(by='last_updated', ascending=False)
        df.to_excel(planilha, index=False)
        mensagem(f'Planilha gerada')


    def gerar_planilha(access_token_value):
        ids_mlb = f'Arquivos/{pegar_nome_da_conta(access_token_value)}/{(access_token_value[-9:])}-ids_mlb.json'
        lista_retorno = []
        lista_geral = []
        gap_vinte = 0
        paginas = 0

        if not os.path.exists(ids_mlb):
            pegar_todos_ids(access_token_value)

        inicio_timer = time.time()

        df = pd.read_json(ids_mlb)
        quantidade_de_an = len(df)

        mensagem(f'Quantidade de anúncios: {quantidade_de_an}')

        while quantidade_de_an > 0:
            quantidade_de_an -= 20
            paginas += 1

        mensagem(f'Páginas para percorrer: {paginas}')

        for pagina in range(paginas):
            inicio = gap_vinte
            fim = gap_vinte + 20
            itens = df[inicio:fim]
            lista_concatenada = ','.join(itens[0])
            lista_geral.append(lista_concatenada)
            gap_vinte += 20

        for i_pack, pack in enumerate(lista_geral):
            mensagem(f'Página: {i_pack + 1} de {paginas}')
            url = f'https://api.mercadolibre.com/items?ids={pack}'
            retorno = fazer_reqs(url, access_token_value)

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

        exportar_para_planilha(lista_retorno, drops, access_token_value)
        fim_timer = time.time()
        mensagem(f"Programa: Atualizar planilha finalizado | Tempo de execução: {fim_timer - inicio_timer} segundos")


    def atualizar(produto, valor_atualizar, access_token_value):
        url = f'{base}/items/{produto}'
        info_produto = fazer_reqs(url, access_token_value)
        est_produto = info_produto['available_quantity']

        prc_produto = info_produto['price']
        org_prc_produto = info_produto['original_price']

        tit_produto = info_produto['title']

        envio = info_produto['shipping']['logistic_type']

        if envio == 'cross_docking':
            info_produto['shipping'] = 'Normal'

        elif envio == 'fulfillment':
            info_produto['shipping'] = 'Full'

        elif envio == 'not_specified':
            info_produto['shipping'] = 'Não especificado'

        else:
            pass

        if type(valor_atualizar) is int:
            if info_produto['shipping'] == 'Full':
                retorno = f'{produto} | Produto Full: Não alterar | {tit_produto}'
                txt_resposta = f'{retorno}'
                return txt_resposta

            if valor_atualizar == est_produto:
                retorno = f'{produto} | Estoque já está correto | {tit_produto}'
                txt_resposta = f'{retorno}'
                return txt_resposta

            if valor_atualizar > 0:
                payload = json.dumps({"available_quantity": valor_atualizar, "status": "active"})

            else:
                payload = json.dumps({"available_quantity": valor_atualizar})

        else:

            if valor_atualizar == prc_produto:
                retorno = f'{produto} | Preço já está correto | {tit_produto}'
                txt_resposta = f'{retorno}'
                return txt_resposta

            org_prc_produto = str(org_prc_produto)

            if org_prc_produto == 'None' or org_prc_produto == 'Null':
                payload = json.dumps({"price": valor_atualizar})

            else:

                prc_produto = str(prc_produto)
                prc_produto = prc_produto.replace('.', ',')

                org_prc_produto = str(org_prc_produto)
                org_prc_produto = org_prc_produto.replace('.', ',')

                retorno = (f'{produto} | Desconto ativo de R$ {org_prc_produto} por R$ {prc_produto} |'
                           f' {tit_produto}')

                txt_resposta = f'{retorno}'
                return txt_resposta

        headers = {"Authorization": f"Bearer {access_token_value}"}
        resposta = requests.put(url=url, headers=headers, data=payload)

        if resposta.status_code != 200:
            retorno = f'{produto} | Não pôde ser alterado'
            txt_resposta = f'{retorno}'

        else:
            if type(valor_atualizar) is int:
                retorno = f'{produto} | Estoque alterado de {est_produto} para {valor_atualizar} | {tit_produto}'

            else:
                valor_atualizar = str(valor_atualizar)
                valor_imprimir = valor_atualizar.replace('.', ',')
                prc_produto = str(prc_produto)
                prc_produto = prc_produto.replace('.', ',')
                retorno = f'{produto} | Preço alterado de R$ {prc_produto} para R$ {valor_imprimir} | {tit_produto}'

            txt_resposta = f'{retorno}'

        return txt_resposta


    def pegar_produtos(sku, valor_atualizar, access_token_value):
        paginas = 0
        url = f"{base}/users/{(access_token_value[-9:])}/items/search?seller_sku={sku}&offset={paginas}"

        resposta = fazer_reqs(url, access_token_value)
        quantidade_de_an = resposta['paging']['total']

        if quantidade_de_an != 0:

            if quantidade_de_an <= 50:
                for produto in resposta['results']:
                    escrever = atualizar(produto, valor_atualizar, access_token_value)

                    mensagem(escrever)

            else:

                while quantidade_de_an > 0:
                    quantidade_de_an -= 50
                    paginas += 1

                for pagina in range(paginas):
                    url = (f"{base}/users/{(access_token_value[-9:])}"
                           f"/items/search?seller_sku={sku}&offset={(pagina * 50)}")

                    resposta = fazer_reqs(url, access_token_value)

                    for produto in resposta['results']:
                        escrever = atualizar(produto, valor_atualizar, access_token_value)
                        mensagem(escrever)

        else:
            mensagem('Nenhum anúncio encontrado')


    def get_input():
        input_user = input(str('> '))
        input_user = input_user.lower()
        input_user = input_user.strip()
        return input_user


    def get_input_mlb():
        input_user = input(str('> '))
        input_user = input_user.strip()
        return input_user


    mensagem_base = (
        '\n[*] Escolha uma das opções, número ou comando'
        '\n[1] Atualizar planilha | Gera uma nova planilha com todos os produtos'
        '\n[2] Atualizar ids | Busca e atualiza a lista de IDS do Mercado Livre'
        '\n[3] Trocar de conta | Altere a conta conectada alterando o Access Token'
        '\n[4] Abrir planilha | Abre a planilha de produtos da conta selecionada'
        '\n[5] Atualizador | Programa para atualizar estoque ou preço por SKU'
        '\n[6] Atualizar por planilha | Escolha uma planilha para atualizar o estoque'
        '\n')

    mensagem('Programa feito por @imparcialista  v0.5')
    access_token = configurar_conta()
    mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
    mensagem('Digite SAIR para encerrar o programa')
    print_colorido(mensagem_base)

    while not sair:
        escolha = get_input()

        if escolha == 'sair':
            mensagem('Encerrando o programa...')
            break

        elif escolha == '?' or escolha == 'ajuda':
            print_colorido('\nDigite SAIR para encerrar o programa')

            mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
            print_colorido(mensagem_base)

        elif escolha == '1' or escolha == 'atualizar planilha':
            gerar_planilha(access_token)

            mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
            print_colorido(mensagem_base)

        elif escolha == '2' or escolha == 'atualizar ids':
            pegar_todos_ids(access_token)

            mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
            print_colorido(mensagem_base)

        elif escolha == '3' or escolha == 'trocar de conta':
            access_token = configurar_conta()

            mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
            print_colorido(mensagem_base)

        elif escolha == '4' or escolha == 'abrir planilha':
            path = f'Arquivos/{(pegar_nome_da_conta(access_token))}/{(access_token[-9:])}-planilha-produtos.xlsx'
            path = os.path.realpath(path)

            if not os.path.exists(path):
                mensagem('A planilha ainda não existe, gerando a planilha...')
                gerar_planilha(access_token)

            mensagem('Abrindo o arquivo...')
            os.startfile(path)
            mensagem('Arquivo aberto')

            mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
            print_colorido(mensagem_base)

        elif escolha == '5' or escolha == 'atualizador':
            atualizar_info = True
            while atualizar_info:
                print_colorido('\n[Digite VOLTAR para retornar ao menu anterior]')
                mensagem('O que você deseja atualizar?')
                mensagem('[1] Estoque | [2] Preço')
                tipo_desejado = get_input()
                if tipo_desejado == 'voltar':
                    break

                if tipo_desejado == '1' or tipo_desejado == '2':

                    if tipo_desejado == '1':
                        atualizar_est = True

                        while atualizar_est:
                            print_colorido('\n[Digite VOLTAR para retornar ao menu anterior]')
                            mensagem('Qual SKU você deseja atualizar o estoque?')
                            sku_escolhido = get_input_mlb()
                            voltar = sku_escolhido.lower()
                            if voltar == 'voltar':
                                atualizar_est = False

                            else:
                                valor_para_atualizar = input('Para qual quantidade você deseja atualizar?\n> ')

                                try:
                                    valor_para_atualizar = int(valor_para_atualizar)

                                except:
                                    mensagem_colorida('[ERRO: Insira apenas números inteiros]', 'red')
                                    break

                                mensagem(f'(SOLICITAÇÃO DE ALTERAÇÃO)')
                                mensagem(f'SKU: {sku_escolhido} | Estoque: {valor_para_atualizar}')

                                pegar_produtos(sku_escolhido, valor_para_atualizar, access_token)

                    else:
                        atualizar_prc = True

                        while atualizar_prc:
                            print_colorido('\n[Digite VOLTAR para retornar ao menu anterior]')
                            mensagem('Qual SKU você deseja atualizar o preço?')
                            sku_escolhido = get_input()

                            if sku_escolhido == 'voltar':
                                print_colorido('Você escolheu voltar')
                                atualizar_prc = False

                            else:
                                valor_para_atualizar = input(str('Para qual preço você deseja atualizar?\n> '))
                                valor_para_atualizar = valor_para_atualizar.replace('.', '')

                                mensagem(f'(SOLICITAÇÃO DE ALTERAÇÃO)')
                                mensagem(f'SKU: {sku_escolhido} | Preço: R$ {valor_para_atualizar}')
                                valor_para_atualizar = valor_para_atualizar.replace(',', '.')

                                pegar_produtos(sku_escolhido, valor_para_atualizar, access_token)

                else:
                    mensagem_colorida('Opção inválida, digite apenas 1 ou 2', 'red')

            mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
            print_colorido(mensagem_base)

        elif escolha == '6' or escolha == 'atualizar por planilha':
            planilha_atualizar = dlg.askopenfilename(filetypes=[("Arquivos excel", ".xlsx")])

            if planilha_atualizar == '':
                mensagem_colorida('Você não selecionou nenhum arquivo', 'red')
                mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
                print_colorido(mensagem_base)

            else:
                print()
                mensagem(f'Caminho do arquivo: {planilha_atualizar}')
                df_atualizar = pd.read_excel(planilha_atualizar)

                lista_sku = []
                valor_trocar = []

                planilha_prc = False

                if df_atualizar.columns[0] == 'SKU':
                    for sku_df in df_atualizar['SKU']:
                        lista_sku.append(sku_df)
                        
                    if df_atualizar.columns[1] == 'EST':
                        mensagem('Modo atualizar estoque por planilha selecionado')
                        mensagem_colorida('ATENÇÃO: Produtos que estão oferecendo '
                                          'Full não serão alterados', 'red')

                        for est_df in df_atualizar['EST']:
                            valor_trocar.append(est_df)
                        
                    elif df_atualizar.columns[1] == 'PRC':
                        mensagem('Modo atualizar preço por planilha selecionado')
                        mensagem_colorida('ATENÇÃO: Produtos com promoção ativa não serão alterados para '
                                          'não sair da promoção', 'red')
                        planilha_prc = True

                        for prc_df in df_atualizar['PRC']:
                            valor_trocar.append(prc_df)

                    else:
                        mensagem_colorida('A planilha não segue um padrão para que seja atualizado', 'red')
                        mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
                        print_colorido(mensagem_base)
                        continue

                else:
                    mensagem_colorida('A planilha não segue um padrão para que seja atualizado', 'red')
                    mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
                    print_colorido(mensagem_base)
                    continue

                continuar = input(str(f'\n{len(df_atualizar['SKU'])} SKUs para atualizar'
                                      f'\nDeseja continuar?'
                                      f'\n[1] Sim | [2] Não'
                                      f'\n> '))

                if continuar == '1':

                    sku_disp = []
                    sku_nao_disp = []

                    for inx_sku, lista_sku_value in enumerate(lista_sku):

                        sku_mlb = str(lista_sku[inx_sku])
                        valor_mlb = valor_trocar[inx_sku]

                        if not planilha_prc:
                            valor_mlb = int(valor_mlb)

                        url_df = (f"{base}/users/{(access_token[-9:])}/items/search?seller_sku="
                                  f"{sku_mlb}&offset={0}")

                        resposta_df = fazer_reqs(url_df, access_token)
                        qtd_de_an = resposta_df['paging']['total']
                        print()

                        if qtd_de_an > 0:
                            # time.sleep(0.25)
                            base_print = f'SKU: {sku_mlb} | {qtd_de_an} Anúncio'

                            if planilha_prc:
                                valor_imprimir_novo = str(valor_mlb)
                                valor_imprimir_novo.replace('.',  ',')
                                complemento = f'Preço: R$ {valor_imprimir_novo}'

                            else:
                                complemento = f'Estoque: {valor_mlb}'

                            if qtd_de_an == 1:
                                mensagem(f'{base_print} | {complemento}')

                            else:
                                mensagem(f'{base_print}s | {complemento}')

                            sku_disp.append(sku_mlb)

                            pegar_produtos(sku_mlb, valor_mlb, access_token)

                        else:
                            mensagem_colorida(f'SKU: {sku_mlb} | Nenhum anúncio encontrado', 'red')
                            sku_nao_disp.append(sku_mlb)

                    print_colorido(f'\nSKUs encontrados: {sku_disp}')
                    print_colorido(f'\nSKUs não encontrados: {sku_nao_disp}\n')

                elif continuar == '2':
                    mensagem_colorida('Você escolheu não continuar', 'red')

                else:
                    mensagem_colorida('Opção inválida', 'red')
                    pass

                mensagem(f'Conta conectada: {(pegar_nome_da_conta(access_token))}')
                print_colorido(mensagem_base)

        else:
            print()
            mensagem_colorida('[X] Opção inválida | Escolha uma das opções', 'red')
            mensagem(f'Conta conectada: {pegar_nome_da_conta(access_token)}')
            print_colorido(mensagem_base)


if __name__ == "__main__":
    main()
