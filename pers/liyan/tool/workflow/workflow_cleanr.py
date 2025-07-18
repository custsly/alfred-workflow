# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args):
    """
    workflow主要方法, 替换剪贴板内容 \r\n 为 \n
    :param args: 命令行参数 -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "c:")
    opts_dict = dict(opts)
    txt = workflow_util.normalize_newlines(opts_dict.get('-c'))

    # workflow
    wf = Workflow3()

    workflow_util.add_wf_item(wf, title=repr(txt), subtitle=r'replace \r\n with \n', arg=txt, valid=True)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
