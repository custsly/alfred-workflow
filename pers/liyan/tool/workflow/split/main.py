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
    移除空白, \t 空格, \n
    :param content: 字符串
    :return: 移除后的内容
    """
    if content is None:
        return ''
    return content.replace('\t', '') \
        .replace(' ', '') \
        .replace('\r', '') \
        .replace('\n', '') \
        .strip()


def un_wrap_brackets(text):
    """
    移除两端的括号
    :param text:
    :return:
    """
    if text is None:
        return ''
    return text.strip('(').strip(')')


def un_wrap_quote(text):
    """
    移除两端的单引号
    :param text:
    :return:
    """
    if text is None:
        return ''
    return text.strip("'")


def main():
    """
    读取剪贴板, split 参数
    :return:
    """
    # split的字符串, 默认值 ,
    splitter = ','
    if len(sys.argv) > 1 and sys.argv[1]:
        splitter = sys.argv[1]

    # 读取剪贴板内容
    txt = pyperclip.paste()
    # 移除空白字符
    txt = remove_blank(txt)
    # 移除两端的括号
    txt = un_wrap_brackets(txt)

    txt_list = txt.split(splitter)

    # workflow
    wf = Workflow3()

    split_result = '\n'.join(txt_list)

    # split 得到的结果
    add_wf_item(wf, title=split_result, subtitle="splitter with " + splitter, copytext=split_result)

    # 移除两端的单引号
    split_unwrap_list = map(un_wrap_quote, txt_list)
    split_unwrap_result = '\n'.join(split_unwrap_list)
    add_wf_item(wf, title=split_unwrap_result, subtitle="splitter with %s, unwrap quote" % splitter,
                copytext=split_unwrap_result)

    wf.send_feedback()


if __name__ == '__main__':
    main()
