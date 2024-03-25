from percorrer_itens import *

planilha_arquivos = f'Arquivos/{nome_da_conta}/{id_do_vendedor}-planilha-produtos.xlsx'
planilha_teste = 'C:/Users/Lucas/Downloads/planilha_teste.xlsx'

if not os.path.exists(planilha_arquivos):
    gerar_planilha()
    time.sleep(1)

df_produtos = pd.read_excel(planilha_teste)
# print(df_produtos)

for linha in df_produtos['Matriz']:
    linha = str(linha)
    linha = linha.replace(' MATRIZ', '')

    print(linha)

print(df_produtos)
