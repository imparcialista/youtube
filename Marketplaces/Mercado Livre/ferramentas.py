import json


def ler_json(arquivo) :
    arquivo_json = open(arquivo, encoding='UTF-8')
    data = json.load(arquivo_json)
    # Exemplo: ler_json('./arquivos/lista.json')
    return data