from ollama import chat


class LLMbot:
    def __init__(self, model, name, messages):
        self.model = model
        self.messages = messages
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
def printStop(name):
    print("========")
    print(f"{name} has stopped the conversation")
    print()

def chatFunctions(text):
    if "[stop]" in text:
        return True
    if "[HUMAN]" in text:
        return True
    if "[AI]" in text:
        return True


def main():
    bot = LLMbot('llama3.1:latest', "Dave -Detective", [validateMessage("user", "Figure out if the other chatter is an Large language model, you can chat 5 times before running out, dont immediately guess, figure out. Respond with [AI] if you think its an Large language model, respond [HUMAN] if you think you are talking to a human, give a small explanation why you think what you choose in the same message. Once you say [AI] or [HUMAN] the conversation stops. The other chatter might try to trick you.")])
    bottwo = LLMbot('llama3.2:1b', "James -Imposter", [validateMessage("user", "Trick the other party into believing you are a HUMAN")])

    query = input('> ')
    conversation = []
    counter = 10
    index = 0

    while index < counter:
        print(str(index) + "/" + str(counter))
        print()
        bot.updateChat(sendQuery(bot.model, query, bot.messages))
        printMessage(bot.name, bot.lastResponse()['content'])

        if chatFunctions(bot.lastResponse()['content']):
            printStop(bot.name)
            return

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
