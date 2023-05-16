import yaml
import openai
import json
import os
import pyperclip

import utils.ColoryChar as ccc
from utils.ColaLogger import ColaMarkdownLogger
from utils.ColaCMDIO import ColaCMDIO

class ChatGPT:
    def __init__(self, user):
        self.user = user
        self.filename="./user_messages.json"
        self.messages = []

    def ask_gpt(self, message):
        rsp = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
        #   model="davinci",
          messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]

def new_chat():
    # user = input("Your Name: ")
    user = "cola"
    chat = ChatGPT(user)
    return chat


class ChatWithGPT:
    def __init__(self, api_key:str) -> None:
        openai.api_key = api_key


    def chat_with_gpt(self):
        logger = ColaMarkdownLogger("gpt")
        chat = new_chat()
        cmdio = ColaCMDIO() 
        while True:
            if len(chat.messages) >= 11:
                print("New chat ...")
                chat = new_chat()
                
            # question
            mesg = cmdio.getline_user("cola_robot", "Input your question")

            
            if mesg == "exit":
                break
            elif "$clip" in mesg:
                clip = pyperclip.paste()
                mesg = mesg.replace("$clip", "\n{}".format(clip))
            elif mesg == "help":
                print("help: manu for this.\nexit: exit.\nclip: get message from clip.")
                continue
            elif mesg == "":
                continue
            elif mesg == "new":
                # save and reload
                chat = new_chat()
                continue
                
            # ask -> ans -> show -> record
            chat.messages.append({"role": "user", "content": mesg})
            answer = chat.ask_gpt(mesg)
            cmdio.out_pair("chatgpt", answer)
            logger.log(chat.user, mesg)
            logger.log("GPT", answer)
            chat.messages.append({"role": "assistant", "content": answer})

if __name__ == '__main__':
    chat = ChatWithGPT(api_key="test")
    chat.chat_with_gpt()
"""
python -m plugins.ChatGPT.ColaChatGPT
"""