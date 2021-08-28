# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def flow(args, clip_content):
    """
    读取剪贴板, repeat
    :param args 命令行参数, 重复次数
    :param clip_content 剪贴板内容
    :return:
    """
    # split的字符串, 默认值 ,
    count = 1
    if len(args) > 1 and args[1]:
        try:
            count = int(args[1])
        except ValueError as e:
            pass

    # 读取剪贴板内容
    txt = clip_content

    repeat_result = txt * count

    # workflow
    wf = Workflow3()

    # split 得到的结果
    workflow_util.add_wf_item(wf, title='repeated result', subtitle="%s * %s" % (repr(txt), count),
                              arg=repeat_result)

    wf.send_feedback()


def main():
    flow(sys.argv, pyperclip.paste())


if __name__ == '__main__':
    main()
