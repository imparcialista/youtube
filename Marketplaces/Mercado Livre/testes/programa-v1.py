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


    def msg_dif(cor, lugar, mensagem):

        linha = f'{"-" * (len(mensagem))}\n'

        texto = f'{mensagem}'

        if lugar == 'cima':
            print(colored(f'{linha}{texto}', cor))

        elif lugar == 'baixo':
            print(colored(f'{texto}{linha}', cor))

        elif lugar == 'ambos':
            print(colored(f'{linha}{texto}\n{linha}', cor))

        else:
            print(colored(f'{texto}', cor))


    def msg(mensagem):
        msg_dif('white', '', f'{mensagem}')


    def msg_cima(mensagem):
        msg_dif('white', 'cima', f'{mensagem}')


    def msg_aviso(mensagem):
        msg_dif('yellow', '', f'{mensagem}')


    def msg_alerta(mensagem):
        msg_dif('yellow', '', f'{mensagem}')


    def msg_destaque(mensagem):
        msg_dif('green', 'ambos', f'{mensagem}')


    def fazer_reqs(url, token_value):
        headers = {'Authorization': f'Bearer {token_value}'}
        resposta = requests.get(f'{url}', headers=headers)

        tentativa = 1
        while tentativa < 12:
            if resposta.status_code != 200:
                if tentativa == 11:
                    msg_alerta('Número máximo de tentativas excedido')
                    quit()

                else:
                    msg_aviso(f'Tentativa {tentativa} | Falha na requisição')
                    tentativa += 1
                    time.sleep(0.25)

            else:
                resposta = resposta.json()
                return resposta


    def configurar_conta():
        conta_configurada = False
        while not conta_configurada:
            msg_cima('Insira o Access Token')
            token_value = input(str('> '))

            headers = {'Authorization': f'Bearer {token_value}'}
            resposta = requests.get(f'https://api.mercadolibre.com/users/me', headers=headers)

            if resposta.status_code == 200:
                os.system('CLS')
                return token_value

            else:
                msg_aviso('Access Token inválido ou expirado')


    def nome_conta(token_value):
        nome_retorno = fazer_reqs(f'{base}/users/me', token_value)
        conta = nome_retorno['nickname']
        return conta


    def pegar_scroll_id(token_value):
        url = f'{base}/users/{(token_value[-9:])}/items/search?search_type=scan&limit=100'
        resposta = fazer_reqs(url, token_value)
        return resposta


    def proxima_pagina(scroll, token_value):
        url = f'{base}/users/{(token_value[-9:])}/items/search?search_type=scan&scroll_id={scroll}&limit=100'
        resposta = fazer_reqs(url, token_value)
        return resposta


    def pegar_todos_ids(token_value):
        msg_destaque(f'Conta conectada: {(nome_conta(token_value))}')
        lista = []
        inicio_timer = time.time()
        paginas = 0

        if apenas_itens_ativos:
            filtro = 'include_filters=true&status=active'
        else:
            filtro = ''

        url = f'{base}/users/{(token_value[-9:])}/items/search?{filtro}&offset={0}'
        resposta = fazer_reqs(url, token_value)

        quantidade_de_an = resposta['paging']['total']

        if quantidade_de_an == 0:
            msg_cima('Nenhum anúncio ativo. Programa finalizado')
            return

        if quantidade_de_an > 1000:
            msg_cima(f'Quantidade de anúncios: {quantidade_de_an}')

            while quantidade_de_an > 0:
                quantidade_de_an -= 100
                paginas += 1

            msg_cima(f'Páginas para percorrer: {paginas}')
            paginas = paginas - 1

            lista_scroll = []
            primeiro_scroll = pegar_scroll_id(token_value)
            msg_cima('Coletando IDs, por favor aguarde...')

            lista_scroll.append(primeiro_scroll['scroll_id'])
            for produto in primeiro_scroll['results']:
                lista.append(produto)


            def gerar_scroll(scroll_anterior):
                scroll = proxima_pagina(scroll_anterior, token_value)

                for id_mlb in scroll['results']:
                    lista.append(id_mlb)

                lista_scroll.append(scroll['scroll_id'])


            for pagina in range(paginas):
                gerar_scroll(lista_scroll[pagina])

        else:
            quantidade_de_an = resposta['paging']['total']

            msg_cima(f'Quantidade de anúncios: {quantidade_de_an}')

            while quantidade_de_an > 0:
                quantidade_de_an -= 50
                paginas += 1

            msg_cima(f'Páginas para percorrer: {paginas}')

            for pagina in range(paginas):
                url = f'{base}/users/{(token_value[-9:])}/items/search?{filtro}&offset={pagina * 50}'

                # msg_cima(f'Página: {pagina + 1} | Offset {pagina * 50}')

                resposta = fazer_reqs(url, token_value)

                for produto in resposta['results']:
                    lista.append(produto)

        if not os.path.exists(f'Arquivos/{nome_conta(token)}'):
            os.makedirs(f'Arquivos/{nome_conta(token)}')
            msg_cima(f'Pasta {nome_conta(token)} criada')

        arquivo_json = f'Arquivos/{nome_conta(token)}/{(token_value[-9:])}-ids_mlb.json'

        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)

        with open(arquivo_json, 'w') as outfile:
            json.dump(lista, outfile)

        fim_timer = time.time()
        msg_cima(f'{nome_conta(token)}: Todos os IDS foram coletados ')
        msg_cima(f'Tempo de execução: {fim_timer - inicio_timer} segundos')

        return lista


    def exportar_para_planilha(lista_json: list, colunas_drop: list, token_value):
        arquivo_json = (f'Arquivos/{(nome_conta(token_value))}/{(token_value[-9:])}'
                        f'-retorno-produtos.json')

        if os.path.exists(arquivo_json):
            os.remove(arquivo_json)

        with open(arquivo_json, 'w') as outfile:
            json.dump(lista_json, outfile)

        df = pd.read_json(arquivo_json)
        df = df.drop(colunas_drop, axis=1, errors='ignore')
        planilha = (f'Arquivos/{nome_conta(token_value)}/'
                    f'{(token_value[-9:])}-planilha-produtos.xlsx')

        if os.path.exists(planilha):
            os.remove(planilha)

        df['date_created'] = pd.to_datetime(df['date_created'], format='%d/%m/%Y %H:%M:%S')
        df['last_updated'] = pd.to_datetime(df['last_updated'], format='%d/%m/%Y %H:%M:%S')

        df = df.sort_values(by='last_updated', ascending=False)
        df.to_excel(planilha, index=False)

        msg(f'Planilha gerada')


    def gerar_planilha(token_value):
        ids_mlb = f'Arquivos/{nome_conta(token_value)}/{(token_value[-9:])}-ids_mlb.json'
        lista_retorno = []
        lista_geral = []
        gap_vinte = 0
        paginas = 0

        if not os.path.exists(ids_mlb):
            pegar_todos_ids(token_value)

        inicio_timer = time.time()

        df = pd.read_json(ids_mlb)
        quantidade_de_an = len(df)

        msg_cima(f'Quantidade de anúncios: {quantidade_de_an}')

        while quantidade_de_an > 0:
            quantidade_de_an -= 20
            paginas += 1

        msg_cima(f'Páginas para percorrer: {paginas}')

        for pagina in range(paginas):
            inicio = gap_vinte
            fim = gap_vinte + 20
            itens = df[inicio:fim]
            lista_concatenada = ','.join(itens[0])
            lista_geral.append(lista_concatenada)
            gap_vinte += 20

        msg(f'Por favor aguarde | Tempo aproximado {(0.38 * paginas)+1} segundos')

        for i_pack, pack in enumerate(lista_geral):

            url = f'https://api.mercadolibre.com/items?ids={pack}'
            retorno = fazer_reqs(url, token_value)

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

        fim_timer = time.time()
        msg(f"Informações coletadas. Tempo de execução: {fim_timer - inicio_timer} segundos")

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

        exportar_para_planilha(lista_retorno, drops, token_value)


    def atualizar(produto, valor_atualizar, token_value):
        url = f'{base}/items/{produto}'
        info_prd = fazer_reqs(url, token_value)
        est_prd = info_prd['available_quantity']

        prc_prd = info_prd['price']
        prc_org_prd = info_prd['original_price']

        tit_produto = info_prd['title']

        envio = info_prd['shipping']['logistic_type']

        if envio == 'cross_docking':
            info_prd['shipping'] = 'Normal'

        elif envio == 'fulfillment':
            info_prd['shipping'] = 'Full'

        elif envio == 'not_specified':
            info_prd['shipping'] = 'Não especificado'

        else:
            pass

        if type(valor_atualizar) is int:
            if info_prd['shipping'] == 'Full':
                msg_dif('yellow', 'cima', f'{produto} | Produto Full: Não alterar | {tit_produto}')
                return

            if valor_atualizar == est_prd:
                msg_dif('green', 'cima', f'{produto} | Estoque já está correto | {tit_produto}')
                return

            if valor_atualizar > 0:
                payload = json.dumps({"available_quantity": valor_atualizar, "status": "active"})

            else:
                payload = json.dumps({"available_quantity": valor_atualizar})

        else:

            if valor_atualizar == prc_prd:
                msg_dif('green', 'cima', f'{produto} | Preço já está correto | {tit_produto}')
                return

            prc_org_prd = str(prc_org_prd)

            if prc_org_prd == 'None' or prc_org_prd == 'Null':
                payload = json.dumps({"price": valor_atualizar})

            else:

                prc_prd = str(prc_prd)
                prc_prd = prc_prd.replace('.', ',')

                prc_org_prd = str(prc_org_prd)
                prc_org_prd = prc_org_prd.replace('.', ',')

                msg_dif('green', 'cima', f'{produto} | Desconto ativo de R$ {prc_org_prd} '
                                         f'por R$ {prc_prd} | {tit_produto}')
                return

        headers = {"Authorization": f"Bearer {token_value}"}
        resposta = requests.put(url=url, headers=headers, data=payload)

        if resposta.status_code != 200:
            msg_dif('red', 'cima', f'{produto} | Não pôde ser alterado')

        else:
            if type(valor_atualizar) is int:
                msg_dif('green', 'cima',
                        f'{produto} | Estoque alterado de {est_prd} para {valor_atualizar} | {tit_produto}')

            else:
                valor_atualizar = str(valor_atualizar)
                valor_imprimir = valor_atualizar.replace('.', ',')

                prc_prd = str(prc_prd)
                prc_prd = prc_prd.replace('.', ',')

                msg_dif('green', 'cima',
                        f'{produto} | Preço alterado de R$ {prc_prd} '
                        f'para R$ {valor_imprimir} | {tit_produto}')


    def pegar_produtos(sku, valor_atualizar, token_value):
        paginas = 0
        url = f"{base}/users/{(token_value[-9:])}/items/search?seller_sku={sku}&offset={paginas}"

        resposta = fazer_reqs(url, token_value)
        quantidade_de_an = resposta['paging']['total']

        if quantidade_de_an != 0:

            if quantidade_de_an <= 50:
                for produto in resposta['results']:
                    atualizar(produto, valor_atualizar, token_value)

            else:

                while quantidade_de_an > 0:
                    quantidade_de_an -= 50
                    paginas += 1

                for pagina in range(paginas):
                    url = (f"{base}/users/{(token_value[-9:])}"
                           f"/items/search?seller_sku={sku}&offset={(pagina * 50)}")

                    resposta = fazer_reqs(url, token_value)

                    for produto in resposta['results']:
                        atualizar(produto, valor_atualizar, token_value)

        else:
            msg_dif('red', 'cima', 'Nenhum anúncio encontrado')


    def get_input():
        input_user = input(str('> '))
        input_user = input_user.lower()
        input_user = input_user.strip()
        return input_user

    mensagem_base = (
        '\n[*] Escolha uma das opções'
        '\n[1] Atualizar planilha'
        '\n[2] Atualizar lista de IDs'
        '\n[3] Trocar de conta'
        '\n[4] Abre a planilha com todos os produtos da conta'
        '\n[5] Atualize preço/estoque por SKU'
        '\n[6] Atualizar preço/estoque por planilha'
        '\n')

    msg_destaque('Programa feito por @imparcialista  v1.0')
    token = configurar_conta()
    msg_destaque(f'Conta conectada: {(nome_conta(token))}')
    msg('Digite SAIR para encerrar o programa')
    msg(mensagem_base)

    while not sair:
        escolha = get_input()

        if escolha == 'sair':
            msg_cima('Encerrando o programa...')
            break

        elif escolha == '?' or escolha == 'ajuda':
            msg('Digite SAIR para encerrar o programa')
            msg(mensagem_base)

        elif escolha == '1' or escolha == 'atualizar planilha':
            gerar_planilha(token)

        elif escolha == '2' or escolha == 'atualizar ids':
            pegar_todos_ids(token)

        elif escolha == '3' or escolha == 'trocar de conta':
            token = configurar_conta()

        elif escolha == '4' or escolha == 'abrir planilha':
            path = f'Arquivos/{(nome_conta(token))}/{(token[-9:])}-planilha-produtos.xlsx'
            path = os.path.realpath(path)

            if not os.path.exists(path):
                msg_cima('A planilha ainda não existe, gerando a planilha...')
                gerar_planilha(token)

            msg('Abrindo o arquivo...')
            os.startfile(path)
            msg('Arquivo aberto')

        elif escolha == '5' or escolha == 'atualizador':
            atualizar_info = True
            while atualizar_info:
                print()
                msg_cima('[Digite VOLTAR para retornar ao menu anterior]')
                msg_cima('O que você deseja atualizar?')
                msg_cima('[1] Estoque | [2] Preço')
                tipo_desejado = get_input()

                if tipo_desejado == 'voltar':
                    break

                if tipo_desejado == '1' or tipo_desejado == '2':

                    if tipo_desejado == '1':
                        atualizar_est = True

                        while atualizar_est:
                            print()
                            msg('[Digite VOLTAR para retornar ao menu anterior]')
                            msg_cima('Qual SKU você deseja atualizar o estoque?')
                            sku_escolhido = input('> ')
                            sku_escolhido = sku_escolhido.strip()
                            voltar = sku_escolhido.lower()

                            if voltar == 'voltar':
                                break

                            else:
                                print()
                                valor_para_atualizar = input('Para qual quantidade você deseja atualizar?\n> ')

                                try:
                                    valor_para_atualizar = int(valor_para_atualizar)

                                except:
                                    print()
                                    msg_alerta('[ERRO: Insira apenas números inteiros]')
                                    break

                                msg_cima(f'(SOLICITAÇÃO DE ALTERAÇÃO)')
                                print()
                                msg_dif('green', 'cima',
                                        f'SKU: {sku_escolhido} | Estoque: {valor_para_atualizar}')
                                pegar_produtos(sku_escolhido, valor_para_atualizar, token)
                                print()

                    else:
                        atualizar_prc = True

                        while atualizar_prc:
                            print()
                            msg('[Digite VOLTAR para retornar ao menu anterior]')
                            msg_cima('Qual SKU você deseja atualizar o preço?')
                            sku_escolhido = get_input()

                            if sku_escolhido == 'voltar':
                                msg('Você escolheu voltar')
                                break

                            else:
                                print()
                                valor_para_atualizar = input(str('Para qual preço você deseja atualizar?\n> '))
                                valor_para_atualizar = valor_para_atualizar.replace('.', '')

                                msg_dif('green', 'cima', f'(SOLICITAÇÃO DE ALTERAÇÃO)')
                                msg_dif('green', 'cima', f'SKU: {sku_escolhido} | Preço: R$ {valor_para_atualizar}')
                                valor_para_atualizar = valor_para_atualizar.replace(',', '.')

                                pegar_produtos(sku_escolhido, valor_para_atualizar, token)

                else:
                    msg_alerta('Opção inválida, digite apenas 1 ou 2')

        elif escolha == '6' or escolha == 'atualizar por planilha':
            planilha_atualizar = dlg.askopenfilename(filetypes=[("Arquivos excel", ".xlsx")])

            if planilha_atualizar == '':
                msg_alerta('Você não selecionou nenhum arquivo')

            else:
                print()
                msg(f'Caminho do arquivo: {planilha_atualizar}')
                df_atualizar = pd.read_excel(planilha_atualizar)

                lista_sku = []
                valor_trocar = []

                planilha_prc = False

                if df_atualizar.columns[0] == 'SKU':
                    for sku_df in df_atualizar['SKU']:
                        lista_sku.append(sku_df)

                    if df_atualizar.columns[1] == 'EST':
                        msg_cima('Modo atualizar estoque por planilha selecionado')
                        msg_alerta('ATENÇÃO: Produtos que estão oferecendo Full não serão alterados')

                        for est_df in df_atualizar['EST']:
                            valor_trocar.append(est_df)

                    elif df_atualizar.columns[1] == 'PRC':
                        msg_cima('Modo atualizar preço por planilha selecionado')
                        msg_alerta('ATENÇÃO: Produtos com promoção ativa não serão alterados para não sair da promoção')
                        planilha_prc = True

                        for prc_df in df_atualizar['PRC']:
                            valor_trocar.append(prc_df)

                    else:
                        msg_alerta('A planilha não segue um padrão para que seja atualizado')
                        break

                else:
                    msg_alerta('A planilha não segue um padrão para que seja atualizado')
                    continue

                msg(f'\n{len(df_atualizar['SKU'])} SKUs para atualizar\nDeseja continuar?\n[1] Sim | [2] Não')
                continuar = input(str('> '))

                if continuar == '1':

                    sku_disp = []
                    sku_nao_disp = []

                    for inx_sku, lista_sku_value in enumerate(lista_sku):

                        sku_mlb = str(lista_sku[inx_sku])
                        valor_mlb = valor_trocar[inx_sku]

                        if not planilha_prc:
                            valor_mlb = int(valor_mlb)

                        url_df = (f"{base}/users/{(token[-9:])}/items/search?seller_sku="
                                  f"{sku_mlb}&offset={0}")

                        resposta_df = fazer_reqs(url_df, token)
                        qtd_de_an = resposta_df['paging']['total']
                        print()

                        if qtd_de_an > 0:
                            base_print = f'SKU: {sku_mlb} | {qtd_de_an} Anúncio'

                            if planilha_prc:
                                valor_imprimir_novo = str(valor_mlb)
                                valor_imprimir_novo.replace('.', ',')
                                complemento = f'Preço: R$ {valor_imprimir_novo}'

                            else:
                                complemento = f'Estoque: {valor_mlb}'

                            if qtd_de_an == 1:
                                msg_dif('green', 'cima', f'{base_print} | {complemento}')

                            else:
                                msg_dif('green', 'cima', f'{base_print}s | {complemento}')

                            sku_disp.append(sku_mlb)

                            pegar_produtos(sku_mlb, valor_mlb, token)

                        else:
                            msg_alerta(f'SKU: {sku_mlb} | Nenhum anúncio encontrado')
                            sku_nao_disp.append(sku_mlb)

                    msg(f'\nSKUs encontrados: {sku_disp}')
                    msg(f'\nSKUs não encontrados: {sku_nao_disp}\n')

                elif continuar == '2':
                    msg_alerta('Você escolheu não continuar')

                else:
                    msg_alerta('Opção inválida')
                    pass

        else:
            print()
            msg_alerta('Opção inválida | Escolha uma das opções')
            msg_destaque(f'Conta conectada: {nome_conta(token)}')
            msg(mensagem_base)


if __name__ == "__main__":
    main()
