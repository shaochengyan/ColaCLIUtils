import unicodedata

def calculate_print_length(s: str) -> int:
    # 统计字符串中字符数，中文算1字符，英文算1字符
    length = len(s)
    # 将 “中文字符” 的长度视为 2 个英文字符长度
    for char in s:
        if unicodedata.east_asian_width(char) in ('F', 'W'):
            length += 1
    return length

if __name__=="__main__":
    # 示例用法
    s = "hello, 你好，python"
    print("字符串长度（普通）:", len(s))
    print("字符串长度（全角）:", calculate_print_length(s))