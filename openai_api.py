import openai
import os
from dotenv import load_dotenv
from data.init_prompts import *

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def eliminar_saltos_de_linea(lista):
    for i in range(len(lista)):
        lista[i] = lista[i].replace('\n', '')
    return lista


def openai_connection(user_prompt):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt = user_prompt,
        max_tokens=2048
    )
    return completion.choices[0].text

itera = 0
prompt_receptor = description_ES_b + sitution_ES_b
prompt_hablante = description_ES_a + sitution_ES_a

receptor_list = []
hablante_list = ['Hola, como estas?']

while itera < 2:
    
    response_receptor = openai_connection(prompt_receptor)
    print(response_receptor)
    prompt_hablante = prompt_hablante + ('\n'+response_receptor+'\n')
    prompt_receptor = prompt_receptor + ('\n'+ response_receptor + '\n')
    receptor_list.append(response_receptor)
    reponse_hablante = openai_connection(response_receptor)
    print(reponse_hablante)
    prompt_receptor = prompt_receptor + ('\nKatherine: '+ reponse_hablante + '\n')
    prompt_hablante = prompt_hablante + ('\nKatherine: '+ reponse_hablante + '\n')
    hablante_list.append(reponse_hablante)
    itera += 1

print('#########################################')
print(prompt_receptor)
print('---------------------')
print(prompt_hablante)

