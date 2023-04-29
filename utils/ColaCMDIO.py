from . import ColoryChar as ccc
import platform

"""
想构建一个模拟terminal的字符串，可以获取输入，以一定格式显示输入！
"""


class ColaCMDIO:
    def __init__(self) -> None:
        pass


    def getline_user(self, user="", info=""):
        """
        just input line.
        """
        # show terminal
        msg = "{}{}".format(
            ccc.colory("{}@{}".format(user, platform.system()), ccc.BOLD, ccc.GREEN), 
            ccc.colory(" {}$ ".format(info) , ccc.BOLD, ccc.BLUE)
        )
        s = input(msg)
        return s
    
    def out_info(self, info):
        msg = ccc.colory(info, ccc.YELLOW, ccc.BOLD)
        print(msg)
    
    def out_pair(self, key, value):
        msg = "{}: {}".format(
            ccc.colory(key, ccc.PURPLE, ccc.BOLD), 
            ccc.colory(value, ccc.CYAN)
        )
        print(msg)

if __name__=="__main__":
    cmdio = ColaCMDIO()
    cmdio.out_pair("chatgpt", "好的!")


"""
python -m utils.ColaCMDIO
"""