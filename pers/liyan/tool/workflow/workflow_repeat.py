# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args):
    """
    读取剪贴板, repeat
    :param args 命令行参数, -a 重复次数, -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "a:c:")
    opts_dict = dict(opts)

    # 重复次数
    count = 1
    if opts_dict.get('-a'):
        try:
            count = int(args[1])
        except ValueError as e:
            pass

    # 读取剪贴板内容
    txt = opts_dict.get('-c')

    repeat_result = txt * count

    # workflow
    wf = Workflow3()

    # split 得到的结果
    workflow_util.add_wf_item(wf, title='repeated result', subtitle="%s * %s" % (repr(txt), count),
                              arg=repeat_result)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
