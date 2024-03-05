import pandas as pd
import os

# Esse programa utiliza a tabela gerada no Melhor Envio para Amazon

# Aqui você pode mudar o nome do arquivo
seu_nome_do_arquivo = 'tabela_amz.xlsx'
tabela_amz = seu_nome_do_arquivo
df = pd.read_excel(tabela_amz)

df = df.replace({'Capital' : 'Capital)', 'Interior' : 'Interior)', 'RO' : 'Rondônia(Rondônia', 'AC' : 'Acre(Acre', 'AM' : 'Amazonas(Amazonas', 'RR' : 'Roraima(Roraima', 'PA' : 'Pará(Pará', 'AP' : 'Amapá(Amapá', 'TO' : 'Tocantins(Tocantins', 'MA' : 'Maranhão(Maranhão', 'PI' : 'Piauí(Piauí', 'CE' : 'Ceará(Ceará', 'RN' : 'Rio Grande do Norte(Rio Grande do Norte', 'PB' : 'Paraíba(Paraíba', 'PE' : 'Pernambuco(Pernambuco', 'AL' : 'Alagoas(Alagoas', 'SE' : 'Sergipe(Sergipe', 'BA' : 'Bahia(Bahia', 'MG' : 'Minas Gerais(Minas Gerais', 'ES' : 'Espírito Santo(Espírito Santo', 'RJ' : 'Rio de Janeiro(Rio de Janeiro', 'SP' : 'São Paulo(São Paulo', 'PR' : 'Paraná(Paraná', 'SC' : 'Santa Catarina(Santa Catarina', 'RS' : 'Rio Grande do Sul(Rio Grande do Sul', 'MS' : 'Mato Grosso do Sul(Mato Grosso do Sul', 'MT' : 'Mato Grosso(Mato Grosso', 'GO' : 'Goiás(Goiás', 'DF' : 'Distrito Federal(Distrito Federal'}, regex=True)

'''
lista_escolhas = {}

for linha in range(30):
    if linha < 3:
        lista_escolhas.update({ linha : 'escolha_1'})
    elif linha < 5:
        lista_escolhas.update({ linha : 'escolha_2'})
    elif linha < 7:
        lista_escolhas.update({ linha : 'escolha_3'})
    elif linha < 9:
        lista_escolhas.update({ linha : 'escolha_4'})
    elif linha < 13:
        lista_escolhas.update({ linha : 'escolha_5'})
    elif linha < 18:
        lista_escolhas.update({ linha : 'escolha_6'})
    elif linha < 22:
        lista_escolhas.update({ linha : 'escolha_7'})
    elif linha <= 28:
        lista_escolhas.update({ linha : 'escolha_8'})
    else:
        lista_escolhas.update({ linha : 'escolha_8'})

print(lista_escolhas)
# aqui você pega o print e coloca no replace abaixo

'''

df = df.replace({0: 'escolha_1', 1: 'escolha_1', 2: 'escolha_1', 3: 'escolha_2', 4: 'escolha_2', 5: 'escolha_3', 6: 'escolha_3', 7: 'escolha_4', 8: 'escolha_4', 9: 'escolha_5', 10: 'escolha_5', 11: 'escolha_5', 12: 'escolha_5', 13: 'escolha_6', 14: 'escolha_6', 15: 'escolha_6', 16: 'escolha_6', 17: 'escolha_6', 18: 'escolha_7', 19: 'escolha_7', 20: 'escolha_7', 21: 'escolha_7', 22: 'escolha_8', 23: 'escolha_8', 24: 'escolha_8', 25: 'escolha_8', 26: 'escolha_8', 27: 'escolha_8', 28: 'escolha_8', 29: 'escolha_8'})

print(df)

if os.path.exists(f'{tabela_amz}'):
    os.remove(f'{tabela_amz}')

df.to_excel(f'{tabela_amz}', index=False)
