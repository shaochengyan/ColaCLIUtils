# -*- coding: utf-8 -*-
import yaml
from dotmap import DotMap 
import subprocess

# cola import
from core.ColaCMDMenu import MenuItemSet



def get_config(file_yaml):
    with open(file_yaml, "r") as f:
        config = yaml.safe_load(f)
    return DotMap(config) 

config = get_config("config.yaml")


class MainPage(MenuItemSet):
    def __init__(self) -> None:
        super().__init__(is_page_dif_prefix=False)

        self.menu_texmd = None
        self.chatgpt = None
        self.session = None
        # main page menu
        self.add_menuAkeyfunc(
            "Cola UTools", 
            _1=["Tex and Markdown", self._keyfunc_terAmdpage], 
            _2=["Run Some exe(TODO such as spider)", self._keyfunc_none],   # TODO
            _3=["Chat with gpt", self._keyfunc_chatwithgpt], 
            _4=["Open session", self._keyfunc_session]
        )    

        # edit config
        self.add_menuAkeyfunc(
            "Meta", 
            econfig=["Edit config.yaml file", self._keyfunc_edit_config]
        )

        # help string    
        helps = """\
- 1: latex and markdown utils
- 3: chat with chatgpt
"""
        self.add_helps(helps)
    
    def _keyfunc_edit_config(self):
        file = config.config_path
        print(file)
        subprocess.Popen(["notepad", "", file], shell=True) # return a object to control subprocess and not control.

    def _keyfunc_session(self):
        if self.session is None:
            from plugins.Sessions.ColaSessions import ColaSessions
            self.session = ColaSessions(config["Session"])
        return self.session.runloop()
    
    def _keyfunc_chatwithgpt(self):
        if self.chatgpt is None:
            from plugins.ChatGPT.ColaChatGPT import ChatWithGPT
            self.chatgpt = ChatWithGPT(api_key=config["ChatGPT"]["api_key"])
        self.chatgpt.chat_with_gpt()
    
    def _keyfunc_terAmdpage(self):
        if self.menu_texmd == None:
            from plugins.TexMD.ColaMDTexPage import ColaMDTexPage
            self.menu_texmd = ColaMDTexPage(**config['TexMD'])  # TODO?
            # self.menu_texmd = ColaMDTexPage()
        return self.menu_texmd.runloop()


def main():
    menu_main = MainPage()
    menu_main.runloop()


if __name__=="__main__":
    main()

"""
python -m main
"""
