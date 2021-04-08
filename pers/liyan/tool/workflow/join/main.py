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


def wrapper_with_symbol(txt_list, symbol="'"):
    """
    使用符号包装
    :param symbol: 包装的符号
    :param txt_list: 文本内容list
    :return: 返回
    """

    return map(lambda txt: symbol + txt + symbol, txt_list)


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
    读取剪贴板, 移除空白行, 使用给定的参数进行 join
    :return:
    """
    # 参数
    param = sys.argv[1]
    valid = True

    # 读取剪贴板内容
    txt = pyperclip.paste()
    txt = remove_blank(txt)
    txt_list = txt.split('\n')

    # workflow
    wf = Workflow3()

    if param == '1':
        # 字符串, 追加单引号
        txt_list = wrapper_with_symbol(txt_list)
    elif param == '2':
        # 不需要添加引号
        pass
    else:
        txt_list = wrapper_with_symbol(txt_list, param)

    if valid:
        # 增加括号
        with_brackets = '(' + ',\n'.join(txt_list) + ')'
        add_wf_item(wf, title=with_brackets, subtitle='with_brackets', copytext=with_brackets)
        # 去掉换行符
        one_line = ', '.join(txt_list)
        add_wf_item(wf, title=one_line, subtitle='one_line', copytext=one_line)
        # 去掉换行增加括号
        one_line_with_brackets = '(' + ', '.join(txt_list) + ')'
        add_wf_item(wf, title=one_line_with_brackets, subtitle='one_line_with_brackets',
                    copytext=one_line_with_brackets)

        # joiner 不加空格
        # 去掉换行符
        one_line_no_space = ','.join(txt_list)
        add_wf_item(wf, title=one_line_no_space, subtitle='one_line_no_space', copytext=one_line_no_space)
        # 去掉换行增加括号
        one_line_with_brackets_no_space = '(' + ','.join(txt_list) + ')'
        add_wf_item(wf, title=one_line_with_brackets_no_space, subtitle='one_line_with_brackets_no_space',
                    copytext=one_line_with_brackets_no_space)

        # 去重, 保留原始顺序
        txt_set = list(set(txt_list))
        txt_set.sort(key=txt_list.index)

        # 增加括号
        with_brackets_distinct = '(' + ',\n'.join(txt_set) + ')'
        add_wf_item(wf, title=with_brackets_distinct, subtitle='distinct_with_brackets', copytext=with_brackets_distinct)
        # 去掉换行符
        one_line_distinct = ', '.join(txt_set)
        add_wf_item(wf, title=one_line_distinct, subtitle='distinct_one_line', copytext=one_line_distinct)
        # 去掉换行增加括号
        one_line_with_brackets_distinct = '(' + ', '.join(txt_set) + ')'
        add_wf_item(wf, title=one_line_with_brackets_distinct, subtitle='distinct_one_line_with_brackets',
                    copytext=one_line_with_brackets_distinct)

        # 去重, joiner 不加空格
        # 去掉换行符
        one_line_no_space_distinct = ','.join(txt_list)
        add_wf_item(wf, title=one_line_no_space_distinct, subtitle='one_line_no_space_distinct', copytext=one_line_no_space_distinct)
        # 去掉换行增加括号
        one_line_with_brackets_no_space_distinct = '(' + ','.join(txt_list) + ')'
        add_wf_item(wf, title=one_line_with_brackets_no_space_distinct, subtitle='one_line_with_brackets_no_space_distinct',
                    copytext=one_line_with_brackets_no_space_distinct)

    wf.send_feedback()
    # print(txt)
    # pyperclip.copy(txt)
    # print('write clipboard finish')


if __name__ == '__main__':
    main()
