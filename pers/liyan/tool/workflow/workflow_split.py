# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args):
    """
    读取剪贴板, split 参数
    :param args 命令行参数, -a 切分的分隔符, 默认 , -c 剪贴板的内容
    :return:
    """

    # 参数
    opts, _ = getopt.getopt(args, "a:c:")
    opts_dict = dict(opts)

    # split的字符串, 默认值 ,
    splitter = ',' if not opts_dict.get('-a') else opts_dict.get('-a')

    # 读取剪贴板内容
    txt = opts_dict.get('-c')
    # 移除空白字符
    txt = workflow_util.remove_blank(txt)
    # 移除两端的括号
    txt = workflow_util.un_wrap_brackets(txt)

    txt_list = txt.split(splitter)

    # workflow
    wf = Workflow3()

    split_result = '\n'.join(txt_list)

    # split 得到的结果
    workflow_util.add_wf_item(wf, title=split_result, subtitle="splitter with " + splitter, arg=split_result)

    # 移除两端的单引号
    split_unwrap_list = map(workflow_util.un_wrap_quote, txt_list)
    split_unwrap_result = '\n'.join(split_unwrap_list)
    workflow_util.add_wf_item(wf, title=split_unwrap_result, subtitle="splitter with %s, unwrap quote" % splitter,
                              arg=split_unwrap_result)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
