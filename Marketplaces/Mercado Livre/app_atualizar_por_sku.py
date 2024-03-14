import flet as ft
from chaves import access_token
from ferramentas import atualizar_estoque
from atualizar_por_sku import fazer_reqs


def pegar_produtos(sku, qtd):
    paginas = 0
    resposta = fazer_reqs(0, sku)
    quantidade_de_an = resposta['paging']['total']

    if quantidade_de_an == 0:
        return

    else:
        resposta = fazer_reqs(0, sku)
        quantidade_de_an = resposta['paging']['total']

        while quantidade_de_an > 0:
            quantidade_de_an -= 50
            paginas += 1

        for pagina in range(paginas):
            print(f'Página: {pagina + 1} | Offset {pagina * 50}')
            resposta = fazer_reqs(pagina * 50, sku)

            for produto in resposta['results']:
                atualizar_estoque(produto, qtd)


def main(page):
    page.scroll = "always"
    page.title = "Atualizar estoque"
    page.window_title_bar_hidden = False
    page.window_frameless = False
    # page.window_left = 500
    # page.window_top = 300
    page.window_width = 300
    page.window_height = 300
    page.window_always_on_top = False


    # page.window_movable = True
    # page.window_opacity = 0.90

    def btn_click(e):
        if not sku_mlb.value:
            sku_mlb.error_text = "Por favor insira um SKU"
            page.update()
        else:

            sku = sku_mlb.value
            qtd = qtd_mlb.value
            qtd = int(qtd)
            pegar_produtos(sku, qtd)
            retorno = f'Solicitado alteração: SKU = {sku} | Estoque: {qtd}'
            txt_resposta = ft.Text(f"{retorno}", size=15)
            page.add(txt_resposta)

            page.update()


    texto_dica = ft.Text(f'', size=20)
    sku_mlb = ft.TextField(label="SKU", width=200, autofocus=True)
    qtd_mlb = ft.TextField(label="Quantidade", width=200, value='')
    # access_token_label = ft.TextField(label="Conta", width=200, value=access_token)
    btn_perguntar = ft.ElevatedButton("Atualizar", on_click=btn_click)

    # page.add(texto_dica, sku_mlb, qtd_mlb, access_token_label, btn_perguntar)
    page.add(texto_dica, sku_mlb, qtd_mlb, btn_perguntar)
    # page.add(sku_mlb, qtd_mlb, btn_perguntar)


ft.app(target=main)