import random

class ColaTexGenerator:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_tex_img(imgname, hspace=0.0, width=0.6):
        tex_code = r"""\begin{{figure}}[htbp]
    \centering
    \hspace*{{-{}cm}}\includegraphics[width={}\textwidth]{{{}}}
    \caption{{}}
    \label{{fig:{}}}
\end{{figure}}\n""".format(hspace, width, imgname, ColaTexGenerator.generate_random_label(l=10)) 
        return tex_code

    @staticmethod
    def clear_wrapper_const_char(s:str, char_wrapper="$"):
        """
        清除掉markdown中一些常量字符串的wrapper，例如
            - **acd** -> acd
            - `a` -> a 
        """
        s = s.strip()
        # clear $$\naccd\n$
        while s[0] == char_wrapper:
            s = s[1:]
        while s[-1] == char_wrapper:
            s = s[:-1]
        s = s.strip()
        return s


    def get_tex_eq(self, eq: str, env="equation", is_label=True) -> str:
        """
        eq: c
        env: 使用的环境equation | equation*
        is_label: 是否添加label
        """
        eq = self.clear_wrapper_const_char(eq)
        label = "eq:{}".format(ColaTexGenerator.generate_random_label())
        # 添加了eqaution环境的latex公式
        rslt_eq = "\\begin{{{}}}\n{}\n {}\n\\end{{{}}}\n".format(
            env,
            eq,
            "\\label{{{}}}".format(label) if is_label else "",
            env
            )
        # 用于引用该公式的ref公式
        rslt_ref_label = "式$\\ref{{{}}}$".format(label)
        return rslt_eq, rslt_ref_label
    
    def get_tex_code(self, code: str, type_code="python", caption=""):
        # print(code)
        rslt = """\\begin{{lstlisting}}[language={},caption={}]\n{}\n
\end{{lstlisting}}\n""".format(type_code, caption, code)
        # print(rslt)
        return rslt

    @staticmethod
    def generate_random_label(l=5):
        # generate randome label
        return ''.join(random.sample(
        list("abcdefghijklmnopqrstuvwxyz" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + "1234567890" + "_"),
        l))

