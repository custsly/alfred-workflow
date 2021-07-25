# -*- coding: UTF-8 -*-

import pyperclip
from wf_utils import workflow_util
from workflow import Workflow3


def remove_return(content):
    """
    替换 \r\n 为 \n
    :param content: 字符串
    :return: 替换后得到的字符串
    """
    return content.replace('\r\n', '\n')


def main():
    """
    join参数
    :return:
    """
    # 读取剪贴板内容
    txt = pyperclip.paste()
    txt = remove_return(txt)

    # workflow
    wf = Workflow3()

    workflow_util.add_wf_item(wf, title=repr(txt), subtitle=r'replace \r\n with \n', arg=txt, valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    main()
