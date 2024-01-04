# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args):
    """
    移除 \r, 按照 \n 拆分行, 按照 \t 拆分列, 转换为 markdown 格式的表格
    :param args: -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "c:")
    opts_dict = dict(opts)
    # 读取剪贴板内容
    txt = opts_dict.get('-c')

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

    workflow_util.add_wf_item(wf, title=md_row_list[0], subtitle='Markdown Table', arg=markdown_table)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
