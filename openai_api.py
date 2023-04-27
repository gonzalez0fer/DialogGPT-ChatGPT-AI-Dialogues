import openai
import os
from dotenv import load_dotenv
from data.init_prompts import *

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def openai_request(language):
    # Define a function to remove line breaks from a list of strings
    def delete_line_break(lista):
        for i in range(len(lista)):
            lista[i] = lista[i].replace('\n', '')
            lista[i] = lista[i].replace('Kyle:', '')
            lista[i] = lista[i].replace('Cartman:', '')
        return lista

    # Define a function to make requests to the OpenAI API with retries
    def openai_connection(user_prompt):
        MAX_TRIES = 3
        tries = 0
        while tries < MAX_TRIES:
            try:
                # Try to make the request to the OpenAI API
                completion = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt = user_prompt,
                    max_tokens=256
                )
                # If the request is successful, return the model's response
                return completion.choices[0].text
            except Exception as e:
                # If an error occurs, print an error message and retry
                tries += 1
                print("Error request to OpenAI. Trying again ({}/{}): {}".format(tries, MAX_TRIES, e))
         # If the maximum number of retries is reached and the request still fails, return None
        return None
    
    if language == "ES":
        prompt_receiver = description_ES_b + situation_ES_b # Initial prompt for the receiver in Spanish
        prompt_sender = description_ES_a + situation_ES_a # Initial prompt for the sender in Spanish
        sender_list = ['Hola chico Slytherin, como estas?'] # Initial response from the sender in Spanish
    else:
        prompt_receiver = description_EN_b + situation_EN_b # Initial prompt for the receiver in English
        prompt_sender = description_EN_a + situation_EN_a # Initial prompt for the sender in English
        sender_list = ['Hello Slytherin boy, how are you?'] # Initial response from the sender in English

    itera = 0 # Initialize the variables needed for the conversation
    openai_iterations = int(os.getenv("OPENAI_NUMBER_ITERATIONS"))
    receiver_list = []
    # Carry out the conversation using requests to the OpenAI API
    while itera < openai_iterations:
        # Generate the receiver's response
        response_receiver = openai_connection(prompt_receiver)
        #print(response_receiver)
        # Add the receiver's response to the sender's prompt
        prompt_sender = prompt_sender + ('\nKyle: '+response_receiver+'\n')
        prompt_receiver = prompt_receiver + ('\nKyle: '+ response_receiver + '\n')
        # Add the receiver's response to the list of receiver's responses
        receiver_list.append(response_receiver)

        # Generate the sender's response based on the receiver's response
        reponse_sender = openai_connection(response_receiver)
        #print(reponse_sender)
        prompt_receiver = prompt_receiver + ('\nCartman: '+ reponse_sender + '\n')
        prompt_sender = prompt_sender + ('\nCartman: '+ reponse_sender + '\n')
        # Add the sender's response to the list of sender's responses
        sender_list.append(reponse_sender)
        itera += 1
    # Return a dictionary with the sender's and receiver's response lists without line breaks
    return {'sender':delete_line_break(sender_list), 'receiver':delete_line_break(receiver_list)}
