import os
from termcolor import colored

# cola
import ColoryChar as ccc
import ColaUtils as utils


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
            l_blank = self.len_max - self.len(key) - self.len(value) - 7
            s_value = "| ({}): {}{}|".format(key, value, " "*l_blank)
            rslts.append(s_value)

        # end line
        s_end2 = "|{}|".format("=" * (self.len_max - 2))
        rslts.append(s_end2)
        rslt_s = "\n".join(rslts)
        return ccc.colory(rslt_s, ccc.GREEN)


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