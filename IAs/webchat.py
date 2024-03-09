import flet as ft
import google.generativeai as genai
from chaves import api_key

genai.configure(api_key=f'{api_key}')

generation_config = {
    "temperature"       : 0.9,
    "top_p"             : 1,
    "top_k"             : 1,
    "max_output_tokens" : 2048,
    }

safety_settings = [
    {
        "category"  : "HARM_CATEGORY_HARASSMENT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    {
        "category"  : "HARM_CATEGORY_HATE_SPEECH",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    {
        "category"  : "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    {
        "category"  : "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold" : "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
        )

convo = model.start_chat(
        history=[
            {
                "role"  : "user",
                "parts" : [
                    "você é um assistente, seu nome é Imparcibot"]
                },
            {
                "role"  : "model",
                "parts" : [
                    "Olá, meu nome é Imparcibot e sou um assistente virtual imparcial. Estou aqui para ajudá-lo com suas perguntas e solicitações de informações. Esforço-me por fornecer respostas precisas, equilibradas e objetivas, independentemente do meu próprio preconceito ou preferência pessoal."]
                },
            ]
        )


def main(page) :
    def btn_click(e) :

        if not pergunta.value :
            pergunta.error_text = "Por favor escreva uma pergunta"
            page.update()
        else :
            msg_usuario = pergunta.value
            convo.send_message(msg_usuario)
            resposta = convo.last.text
            txt_resposta = ft.Text(resposta, size=10)
            page.add(txt_resposta)


    texto_dica = ft.Text(
            f"Algumas respostas podem estar erradas", size=15
            )
    pergunta = ft.TextField(
            label="Qual sua pergunta?", width=400,
            autofocus=True
            )
    btn_perguntar = ft.ElevatedButton(
            "Perguntar", on_click=btn_click
            )

    page.add(texto_dica, pergunta, btn_perguntar)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
