import requests


def configurar_conta():
    conta_configurada = False
    while not conta_configurada:
        access_token_value = input(str('Insira o Access Token = '))

        headers = {'Authorization': f'Bearer {access_token_value}'}
        resposta = requests.get(f'https://api.mercadolibre.com/users/me', headers=headers)

        if resposta.status_code == 200:
            return access_token_value
        else:
            print('Access Token inválido ou expirado\n')

