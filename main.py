from ollama import chat
import copy


class LLMbot:
    def __init__(self, model, name):
        self.model = model
        self.messages = []
        self.name = name

    def updateChat(self, newMessages):
        self.messages = newMessages

    def lastResponse(self):
        return self.messages[-1] if self.messages else None


def sendQuery(model, query, messages):
    message = validateMessage('user', query)
    new_messages = messages + [message]

    chatResponse = chat(model=model, messages=new_messages)

    if 'message' in chatResponse:
        new_messages.append(chatResponse['message'])
    else:
        raise ValueError("Chat response is missing the 'message' field")

    return new_messages


def validateMessage(role, content):
    return {
        'role': role,
        'content': content,
    }


def printMessage(name, content):
    print("---------")
    print(f"{name}:")
    print(content)
    print()


def main():
    bot = LLMbot('llama3.2:3b', "Dave")
    bottwo = LLMbot('llama3.2:3b', "James")

    query = input('> ')
    conversation = []
    counter = 3
    index = 0

    while index < counter:

        bot.updateChat(sendQuery(bot.model, query, bot.messages))
        printMessage(bot.name, bot.lastResponse()['content'])


        query = bot.lastResponse()['content']
        bottwo.updateChat(sendQuery(bottwo.model, query, bottwo.messages))
        printMessage(bottwo.name, bottwo.lastResponse()['content'])


        query = bottwo.lastResponse()['content']
        index += 1


    with open("rawLog.txt", "a") as f:
        for message in bot.messages:
            f.write(f"{message}\n")


if __name__ == "__main__":
    main()
