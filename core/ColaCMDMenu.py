import os
import re
import platform

# cola
import utils.ColoryChar as ccc
import utils.ColaUtils as utils
from utils.ColaCMDIO import ColaCMDIO


class ColaCMDMenuItem:
    def __init__(self, name, len_max=80, **cmd_dict) -> None:
        self.len_max = len_max
        self.menu_name = name
        self.cmd_dict = self.init_cmd_dict(**cmd_dict)
    
    def init_cmd_dict(self, **kwargs):
        """
        NOTE: _1 -> number 1
        """ 
        rslt = dict()
        for key, value in kwargs.items():
            if key[0] == "_":
                key = key[1:]
            
            rslt[key] = value
        return rslt
    
    @staticmethod
    def len(s):
        return utils.calculate_print_length(s)
    
    def run_menu(self, key):
        if key in self.cmd_dict:
            keyfunc = self.cmd_dict[key][1]  # 执行函数
            if callable(keyfunc):
                ret = keyfunc()
                return True if ret is None else ret
        return False

    def __str__(self) -> str:
        rslts = []
        # show name
        n_rest = self.len_max - self.len(self.menu_name)- 2
        n_left_ = int(n_rest / 2)
        n_right_ = n_rest - n_left_
        s_name = "|{}{}{}|".format("-"*n_left_, self.menu_name, "-"*n_right_)
        rslts.append(s_name)

        # show dict
        for key, value in self.cmd_dict.items():
            dsc = value[0] if isinstance(value, list) else value  # TODO: delete it or keep?
            l_blank = self.len_max - self.len(key) - self.len(dsc) - 5
            s_dsc = "| {}: {}{}|".format(key, dsc, " "*l_blank)
            rslts.append(s_dsc)

        # end line
        s_end2 = "|{}|".format("=" * (self.len_max - 2))
        rslts.append(s_end2)
        rslt_s = "\n".join(rslts)
        return ccc.colory(rslt_s, ccc.GREEN)


"""
Page -> a set of Menu item 
"""
class MenuItemSet:
    def __init__(self, username="cola") -> None:
        self.menus = []
        self.helps = """\
- exit: exit this page.
- help: show help document.
- cls: clear terminal and show page.
- enter: show page.
"""
        self.username = username
        self.cmdio = ColaCMDIO()

    def add_helps(self, s):
        self.helps = self.helps + s

    def run_help(self):
        self.cmdio.out_info(self.helps)

    def new_key(self, key):
        """  # reprensente a, b, c ...
        _1 -> #1
        """
        if re.match(r'^_[0-9]+$', key):
            key = key[1:]

        assert len(key) < 10, "Length of key less than 10." 

        return 'abcdefghijk'[len(self.menus)] + key

    def process_cmd_dict(self, **cmd_dict):
        dict_new = dict()
        for key, value in cmd_dict.items():
            key_new = self.new_key(key) # a1, b2, 等通过首字母来区分不同的menu 
            dict_new[key_new] = value 
        return dict_new

    def add_menuAkeyfunc(self, name, **cmd_dict):
        """
        添加key: [description, keyfunction]
        """
        cmd_dict = self.process_cmd_dict(**cmd_dict)
        self.menus.append(
            ColaCMDMenuItem(name, **cmd_dict))

    def show(self):
        for menu in self.menus:
            print(menu)
        print("")
    
    def getkey(self):
        key = self.cmdio.getline_user(user=self.username, info="~")
        return key

    def clear_terminal(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')            
    
    def run_page(self, key):
        for menu in self.menus:
            ret = menu.run_menu(key)
            if ret:
                if ret == 2:
                    self.show()
                return True
        return False
    
    def _keyfunc_default(self, key):
        if key == "help":
            self.run_help()
            return True
        elif key == "cls":
            self.clear_terminal()
            self.show()
            return True
        elif key == "":
            self.show()
            return True
        # not right
        print(ccc.colory("Please input right command.", ccc.BOLD, ccc.RED)) 
        # self.show()
        return False
    
    def _keyfunc_none(self):
        """
        Do nothing function, just for help
        """
        print("TODO")

    def runloop(self):
        self.show()
        while True:
            key = self.getkey()
            if key == "exit":
                return 2
            is_run = self.run_page(key)
            if not is_run:
                is_run = self._keyfunc_default(key)


if __name__=="__main__":
    menu = ColaCMDMenuItem(
        "Name", 
        _1="tool 1", 
        l="list all file"
    )
    print(menu)
"""
python ColaCMDMenu.py
"""