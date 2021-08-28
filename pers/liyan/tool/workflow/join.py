# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def flow(args, clip_content):
    """
    读取剪贴板, 移除空白行, 使用给定的参数进行 join
    :param args: 命令行参数, 1 - 字符串类型, 2 - 数值类型, 其他参数作为包装字符串的字符
    :param clip_content: 剪贴板内容
    :return:
    """
    # 参数
    param = args[1] if len(args) > 1 else '2'

    # 读取剪贴板内容
    txt = clip_content
    txt = workflow_util.remove_blank_exclude_newline(txt)
    txt_list = txt.split('\n')

    # workflow
    wf = Workflow3()

    if param == '1':
        # 字符串, 追加单引号
        txt_list = workflow_util.wrap_with_symbol(txt_list)
    elif param == '2':
        # 不需要添加引号
        pass
    else:
        txt_list = workflow_util.wrap_with_symbol(txt_list, param)

    # 增加括号
    with_brackets = '(' + ',\n'.join(txt_list) + ')'
    workflow_util.add_wf_item(wf, title=with_brackets, subtitle='with_brackets', arg=with_brackets)

    # 去掉换行符
    one_line = ', '.join(txt_list)
    one_line_item = workflow_util.add_wf_item(wf, title=one_line, subtitle='one_line', arg=one_line)
    # 不加空格
    one_line_no_space = ','.join(txt_list)
    one_line_item.add_modifier('alt', subtitle='one_line_no_space', arg=one_line_no_space, valid=True)

    # 去掉换行增加括号
    one_line_with_brackets = '(' + ', '.join(txt_list) + ')'
    one_line_with_brackets_item = workflow_util.add_wf_item(wf, title=one_line_with_brackets,
                                                            subtitle='one_line_with_brackets',
                                                            arg=one_line_with_brackets)
    # 不加空格
    one_line_with_brackets_no_space = '(' + ','.join(txt_list) + ')'
    one_line_with_brackets_item.add_modifier('alt', subtitle='one_line_with_brackets_no_space',
                                             arg=one_line_with_brackets_no_space, valid=True)

    # 去重, 保留原始顺序
    txt_set = list(set(txt_list))
    txt_set.sort(key=txt_list.index)

    # 只进行去重, 换行, 不增加其他分隔符
    distinct_with_line = '\n'.join(txt_set)
    workflow_util.add_wf_item(wf, title=distinct_with_line, subtitle='distinct_with_line',
                              arg=distinct_with_line)

    # 增加括号
    with_brackets_distinct = '(' + ',\n'.join(txt_set) + ')'
    workflow_util.add_wf_item(wf, title=with_brackets_distinct, subtitle='distinct_with_brackets',
                              arg=with_brackets_distinct)
    # 去掉换行符
    one_line_distinct = ', '.join(txt_set)
    one_line_distinct_item = workflow_util.add_wf_item(wf, title=one_line_distinct, subtitle='distinct_one_line',
                                                       arg=one_line_distinct)
    # 不加空格
    one_line_distinct_no_space = ','.join(txt_set)
    one_line_distinct_item.add_modifier('alt', subtitle='distinct_one_line_no_space',
                                        arg=one_line_distinct_no_space, valid=True)

    # 去掉换行增加括号
    one_line_with_brackets_distinct = '(' + ', '.join(txt_set) + ')'
    one_line_with_brackets_distinct_item = workflow_util.add_wf_item(wf, title=one_line_with_brackets_distinct,
                                                                     subtitle='distinct_one_line_with_brackets',
                                                                     arg=one_line_with_brackets_distinct)
    # 不加空格
    one_line_with_brackets_distinct_no_space = '(' + ','.join(txt_set) + ')'
    one_line_with_brackets_distinct_item.add_modifier('alt', subtitle='distinct_one_line_with_brackets_no_space',
                                                      arg=one_line_with_brackets_distinct_no_space, valid=True)

    wf.send_feedback()


def main():
    flow(sys.argv, pyperclip.paste())


if __name__ == '__main__':
    main()
