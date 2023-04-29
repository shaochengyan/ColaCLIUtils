# -*- coding: utf-8 -*-
from dotmap import DotMap    

# cola import
from core.ColaCMDMenu import MenuItemSet

def get_config(**kwargs):
    return DotMap(kwargs) 

config = get_config(
    dir_mdfile="D:/ColaDatabase/ColaBook/tmp_md", 
    dir_img_save="D:/ColaDatabase/ColaBook/cola_figures"
)

class MainPage(MenuItemSet):
    def __init__(self) -> None:
        super().__init__()

        self.menu_texmd = None
        # main page menu
        self.add_menuAkeyfunc(
            "Cola UTools", 
            _1=["Tex and Markdown", self._keyfunc_terAmdpage], 
            _2=["Run Some exe(TODO such as spider)", self._keyfunc_none],   # TODO
            _3=["Chat with gpt", self._keyfunc_chatwithgpt]
        )    

        # help string    
        helps = """\
- 1: latex and markdown utils
- 3: chat with chatgpt
"""
        self.add_helps(helps)
    
    def _keyfunc_chatwithgpt(self):
        from plugins.ChatGPT.ColaChatGPT import chat_with_gpt
        chat_with_gpt()
    
    def _keyfunc_terAmdpage(self):
        if self.menu_texmd == None:
            from plugins.TexMD.ColaMDTexPage import ColaMDTexPage
            self.menu_texmd = ColaMDTexPage(**config)  # TODO?
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
