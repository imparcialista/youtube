# from percorrer_itens import *

'''
planilha_arquivos = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'
planilha_teste = 'C:/Users/Lucas/Downloads/planilha_teste.xlsx'

if not os.path.exists(planilha_arquivos):
    gerar_planilha()
    time.sleep(1)

# df_produtos = pd.read_excel(planilha_teste)
df_produtos = pd.read_excel(planilha_arquivos)
# print(df_produtos)

for linha in df_produtos['Matriz']:
    linha = str(linha)
    linha = linha.replace(' MATRIZ', '')

    print(linha)

print(df_produtos)
'''

sair = False
print('Digite SAIR para encerrar o programa')


def get_input():
    input_user = input(str(''))
    input_user = input_user.lower()
    input_user = input_user.strip()
    return input_user


while not sair:
    escolha = get_input()
    
    if escolha == 'sair':
        print('Encerrando o programa...')
        quit()
    elif escolha == 'ajuda':
        print('Digite SAIR para encerrar o programa')
    else:
        print('Opção inválida | Escolha uma das opções')

    # print(input_user)
