import yaml
import openai
import json
import os
import pyperclip

import ColoryChar as ccc
from ColaLogger import ColaLogger

# load api key
def get_api_key():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    api_key = config["api_key"]
    return api_key



class ChatGPT:
    def __init__(self, user):
        openai.api_key = get_api_key()
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

def chat_with_gpt():
    logger = ColaLogger("gpt", is_just_info=True)
    chat = new_chat()
    while True:
        if len(chat.messages) >= 11:
            print("New chat ...")
            chat = new_chat()
            
        # question
        mesg = input("{}{}".format(
            ccc.colory(chat.user, ccc.BOLD, ccc.GREEN),
            ccc.colory("@win>> ", ccc.BOLD, ccc.BLUE) 
        ))
        
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
        info_ans = "{}{}\n".format(
            ccc.colory("ChatGPT>> ", ccc.PURPLE, ccc.BOLD), 
            ccc.colory(answer, ccc.CYAN), 
            )
        logger.info("{}>> {}".format(chat.user, mesg))
        logger.info(info_ans)
        print(info_ans)
        chat.messages.append({"role": "assistant", "content": answer})

if __name__ == '__main__':
    chat_with_gpt()