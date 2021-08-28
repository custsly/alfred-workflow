# -*- coding: UTF-8 -*-

import pyperclip
from workflow import Workflow3

from wf_utils import workflow_util


def remove_return(content):
    """
    替换 \r\n 为 \n
    :param content: 字符串
    :return: 替换后得到的字符串
    """
    return content.replace('\r\n', '\n')


def flow(args, clip_content):
    """
    workflow主要方法, 替换剪贴板内容 \r\n 为 \n
    :param args: 命令行参数
    :param clip_content: 剪贴板内容
    :return:
    """
    txt = remove_return(clip_content)

    # workflow
    wf = Workflow3()

    workflow_util.add_wf_item(wf, title=repr(txt), subtitle=r'replace \r\n with \n', arg=txt, valid=True)

    wf.send_feedback()


def main():
    flow([], pyperclip.paste())


if __name__ == '__main__':
    main()
