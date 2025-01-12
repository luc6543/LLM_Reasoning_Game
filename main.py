from ollama import chat
from ollama import ChatResponse
from pydantic.v1.validators import constr_lower
class LLMbot:
    def __init__(self, model, messages):
        self.model = model
        self.messages = messages

    def updateChat(self, newMessages):
        self.messages = newMessages

    def lastResponse(self):
        return self.messages[-1]['content']

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

bot = LLMbot('llama3.2:1b', [])
while True:
    query = input('> ')
    conversation = sendQuery(bot.model, query, bot.messages)
    bot.updateChat(conversation)
    print(bot.lastResponse())



