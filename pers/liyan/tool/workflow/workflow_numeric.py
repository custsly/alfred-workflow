# -*- coding: UTF-8 -*-
import getopt
import re
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def remove_non_digits(string):
    return re.sub(r'\D', '', string)


def flow(args):
    """
    workflow主要方法, 移除剪贴板内容非非数字字符
    :param args: 命令行参数 -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "c:")
    opts_dict = dict(opts)
    origin_txt = opts_dict.get('-c')
    result_txt = remove_non_digits(origin_txt)

    # workflow
    wf = Workflow3()

    workflow_util.add_wf_item(wf, title=repr(result_txt), subtitle=r'origin str %s' % repr(origin_txt), arg=result_txt,
                              valid=True)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
