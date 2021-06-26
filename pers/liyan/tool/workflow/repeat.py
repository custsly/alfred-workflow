# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3


def main():
    """
    读取剪贴板, repeat
    :return:
    """
    # split的字符串, 默认值 ,
    count = 1
    if len(sys.argv) > 1 and sys.argv[1]:
        try:
            count = int(sys.argv[1])
        except ValueError as e:
            pass

    # 读取剪贴板内容
    txt = pyperclip.paste()

    repeat_result = txt * count

    # workflow
    wf = Workflow3()

    # split 得到的结果
    workflow_util.add_wf_item(wf, title='repeated result', subtitle="%s * %s" % (repr(txt), count),
                              copytext=repeat_result)

    wf.send_feedback()


if __name__ == '__main__':
    main()
