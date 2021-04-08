# -*- coding: UTF-8 -*-
import sys
import pyperclip
from workflow import Workflow3


def add_wf_item(wf, title, subtitle=None, copytext=None, valid=True):
    """
    workflow 增加 item
    :param wf: workflow
    :param title: title
    :param subtitle: subtitle
    :param copytext: copytext
    :param valid: valid
    :return:
    """
    wf.add_item(title=title, subtitle=subtitle, valid=valid, copytext=copytext)


def remove_blank(content):
    """
    移除空白, /t 空格
    :param content: 字符串
    :return: 移除后的内容
    """
    if content is None:
        return ''
    return content.replace('\t', '') \
        .replace(' ', '') \
        .replace('\r', '') \
        .strip()


def main():
    """
    join参数
    :return:
    """
    # 包装的字符串
    wrapper = ''
    if len(sys.argv) > 1:
        wrapper = sys.argv[1]

    # 读取剪贴板内容
    txt = pyperclip.paste()
    # 移除空白字符
    txt = remove_blank(txt)
    txt_list = txt.split('\n')
    # 使用字符包装
    txt_list = map(lambda x: wrapper + x + wrapper, txt_list)

    # workflow
    wf = Workflow3()

    # result
    result = '\n'.join(txt_list)

    add_wf_item(wf, title=result, subtitle="wrapper with " + wrapper, copytext=result)

    wf.send_feedback()


if __name__ == '__main__':
    main()
