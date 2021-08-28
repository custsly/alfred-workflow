# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def flow(args, clip_content):
    """
    包装字符串, 按照换行 /n 切分之后包装
    :param args 命令行参数, 包装的字符串, 默认 ,
    :param clip_content 剪贴板内容
    :return:
    """

    # 包装的字符串
    wrapper = ''
    if len(args) > 1:
        wrapper = args[1]

    # 读取剪贴板内容
    txt = clip_content
    # 移除空白字符
    txt = workflow_util.remove_blank_exclude_newline(txt)
    txt_list = txt.split('\n')
    # 使用字符包装
    txt_list = map(lambda x: wrapper + x + wrapper, txt_list)

    # workflow
    wf = Workflow3()

    # result
    result = '\n'.join(txt_list)

    workflow_util.add_wf_item(wf, title=result, subtitle="wrapper with " + wrapper, copytext=result)

    wf.send_feedback()


def main():
    flow(sys.argv, pyperclip.paste())


if __name__ == '__main__':
    main()
