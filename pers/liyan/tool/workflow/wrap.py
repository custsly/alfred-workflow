# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def main():
    """
    包装字符串
    :return:
    """
    # 包装的字符串
    wrapper = ''
    if len(sys.argv) > 1:
        wrapper = sys.argv[1]

    # 读取剪贴板内容
    txt = pyperclip.paste()
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


if __name__ == '__main__':
    main()
