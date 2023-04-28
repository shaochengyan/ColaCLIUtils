Utils for use latex and latex with markdown. 

# CLI(up to 2023年4月28日)

**主界面**

![image-20230428184657031](readme.assets/image-20230428184657031.png)

**GPT聊天**

![image-20230428184835539](readme.assets/image-20230428184835539.png)

**Latex与Markdown的工具库**

![image-20230428184904002](readme.assets/image-20230428184904002.png)


# 日志(up to 2023年4月28日)
2023年4月28日
- 加入ChatGPT的选项，用户需要在config.yaml中写入以下内容
  - api key 会失效！ 需要进入 [web](https://platform.openai.com/account/api-keys) 重新申请!
``` yaml
api_key: <Your API Key>
```
- 加入多层目录，顶层为`MainPageMenu`控制，其可以理解为一个文件夹，下面可以存放很多文件(对应于多个menu)，然后可以递归调用其余目录
  - 每一个目录都是一个`MenuItemSet`: 即由多个目录构成的集合
  - 每次构造一个目录时，需要继承于`MenuItemSet`，然后调用`add_menu`添加选项(TODO: 添加选项的语法)(可以调用多次), 然后需要重新实现`runloop`函数，其内部是while循环，不断读取键盘输入，然后作出对应响应

# TODO
- [ ] ...

# 使用说明(quick start)(up to 2023年4月27日)
```shell
conda activate you env
python main.py
```
You should see:
```shell
> python main.py
|---------------------------------Markdown2Tex---------------------------------|
| (1): Clipboard markdown to latex code                                        |
| (2): Input markdown specified file, and store it into latex code (todo)      |
|______________________________________________________________________________|
|______________________________________________________________________________|
|----------------------------------Tex Utils-----------------------------------|
| (3): Generate random lable                                                   |
| (4): Clear equation with dollar(from clip)                                   |
| (5): Save image and copy texcode (image from clip)                           |
|______________________________________________________________________________|
|______________________________________________________________________________|


Input: 
```
功能说明
1. 从剪切板读取markdown语句，然后转为latex代码(仅转换指定格式)
2. TODO: 指定markdown文件 -> 转为对应的latex文件
3. 产生随机标签
4. 清除由AxMath复制latex代码过来时的双$$符号
5. 从剪切板存储图片到指定的文件夹后，产生对应的tex代码

> - NOTE: 输入`q`是退出

## an example
Now my clipboard contain a str:
``` markdown
**要点** 这是要点

**key2** this is key2

**list**

- item 1
- item 2

其他文字

**结束**
```

after Input 1, my clipboard contain:
``` latex
\pptextbf{要点} 这是要点



\pptextbf{key2} this is key2



\pptextbf{list}



\begin{enumerate}
	\item item 1
	\item item 2
\end{enumerate}



其他文字



\pptextbf{结束}
```

### Input: 3

```latex
\label{oWeb3PhTO8CvS_apDkrm}
```

### Input: 4:
clipboard contain:
```latex
$$
  E = mc\\
  p = 1
$$
```
after input 4:
```latex
\begin{equation}
E = mc\\
  p = 1
 \label{eq:Iwait}
\end{equation}
```

# git
```shell
git add .
git commit -m "upload"
git branch -M main
# git remote add origin https://github.com/shaochengyan/ColaCLIUtils.git
git push -u origin main
```

# 需求记录
## MD TO Latex需求
> - **场景** 首先在markdown中按照一定的格式写，然后通过代码将其转换为对应的latex代码。
> - **原理** 通过正则表达式匹配目标字符串 -> 替换为指定字符串
**转换场景**
- 以加粗字符串为开的句子，将其开头的用latex的`\pptextbf`包裹
  - 正文内容的list -> 用latex的`enumerate`环境包裹
- 正文引用内容的list -> 用latex的`colaQuote`环境包裹
  - 先暂时不考虑多层list

# CODE
- [main.py](./main.py) 主程序
    - [MD2Tex.py](MD2Tex.py) 函数族:获得字符串 -> 处理 -> 返回 -> 这样的一些函数族(module: md_to_latex)
- [ColaCMDMunu.py](ColaCMDMenu.py) 以name+cmd_dict构成一个menu_item，
- [test.py](./test.py) 测试程序
  - [test.ipynb](test.ipynb)对应的测试notebook