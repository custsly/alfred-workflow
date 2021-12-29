# -*- coding: UTF-8 -*-
import getopt
import sys
import re

from wf_utils import workflow_util
from workflow import Workflow3


def remove_return(content):
    """
    替换换行符为空格
    :param content: 字符串
    :return: 替换后得到的字符串
    """
    return re.sub(r'\s*\n+\s*', ' ', content.replace('\r\n', '\n'))


def flow(args):
    """
    workflow主要方法, 替换剪贴板内容换行符为 空格
    :param args: 命令行参数 -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "c:")
    opts_dict = dict(opts)
    txt = remove_return(opts_dict.get('-c'))

    # workflow
    wf = Workflow3()

    workflow_util.add_wf_item(wf, title=repr(txt), subtitle=r'replace newline with space', arg=txt, valid=True)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
