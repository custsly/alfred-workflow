# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def flow(args, clip_content):
    """
    读取剪贴板, split 参数
    :param args 命令行参数, 切分的分隔符, 默认 ,
    :param clip_content 剪贴板内容
    :return:
    """

    # split的字符串, 默认值 ,
    splitter = ','
    if len(args) > 1 and args[1]:
        splitter = args[1]

    # 读取剪贴板内容
    txt = clip_content
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
    flow(sys.argv, pyperclip.paste())


if __name__ == '__main__':
    main()
