import os
import pyperclip
import re
import time
import shutil

# PIL
from PIL import ImageGrab
from PIL import Image

# cola import
from plugins.TexMD.TexUtils import ColaTexGenerator
from utils.ColaLogger import ColaLogger

class ColaMD2Tex:
    def __init__(self, dir_mdfile="./", dir_img_save="./") -> None:
        self.tex_gen = ColaTexGenerator()
        self.dir_mdfile = dir_mdfile  # dir of markdown file
        self.dir_img_save = dir_img_save
        self.logger = ColaLogger("log_mdtex_utils")

    @staticmethod
    def check_is_list(line: str):
        return line[:2] == "- "
    
    @staticmethod
    def check_is_2dollar(line: str):
        return line[:2] == "$$" 
    
    @staticmethod
    def check_is_quote(line: str):
        return line[:4] == "> - "  # must list in quote
    
    def process_img_line(self, line: str, is_copy=False):
        # var
        pattern = re.compile("\!\[.*\]\((.*)\)")
        img_path = pattern.findall(line)
        if len(img_path) == 0:
            return line  # not img -> return origin line

        # copy img
        if is_copy:
            assert os.path.isdir(self.dir_img_save)
        filepath_rl = img_path[0]
        filename = os.path.basename(filepath_rl)
        info_img = ""
        if is_copy:
            fp_full = os.path.join(self.dir_mdfile, filepath_rl)
            if not os.path.isfile(fp_full):
                self.logger.info("No imag: {}".format(fp_full), is_print=True)

            else:
                fp_save = os.path.join(self.dir_img_save, filename)  
                info_img = "{} -> {}".format(fp_full, fp_save)
                self.logger.info(info_img, is_print=True)
                shutil.copyfile(fp_full, fp_save) 

        # text code
        tex_code = self.tex_gen.get_tex_img(filename)
        return "% {}\n{}".format(info_img, tex_code)

    def proces_line_base(self, line, env_start_bf="pptextbf", env_other_bf="bluetextbf"):
        """
        base md to latex
            - **** -> pptextbf
        """
        # ^**{}** -> pptextbf
        pattern = re.compile(r"^\*\*(.*?)\*\*")
        line = re.sub(pattern, r"\\" + env_start_bf + r"{\1}", line)

        # for other bf
        pattern = re.compile(r"\*\*(.*?)\*\*")
        line = re.sub(pattern, r"\\" + env_start_bf + r"{\1}", line)

        # -> to $rightarrow$
        line = re.sub("->", "$rightarrow$", line)
        line = re.sub("<-", "$leftarrow$", line)

        return line

    def process_quote_lines(self, lines):
        lines = [line[2:] for line in lines]
        return self.process_list_lines(lines, env="colaQuote")

    def process_list_lines(self, lines, env="enumerate"):
        """
        lines: list of str
        """
        lines_new = ["\t\\item " + self.proces_line_base(line[2:], env_start_bf="bluetextbf") for line in lines]
        rslt = "\\begin{{{}}}\n{}\n\\end{{{}}}".format(env, "\n".join(lines_new), env)
        return rslt

    @staticmethod
    def _get_right(lines, end, check_func, N):
        while end < N:
            if check_func(lines[end]):
                end += 1
            else:
                break
        return end

    def special_characters_to_replace(self, s:str):
        return s
       
    def mdtext2tex(self, s_md, is_clip=True):
        # replace special characters
        s_md = self.special_characters_to_replace(s_md)

        # step1 split to lines
        lines = [ line for line in s_md.split(sep='\n') if len(line) > 0 ]

        # step2 loop process the lines
        N = len(lines)
        i = 0


        rslts = []
        while i < N:
            # 1. process list
            if self.check_is_list(lines[i]):
                end_list = self._get_right(lines, end=i + 1, check_func=self.check_is_list, N=N)
                rslt_tex = self.process_list_lines(lines[i:end_list], env="enumerate")
                rslts.append(rslt_tex)
                i = end_list
                continue

            # 2. process quote 
            if self.check_is_quote(lines[i]):
                end_quote = self._get_right(lines, end=i + 1, check_func=self.check_is_quote, N=N)
                rslt_tex = self.process_quote_lines(lines[i:end_quote])
                rslts.append(rslt_tex)
                i = end_quote
                continue

            # 2+1. process $$equatio$$
            if self.check_is_2dollar(lines[i]):
                end_dollar = i + 1
                while end_dollar < N and not self.check_is_2dollar(lines[end_dollar]):
                    end_dollar += 1
                # [i, end_dollar)  
                eq_tex = "\n".join(lines[i+1:end_dollar])
                eq_tex = self.tex_gen.get_tex_eq(eq_tex)[0]
                rslts.append(eq_tex)
                i = end_dollar + 1  # pass last $$
                continue

            line = lines[i]
            # 3. process img
            line = self.process_img_line(line, is_copy=True)

            # 3. process one line
            line = self.proces_line_base(line)
            rslts.append(line)

            i += 1
        rslt_tex = "\n\n".join(rslts)
        if is_clip:
            pyperclip.copy(rslt_tex)
        return rslt_tex
    
    def save_img_create_texcode(self):
        """ get img from clip -> save to target dir -> gen texcode
        """
        # 获取屏幕截图
        screenshot = ImageGrab.grabclipboard()
        filename = time.strftime("mdimg_%Y%m%d-%H%M%S.png", time.localtime())
        save_path = os.path.join(self.dir_img_save, filename)

        # 检查剪贴板中是否包含图像
        if screenshot is not None and isinstance(screenshot, Image.Image):
            # 将图像保存到指定文件路径
            self.logger.info("Save image to: {}".format(save_path), is_print=True)
            screenshot.save(save_path)
        else:
            self.logger.info('clipboard does not contain effective image.', is_print=True)
        tex_code = self.tex_gen.get_tex_img(filename)
        return tex_code

if __name__=="__main__":
    mder = ColaMD2Tex("./", "./tmp")
    rslt = mder.mdtext2tex("**cdas**")
    print(rslt)

"""
python -m plugins.TexMD.MD2Tex
"""