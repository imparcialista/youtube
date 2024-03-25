from gerar_planilha import *

planilha_arquivos = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'
planilha_teste = 'C:/Users/Lucas/Downloads/planilha_teste.xlsx'

if not os.path.exists(planilha_arquivos):
    gerar_planilha()
    time.sleep(1)

# df_produtos = pd.read_excel(planilha_teste)
# df_produtos = pd.read_excel(planilha_arquivos)
# print(df_produtos)
'''
for linha in df_produtos['Matriz']:
    linha = str(linha)
    linha = linha.replace(' MATRIZ', '')

    print(linha)
'''
# print(df_produtos)

sair = False

mensagem('Digite SAIR para encerrar o programa')
mensagem(f'Conta conectada: {nome_da_conta}')
mensagem_base = ('\n[*] Escolha uma das opções, número ou comando'
                 '\n[1] Atualizar planilha | Gera uma nova planilha com todos os produtos'
                 '\n[2] Atualizar ids | Busca e atualiza a lista de IDS do Mercado Livre'
                 '\n[3] Trocar de conta | Altere a conta conectada alterando o Access Token'
                 '\n[?] Ajuda | Mostra os comandos disponíveis')
print(mensagem_base)


def get_input():
    input_user = input(str('> '))
    input_user = input_user.lower()
    input_user = input_user.strip()
    return input_user


while not sair:
    escolha = get_input()

    if escolha == 'sair':
        mensagem('Encerrando o programa...')
        quit()

    elif escolha == '?' or escolha == 'ajuda':
        mensagem('Digite SAIR para encerrar o programa')
        print(mensagem_base)

    elif escolha == '1' or escolha == 'atualizar planilha':
        gerar_planilha()
        print(mensagem_base)

    elif escolha == '2' or escolha == 'atualizar ids':
        pegar_todos_ids()
        print(mensagem_base)
    elif escolha == '3' or escolha == 'trocar de conta':
        mensagem('Função indisponível no momento')
        print(mensagem_base)

        '''
        conta_nova = False
        while not conta_nova:

            novo_token = input(str('access_token = '))

            headers = {'Authorization': f'Bearer {novo_token}'}
            resposta = requests.get(f'{base}/users/me', headers=headers)

            if resposta.status_code != 200:
                mensagem(f'Falha na requisição | {novo_token} é inválido')
                pass
            
            else:
                resposta = resposta.json()
                nome_da_conta = resposta['nickname']
                mensagem(f'Conta conectada: {nome_da_conta}')
                print(mensagem_base)

                with open('access_token.py', 'w') as trocar_conta:
                    trocar_conta.write(f"access_token = '{novo_token}'\n")

                conta_nova = True

        '''
    else:
        print('\n[X] Opção inválida | Escolha uma das opções')
        print(mensagem_base)
