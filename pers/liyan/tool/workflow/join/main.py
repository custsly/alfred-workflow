# -*- coding: UTF-8 -*-
import sys

sys.path.append(r'/Users/shiliyan/Workspace/python/tools/lib')
import pyperclip
from workflow import Workflow3
from wf_utils import workflow_util


def wrapper_with_symbol(txt_list, symbol="'"):
    """
    使用符号包装
    :param symbol: 包装的符号
    :param txt_list: 文本内容list
    :return: 返回
    """

    return map(lambda txt: symbol + txt + symbol, txt_list)


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
    txt = workflow_util.remove_blank_exclude_newline(txt)
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
        workflow_util.add_wf_item(wf, title=with_brackets, subtitle='with_brackets', copytext=with_brackets)
        # 去掉换行符
        one_line = ', '.join(txt_list)
        workflow_util.add_wf_item(wf, title=one_line, subtitle='one_line', copytext=one_line)
        # 去掉换行增加括号
        one_line_with_brackets = '(' + ', '.join(txt_list) + ')'
        workflow_util.add_wf_item(wf, title=one_line_with_brackets, subtitle='one_line_with_brackets',
                                  copytext=one_line_with_brackets)

        # joiner 不加空格
        # 去掉换行符
        one_line_no_space = ','.join(txt_list)
        workflow_util.add_wf_item(wf, title=one_line_no_space, subtitle='one_line_no_space', copytext=one_line_no_space)
        # 去掉换行增加括号
        one_line_with_brackets_no_space = '(' + ','.join(txt_list) + ')'
        workflow_util.add_wf_item(wf, title=one_line_with_brackets_no_space, subtitle='one_line_with_brackets_no_space',
                                  copytext=one_line_with_brackets_no_space)

        # 去重, 保留原始顺序
        txt_set = list(set(txt_list))
        txt_set.sort(key=txt_list.index)

        # 增加括号
        with_brackets_distinct = '(' + ',\n'.join(txt_set) + ')'
        workflow_util.add_wf_item(wf, title=with_brackets_distinct, subtitle='distinct_with_brackets',
                                  copytext=with_brackets_distinct)
        # 去掉换行符
        one_line_distinct = ', '.join(txt_set)
        workflow_util.add_wf_item(wf, title=one_line_distinct, subtitle='distinct_one_line', copytext=one_line_distinct)
        # 去掉换行增加括号
        one_line_with_brackets_distinct = '(' + ', '.join(txt_set) + ')'
        workflow_util.add_wf_item(wf, title=one_line_with_brackets_distinct, subtitle='distinct_one_line_with_brackets',
                                  copytext=one_line_with_brackets_distinct)

        # 去重, joiner 不加空格
        # 去掉换行符
        one_line_no_space_distinct = ','.join(txt_list)
        workflow_util.add_wf_item(wf, title=one_line_no_space_distinct, subtitle='one_line_no_space_distinct',
                                  copytext=one_line_no_space_distinct)
        # 去掉换行增加括号
        one_line_with_brackets_no_space_distinct = '(' + ','.join(txt_list) + ')'
        workflow_util.add_wf_item(wf, title=one_line_with_brackets_no_space_distinct,
                                  subtitle='one_line_with_brackets_no_space_distinct',
                                  copytext=one_line_with_brackets_no_space_distinct)

    wf.send_feedback()


if __name__ == '__main__':
    main()
