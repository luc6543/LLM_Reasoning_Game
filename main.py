from ollama import chat
from ollama import ChatResponse
from pydantic.v1.validators import constr_lower


# response: ChatResponse = chat(model='llama3.2:1b', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])
# # or access fields directly from the response object
# print(response.message.content)


def sendQuery(model, query, conversation):

    message = validateMessage('user', query)

    conversation.append(message)

    chatResponse = chat(model=model, messages=conversation)



    conversation.append(chatResponse['message'])

    return conversation


def validateMessage(role, content):
    message = {
        'role': role,
        'content': content,
    }
    return message



conversation = []
while True:
    query = input('> ')
    conversation = sendQuery('llama3.2:1b', query, conversation)
    print(conversation[-1]['content'])