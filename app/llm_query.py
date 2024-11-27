from openai import OpenAI
import os

api_key = os.getenv('OPENAI_API_KEY')
print(api_key)

def conversation_to_string(conversation):
    # print(conversation)
    conversation_string = ""
    for message in conversation.messages:
        message_str = "{Sender: " + message.sender +  ", Message: " + message.content +"} "
        conversation_string += message_str
    # print(conversation_string)
    return conversation_string

def get_open_ai_resp(previous_conv,userInput):

    # Define the prompt you want to send to the GPT model
    global api_key
    client = OpenAI(api_key=api_key)
    # conversation_to_string(previous_conv)
    prompt = "The previous conversation is: ["+ conversation_to_string(previous_conv) +"]. Answer the following: " + str(userInput)
    print("get_open_ai_prompt: ",prompt)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
           {"role": "system", "content": "You are a chatbot on Math Assistant website"},
        {"role": "user", "content": prompt}
    ]
    )
    # print("get_open_ai_resp: ",completion.choices[0].message.content)
    return completion.choices[0].message.content