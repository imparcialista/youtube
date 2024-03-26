from gerar_planilha import *
from configurar_conta import configurar_conta
'''
planilha_arquivos = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'
planilha_base = f'Arquivos/planilha_base.xlsx'

if not os.path.exists(planilha_arquivos):
    gerar_planilha()
    time.sleep(1)


df_produtos = pd.read_excel(planilha_arquivos)
# print(df_produtos)

df_filtrado = df_produtos.loc[0:, ['attributes', 'available_quantity', 'id', ]]

print(df_filtrado)
df_teste = df_filtrado.groupby("attributes").count()
print(df_teste)

# df_filtrado.to_excel('df_filtrado.xlsx', index=False)
'''

access_token = configurar_conta()
nome = fazer_reqs(f'{base}/users/me', access_token)
nome_da_conta = nome['nickname']

sair = False

mensagem('Digite SAIR para encerrar o programa')
mensagem(f'Conta conectada: {nome_da_conta}')
mensagem_base = ('\n[*] Escolha uma das opções, número ou comando'
                 '\n[1] Atualizar planilha | Gera uma nova planilha com todos os produtos'
                 '\n[2] Atualizar ids | Busca e atualiza a lista de IDS do Mercado Livre'
                 '\n[3] Trocar de conta | Altere a conta conectada alterando o Access Token')
# '\n[?] Ajuda | Mostra os comandos disponíveis'
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
        mensagem(f'Conta conectada: {nome_da_conta}')
        print(mensagem_base)

    elif escolha == '1' or escolha == 'atualizar planilha':
        gerar_planilha(access_token)
        mensagem(f'Conta conectada: {nome_da_conta}')
        print(mensagem_base)

    elif escolha == '2' or escolha == 'atualizar ids':
        pegar_todos_ids(access_token)
        mensagem(f'Conta conectada: {nome_da_conta}')
        print(mensagem_base)

    elif escolha == '3' or escolha == 'trocar de conta':
        mensagem('Função indisponível no momento')
        access_token = configurar_conta()
        mensagem(f'Conta conectada: {nome_da_conta}')
        print(mensagem_base)

    else:
        print('\n[X] Opção inválida | Escolha uma das opções')
        mensagem(f'Conta conectada: {nome_da_conta}')
        print(mensagem_base)
