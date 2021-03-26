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
    operation = sys.argv[1].lower()

    # 读取剪贴板内容
    txt = pyperclip.paste()
    # 移除空白字符
    txt = remove_blank(txt)
    txt_list = txt.split('\n')
    # workflow
    wf = Workflow3()

    try:
        # 使用字符包装
        number_list = map(int, txt_list)

        result = None
        # 计算
        if operation == 'sum':
            result = sum(number_list)
        elif operation == 'avg':
            result = sum(number_list) / len(number_list)
        else:
            result = "unknown operation " + operation
    except Exception as e:
        result = "error " + str(e.args)

    add_wf_item(wf, title=result, subtitle="operation result", copytext=result)

    wf.send_feedback()


if __name__ == '__main__':
    main()
