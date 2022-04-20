# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from workflow import Workflow3


def un_tab(content):
    """

    :param content: 字符串
    :return: 处理后后得到的字符串
    """

    content = content.replace('\r\n', '\n')
    if not content:
        return content
    rows = content.split('\n')
    if len(rows) == 1:
        # 第一行, 移除开头的空白字符t
        return rows[0].lstrip(' \t')

    rows_new = [rows[0].lstrip(' \t')]
    # 后面的行数按照最后一行的空白字符数进行删除
    right_space_index = -1
    for c in rows[-1]:
        if c == ' ' or c == '\t':
            right_space_index += 1

    for row in rows[1:]:
        rows_new.append(row[right_space_index:])
    return '\n'.join(rows_new)


def flow(args):
    """
    workflow主要方法, 移除开头的缩进
    :param args: 命令行参数 -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "c:")
    opts_dict = dict(opts)
    txt = un_tab(opts_dict.get('-c'))

    # workflow
    wf = Workflow3()

    workflow_util.add_wf_item(wf, title=repr(txt), subtitle=r'untab result', arg=txt, valid=True)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
