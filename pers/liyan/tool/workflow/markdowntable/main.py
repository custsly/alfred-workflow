# -*- coding: UTF-8 -*-
import sys

sys.path.append(r'/Users/shiliyan/Workspace/python/tools/lib')
import pyperclip
from workflow import Workflow3
from wf_utils import workflow_util


def main():
    """
    读取剪贴板, 移除 \r, 按照 \n 拆分行, 按照 \t 拆分列, 转换为 markdown 格式的表格
    :return:
    """

    # 读取剪贴板内容
    txt = pyperclip.paste()

    if txt is None:
        txt = ''
    txt = txt.replace('\r', '')
    # 拆分成行
    row_list = txt.split('\n')
    # 再拆分一次
    sheet = list(map(lambda r: r.split('\t'), row_list))

    max_width_list = []
    # 得到每一列的最大宽度
    for row in sheet:
        for index, val in enumerate(row):
            if index < len(max_width_list):
                max_width_list[index] = max(len(val), max_width_list[index])
            else:
                max_width_list.append(len(val))

    # 根据长度向右填充字符
    for row in sheet:
        for index, val in enumerate(row):
            # 向右补全字符
            row[index] = val.ljust(max_width_list[index], ' ')

    # workflow
    wf = Workflow3()

    # 没有表头
    md_row_list = list(map(lambda r: '| ' + ' | '.join(r) + ' |', sheet))

    head_separator = '| ' + ' | '.join(list(map(lambda l: '-' * l, max_width_list))) + ' |'

    # 插入表头和数据分隔符
    md_row_list.insert(1, head_separator)

    markdown_table = '\n'.join(md_row_list)

    workflow_util.add_wf_item(wf, title=md_row_list[0], subtitle='Markdown Table', copytext=markdown_table)

    wf.send_feedback()


if __name__ == '__main__':
    main()
