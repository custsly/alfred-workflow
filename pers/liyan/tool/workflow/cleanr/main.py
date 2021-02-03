# -*- coding: UTF-8 -*-
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


def remove_return(content):
    """
    替换 \r\n 为 \n
    :param content: 字符串
    :return: 替换后得到的字符串
    """
    return content.replace('\r\n', '\n')


def main():
    """
    join参数
    :return:
    """
    # 读取剪贴板内容
    txt = pyperclip.paste()
    txt = remove_return(txt)

    # 写入剪贴板
    pyperclip.copy(txt)

    # workflow
    wf = Workflow3()

    add_wf_item(wf, title=repr(txt), subtitle=r'replace \r\n with \n', copytext=txt, valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    main()
