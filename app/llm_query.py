from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')

def conversation_to_string(conversation):
    conversation_string = ""
    for message in conversation.messages:
        message_str = "{Sender: " + message.sender +  ", Message: " + message.content +"} "
        conversation_string += message_str
    return conversation_string

def get_open_ai_resp(previous_conv,userInput):
    global api_key
    client = OpenAI(api_key=api_key)
    prompt = "The previous conversation is: ["+ conversation_to_string(previous_conv) +"]. Answer the following: " + str(userInput)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": "You are a chatbot on Math Assistant website, only assist with math problems and politely decline to assist on things not related to Math"},
        {"role": "user", "content": prompt}
    ]
    )
    return completion.choices[0].message.content