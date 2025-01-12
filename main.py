from ollama import chat
from ollama import ChatResponse
from pydantic.v1.validators import constr_lower
import copy


class LLMbot:
    def __init__(self, model, messages, name):
        self.model = model
        self.messages = messages
        self.name = name

    def updateChat(self, newMessages):
        self.messages = newMessages

    def lastResponse(self):
        try:
            return self.messages[-1]['content']
        except IndexError:  #
            return None


def sendQuery(model, query, conversation):
    message = validateMessage('user', query)
    conversation.append(message)

    chatResponse = chat(model=model, messages=conversation)

    if 'message' in chatResponse:
        conversation.append(chatResponse['message'])
    else:
        raise ValueError("Chat response is missing the 'message' field")

    return conversation


def validateMessage(role, content):
    return {
        'role': role,
        'content': content,
    }


def generateName(level):
    adjective = ""
    if level == 0:
        adjective = "gamer tag"
    elif level == 1:
        adjective = "name"

    query = "Generate me a " + adjective + ". Dont respond with anything else"

    response = sendQuery(model='llama3.2:1b', query=query, conversation=[])

    return response[-1]['content'];

def switchSender(messages):
    newMessages = []
    for message in messages:
        newMessage = copy.deepcopy(message)
        if newMessage['role'] == 'user':
            newMessage['role'] = 'assistant'
        elif newMessage['role'] == 'assistant':
            newMessage['role'] = 'user'
        newMessages.append(newMessage)
    return newMessages


def printMessage(name, content):
    print("---------")
    print(f"{name}:")
    print(content)
    print()


bot = LLMbot('llama3.2:3b', [], generateName(0))
bottwo = LLMbot('llama3.2:3b', [], generateName(0))
conversation = []

query = input('> ')
counter = 30
index = 0

bot.updateChat(switchSender(conversation))
conversation = sendQuery(bot.model, query, bot.messages)

while counter > index:
    bottwo.updateChat(switchSender(conversation))
    conversation = sendQuery(bottwo.model, bot.lastResponse(), bottwo.messages)
    printMessage(bottwo.name, bottwo.lastResponse())

    bot.updateChat(switchSender(conversation))
    conversation = sendQuery(bot.model, bottwo.lastResponse(), bot.messages)
    printMessage(bot.name, bot.lastResponse())

    index += 1

with open("rawLog.txt", "a") as f:
    for message in bot.messages:
        f.write(f"{message}\n")
