import google.generativeai as genai
from simple_colors import *
from chaves import api_key


genai.configure(api_key=f'{api_key}')

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
  }

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
  ]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["você é um assistente, seu nome é Imparcibot"]
    },
  {
    "role": "model",
    "parts": ["Olá, meu nome é Imparcibot e sou um assistente virtual imparcial. Estou aqui para ajudá-lo com suas perguntas e solicitações de informações. Esforço-me por fornecer respostas precisas, equilibradas e objetivas, independentemente do meu próprio preconceito ou preferência pessoal."]
    },
  ])


sair = False
print('Digite SAIR para sair\n')

convo.send_message('Por favor, se apresente')
resposta = convo.last.text
print(blue(resposta, 'bold'))

while not sair:
  msg_usuario = input(str('> '))
  if msg_usuario == 'SAIR':
    sair = True

  convo.send_message(msg_usuario)
  resposta = convo.last.text
  print(blue(resposta, 'bold'))

