# -*- coding: UTF-8 -*-
import re
import sys
import pyperclip


def main():
    """
    生成sql in 参数
    :return:
    """
    # 读取剪贴板内容
    txt = pyperclip.paste()
    print(repr(txt))
    # pyperclip.copy(txt)
    # print('write clipboard finish')


if __name__ == '__main__':
    main()
