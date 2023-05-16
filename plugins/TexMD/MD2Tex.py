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
    def check_is_code(line: str):
        return line[:3] == "```"
    
    @staticmethod
    def check_is_quote(line: str):
        return line[:4] == "> - "  # must list in quote
    
    def get_image_path(self, line:str):
        img_path = re.findall("\!\[.*\]\((.*)\)", line)
        if len(img_path) == 0:
            img_path = re.findall(r"<img src=\"(.*?)\".*/>", line)
        
        if len(img_path) > 0:
            return img_path[0]
        else:
            return ""


    def process_img_line(self, line: str, is_copy=False):
        # var
        img_path = self.get_image_path(line)   
        if len(img_path) == 0:
            return line  # not img -> return origin line

        # copy img
        if is_copy:
            assert os.path.isdir(self.dir_img_save)
        fp_full = img_path if os.path.isfile(img_path) else os.path.join(self.dir_mdfile, img_path)
        filename = os.path.basename(img_path)
        info_img = ""
        if is_copy:
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
        line = re.sub("->", r"$\\rightarrow$", line)
        line = re.sub("<-", r"$\\leftarrow$", line)

        return line

    def process_quote_lines(self, lines):
        lines = [line[2:] for line in lines]
        lines_new = ["\t\\item " + self.proces_line_base(line[2:], env_start_bf="bluetextbf") for line in lines]
        rslt = "\\begin{{{}}}\n{}\n\\end{{{}}}\n".format("colaQuote", "\n".join(lines_new), "colaQuote")
        return rslt
    

    def process_enumerate(self, lines):
        """
        lines: list of str
        """
        lines_new = ["\t\\item " + self.proces_line_base(line[2:], env_start_bf="bluetextbf") for line in lines]
        rslt = "\\begin{{enumerate}}[leftmargin=4em,itemindent=1em, label=$\\bullet$]\n{}\n\\end{{enumerate}}".format("\n".join(lines_new))
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
                rslt_tex = self.process_enumerate(lines[i:end_list])
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
            
            # 2+2. process code
            if self.check_is_code(lines[i]):
                type_code = lines[i][3:]
                end_code = i + 1
                while end_code < N and not self.check_is_code(lines[end_code]):
                    end_code += 1
                # [i, end_code)  
                code_tex = "\n".join(lines[i+1:end_code])
                code_tex = self.tex_gen.get_tex_code(code_tex, type_code=type_code)
                rslts.append(code_tex)
                i = end_code + 1  # pass last ```
                continue

            line = lines[i]
            # 3. process img
            line = self.process_img_line(line, is_copy=True)

            # 3. process one line
            line = self.proces_line_base(line)
            rslts.append(line)

            i += 1
        rslt_tex = "\n".join(rslts)
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

smd = r"""

### **OverLook** 

**一句话** 设计了一个FPN网络来从点云中提取关键点及其显著性，并设计了训练框架使得该网络的关键点具备重复性(点越显著，则重复性越高)

### **训练流程**

![image-20221219143817930](ColaNote_USIP(无监督点云关键点检测).assets/image-20221219143817930.png)

- 分别将原始点云和变换后的点云输入FPN -> M个关键点及其不确定度
- **$\mathcal{L}_c $(probabilistic chamfer loss)** 最小化两个关键点集对应点之间的距离
- **$\mathcal{L}_p$(Point-to-Point Loss)** 用于最小化估计的关键点与其周围邻居的距离(限制关键点不能超出点云)

### **FPN网络架构**

FPS采样M个点S -> 利用point-to-node获得Si周围ki个点(每个group大小不同) -> 规范化每一个group(去中心 -> 簇与平移变换无关) -> 送入PointNet-like网络获得groupSm的特征向量Gm -> 基于kNN的grouping layer作用在特征向量上获得层次信息的集成 -> M个特征向量 -> 送入MLP估计出M个关键点和不确定度 -> 去规范化(给每一关键点加上对应的平移向量) -> 输出坐标点以及不确定度 $\{(Q, \Sigma)\}$

<img src="D:/DData/1.StudyMain/5.GraduationProject/ColaModelPCR/USIP/ColaNote_USIP(无监督点云关键点检测).assets/image-20221219143817930.png" alt="image-20221219152758762" style="zoom: 80%;" />
---------

```python
import os
import time
import pyperclip

from core.ColaCMDMenu import MenuItemSet
from .MD2Tex import ColaMD2Tex
from .TexUtils import ColaTexGenerator

class ColaMDTexPage(MenuItemSet):
    def __init__(self, **config_md2texer) -> None:
        super().__init__(is_page_dif_prefix=False)
        self.mder = ColaMD2Tex(**config_md2texer)
        self.texer = ColaTexGenerator()
```
> - **NOTE** 测试
> - **NOTE** 测试

- **NOTE** 测试
- **NOTE** 测试
"""

if __name__=="__main__":
    mder = ColaMD2Tex("./", "./tmp")
    rslt = mder.mdtext2tex(smd, is_clip=True)
    # print(rslt)

"""
python -m plugins.TexMD.MD2Tex
"""