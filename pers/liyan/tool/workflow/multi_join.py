# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def transpose_2d(data):
    transposed = []
    for i in range(len(data[0])):
        new_row = []
        for row in data:
            if len(row) > i:
                new_row.append(row[i])
        transposed.append(new_row)
    return transposed


def flow(args, clip_content):
    """
    读取剪贴板, 移除 \r, 按照 \n 拆分行, 按照 \t 拆分列, 使用给定的参数对所有列进行 join
    :param args 命令行参数, 1-字符串, 2-数值
    :param clip_content 剪贴板内容
    :return:
    """
    # 参数
    param = args[1]

    # 读取剪贴板内容
    txt = clip_content

    if txt is None:
        txt = ''
    txt = txt.replace('\r', '')
    # 拆分成行
    row_list = txt.split('\n')
    # 再拆分一次
    sheet = list(map(lambda row: row.split('\t'), row_list))
    # 移除每一行的空数据
    sheet = list(map(workflow_util.remove_blank_element, sheet))

    # workflow
    wf = Workflow3()

    if param == '1':
        # 字符串, 追加单引号
        sheet = list(map(lambda row: workflow_util.wrap_with_symbol(row), sheet))
    elif param == '2':
        # 不需要添加引号
        pass
    else:
        sheet = list(map(lambda row: workflow_util.wrap_with_symbol(row, param), sheet))

    # 转置处理
    sheet_transpose = transpose_2d(sheet)

    # 第一行增加左括号
    sheet[0] = list(map(lambda s: '(' + s, sheet[0]))
    # 最后一行增加右括号
    for i in range(0, len(sheet)):
        for j in range(0, len(sheet[i])):
            # 每列的最后一行增加右括号
            if i == len(sheet) - 1 or j + 1 > len(sheet[i + 1]):
                sheet[i][j] = sheet[i][j] + ')'
            else:
                # 其他的增加逗号
                sheet[i][j] = sheet[i][j] + ','

    # 按照原有excel行列格式处理
    excel_format = '\n'.join(map(lambda txt_list: '\t'.join(txt_list), sheet))
    workflow_util.add_wf_item(wf, title=excel_format, subtitle='excel_format', arg=excel_format)

    transpose_result = '\n'.join(map(lambda txt_list: ','.join(txt_list), sheet_transpose))
    workflow_util.add_wf_item(wf, title=transpose_result, subtitle='transpose_result', arg=transpose_result)

    #
    # # 为了防止有特殊字符导致粘贴到 excel 中不能正确分列, 每一个单元格使用双引号处理
    # # 增加括号
    # with_brackets = '\t'.join(map(lambda txt_list: '"(' + ',\n'.join(txt_list) + ')"', sheet))
    # workflow_util.add_wf_item(wf, title=with_brackets, subtitle='with_brackets', copytext=with_brackets)
    # # 去掉换行符
    # one_line = '\t'.join(map(lambda txt_list: '"' + ', '.join(txt_list) + '"', sheet))
    # workflow_util.add_wf_item(wf, title=one_line, subtitle='one_line', copytext=one_line)
    # # 去掉换行增加括号
    # one_line_with_brackets = '\t'.join(map(lambda txt_list: '"(' + ', '.join(txt_list) + ')"', sheet))
    # workflow_util.add_wf_item(wf, title=one_line_with_brackets, subtitle='one_line_with_brackets',
    #                           copytext=one_line_with_brackets)
    #
    # # joiner 不加空格
    # # 去掉换行符
    # one_line_no_space = '\t'.join(map(lambda txt_list: '"' + ','.join(txt_list) + '"', sheet))
    # workflow_util.add_wf_item(wf, title=one_line_no_space, subtitle='one_line_no_space', copytext=one_line_no_space)
    # # 去掉换行增加括号
    # one_line_with_brackets_no_space = '\t'.join(map(lambda txt_list: '"(' + ','.join(txt_list) + ')"', sheet))
    # workflow_util.add_wf_item(wf, title=one_line_with_brackets_no_space, subtitle='one_line_with_brackets_no_space',
    #                           copytext=one_line_with_brackets_no_space)

    wf.send_feedback()


def main():
    flow(sys.argv, pyperclip.paste())


if __name__ == '__main__':
    main()
