# -*- coding: utf-8 -*-
from dotmap import DotMap    
import pyperclip
import time
import os
import platform

# cola import
from ColaCMDMenu import ColaCMDMenuItem
from MD2Tex import ColaMD2Tex
from TexUtils import ColaTexGenerator
import ColoryChar as ccc
from ColaChatGPT import chat_with_gpt

def get_config(**kwargs):
    return DotMap(kwargs) 

config = get_config(
    dir_mdfile="D:/ColaDatabase/ColaBook/tmp_md", 
    dir_img_save="D:/ColaDatabase/ColaBook/cola_figures"
)

class MenuItemSet:
    def __init__(self) -> None:
        self.menus = []
    
    def help(self):
        print("q: exit\n h: help\ncls: clear terminal")
    
    def add_menu(self, name, **cmd_dict):
        self.menus.append(
            ColaCMDMenuItem(name, **cmd_dict)
        )

    def show(self):
        for menu in self.menus:
            print(menu)
        print("")
    
    def getkey(self):
        # self.clear_terminal()
        self.show()
        key = input(ccc.colory(">> ", ccc.BOLD))
        # self.show()
        self.clear_terminal()
        return key

    def clear_terminal(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')            
 
    def runloop(self):
        pass
    

class ColaMDTexMenu(MenuItemSet):
    def __init__(self, config_md2texer) -> None:
        super().__init__()
        self.mder = ColaMD2Tex(**config_md2texer)
        self.texer = ColaTexGenerator()

        # menu 1: for MD to latex 
        menu_name = "Markdown2Tex"
        cmd_dict = {
            "1": "Clipboard markdown to latex code", 
            "2": "Input markdown specified file, and store it into latex code (todo)", 
            "c": "Change dir_md & dir_img_save"
        }
        self.add_menu(menu_name, **cmd_dict)

        # menu 2: for latex edit
        self.add_menu(
            "Tex Utils", 
            _3="Generate random lable", 
            _4="Clear equation with dollar(from clip)", 
            _5="Save image and copy texcode (image from clip)"
        )
    
    def chage_dir(self):
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

    def runloop(self):
        while True:
            key = self.getkey()

            # key -> function
            s_md = pyperclip.paste()

            # 1 markdown 字符串 -> texcode
            if key == "1":
                self.mder.mdtext2tex(s_md, is_clip=True)
            # TODO
            elif key == "2":
                pass
            # 产生随机label
            elif key == "3":  
                l = self.texer.generate_random_label(l=20)
                pyperclip.copy("\label{{{}}}".format(l))
            # 清除由AxMath复制latex代码过来时的双$$符号jj
            elif key == "4":
                eq = pyperclip.paste()
                eqtex, eq_ref = self.texer.get_tex_eq(eq)
                pyperclip.copy(eq_ref)
                time.sleep(0.5)
                pyperclip.copy(eqtex)
            # 从剪切板存储图片到指定的文件夹后，产生对应的tex代码
            elif key == "5":
                texcode = self.mder.save_img_create_texcode()    
                pyperclip.copy(texcode)
            elif key == "help":
                print("chd: change dir\nhelp: help\nexit: exit this page")
            elif key == "chd":
                self.chage_dir()
            elif key == "exit":
                break
 
    # old version
    def run(self):
        self.show()
        key = input(ccc.colory("INPUT: ", ccc.BOLD))
        self.clear_terminal()
        # get str from clip
        s_md = pyperclip.paste()
        # TODO: do somthing by Key
        # markdown 字符串 -> texcode
        if key == "1":
            self.mder.mdtext2tex(s_md, is_clip=True)
        # TODO
        elif key == "2":
            pass
        # 产生随机label
        elif key == "3":  
            l = self.texer.generate_random_label(l=20)
            pyperclip.copy("\label{{{}}}".format(l))
        # 清除由AxMath复制latex代码过来时的双$$符号jj
        elif key == "4":
            eq = pyperclip.paste()
            eqtex, eq_ref = self.texer.get_tex_eq(eq)
            pyperclip.copy(eq_ref)
            time.sleep(0.5)
            pyperclip.copy(eqtex)
        # 从剪切板存储图片到指定的文件夹后，产生对应的tex代码
        elif key == "5":
            texcode = self.mder.save_img_create_texcode()    
            pyperclip.copy(texcode)
        return key



class MainPageMenu(MenuItemSet):
    def __init__(self) -> None:
        super().__init__()

        # main page menu
        self.add_menu(
            "Cola UTools", 
            _1="Tex and Markdown", 
            _2="Run Some exe(TODO such as spider)",   # TODO
            _3="Chat with gpt"
        )    

        # test
        self.add_menu(
            "Test", 
        )
        
        self.add_menu(
            "这是一个中文测试!", 
            **{
                "_1": "这是测试，不要选呀！"
            }
        )

        # sub menu
        self.menu_texmd = ColaMDTexMenu(config_md2texer=config)
    
    def runloop(self):
        while True:
            try:
                key = self.getkey()
                if key == "1":
                    self.menu_texmd.runloop()
                elif key == "3":
                    chat_with_gpt()
                elif key == "help":
                    self.help()
                elif key == "exit":
                    break
            except Exception as ex:
                print(ex)
       
def main():
    menu_main = MainPageMenu()
    menu_main.runloop()


if __name__=="__main__":
    main()

"""
python main.py
"""
