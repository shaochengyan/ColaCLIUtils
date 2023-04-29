import os
import time
import pyperclip

from core.ColaCMDMenu import MenuItemSet
from .MD2Tex import ColaMD2Tex
from .TexUtils import ColaTexGenerator

class ColaMDTexPage(MenuItemSet):
    def __init__(self, **config_md2texer) -> None:
        super().__init__()
        self.mder = ColaMD2Tex(**config_md2texer)
        self.texer = ColaTexGenerator()

        # menu 1: for MD to latex 
        menu_name = "Markdown2Tex"
        cmd_dict = {
            "1": ["Clipboard markdown to latex code", self._keyfunc_mdAtex], 
            "2": [" Input markdown specified file, and store it into latex code (todo) ", self._keyfunc_none], 
            "chd": ["Change dir_md & dir_img_save ", self._keyfunc_chage_dir]
        }
        self.add_menuAkeyfunc(menu_name, **cmd_dict)

        # menu 2: for latex edit
        self.add_menuAkeyfunc(
            "Tex Utils", 
            _3=["Generate random lable.", self._keyfunc_texgen], 
            _4=["Clear equation with dollar(from clip).", self._keyfunc_axmatheq], 
            _5=["Save image and copy texcode (image from clip) ", self._keyfunc_clipimagetotex]
        )

        # help str
        helps = """\
- help: help
- chd: change dir (dir_mdfile for markdown file, dir_save_img for latex figures)
- exit: exit this page
"""
        self.add_helps(helps)


    def _keyfunc_mdAtex(self):
        s_md = pyperclip.paste()
        self.mder.mdtext2tex(s_md, is_clip=True)
    
    def _keyfunc_texgen(self):
        l = self.texer.generate_random_label(l=20)
        pyperclip.copy("\label{{{}}}".format(l))
    
    def _keyfunc_axmatheq(self):
        eq = pyperclip.paste()
        eqtex, eq_ref = self.texer.get_tex_eq(eq)
        pyperclip.copy(eq_ref)
        time.sleep(0.5)
        pyperclip.copy(eqtex)

    def _keyfunc_clipimagetotex(self):
        texcode = self.mder.save_img_create_texcode()    
        pyperclip.copy(texcode)

    def _keyfunc_chage_dir(self):
        path = input("Input dir_mdfile: ")
        if os.path.isdir(path):
            self.mder.dir_mdfile = path
        else:
            print("Path error.")
        path = input("Input dir_img_save:")
        if os.path.isdir(path):
            self.mder.dir_img_save = path
        else:
            print("Path error.")

if __name__=="__main__":
    menu = ColaMDTexPage()
    menu.runloop()

"""
python -m plugins.TexMD.MenuMDTex
"""