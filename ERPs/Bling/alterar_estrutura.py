import requests
import json

nome_produto = '4x Acendedor Bic Megalighter Flex Fogão Lareira Churrasqueira'
code_produto = '510-4'
id_produto_alterar = '16246285362'
id_produto_matriz = '15270604288'
quantidade_estrutura = '4'

estrutura = [nome_produto, code_produto, id_produto_matriz, quantidade_estrutura, id_produto_alterar]

url = f"https://www.bling.com.br/Api/v3/produtos/{estrutura[4]}"

payload = json.dumps(
        {
            "nome"     : f"{estrutura[0]}",
            "codigo"    : f"{estrutura[1]}",
            "tipo"     : "P",
            "formato"  : "E",
            "unidade": "UN",
            "observacoes": "@imparcialista",
            "estrutura": {
                "tipoEstoque": "V",
                "componentes": [
                    {
                        "produto"   : {
                            "id": f"{estrutura[2]}"
                            },
                        "quantidade": f"{estrutura[3]}"
                        }
                    ]
                }
            })

headers = {
    'Content-Type' : 'application/json',
    'Accept'       : 'application/json',
    'Authorization': '-',
    'Cookie'       : '-'
    }

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
