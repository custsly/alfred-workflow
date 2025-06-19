# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args):
    """
    读取剪贴板, repeat
    :param args 命令行参数, -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "c:")
    opts_dict = dict(opts)

    # 读取剪贴板内容
    txt = opts_dict.get('-c')
    txt = workflow_util.remove_whitespace_except_newlines(txt)
    txt_list = txt.split('\n')
    # 按照 / split, 长度填充为两位
    txt_list = map(lambda row: '-'.join(map(lambda n: n.rjust(2, '0'), row.split(r'/'))), txt_list)
    txt = '\n'.join(txt_list)

    # workflow
    wf = Workflow3()

    # split 得到的结果
    workflow_util.add_wf_item(wf, title='date format result', subtitle=repr(txt),
                              arg=txt)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
