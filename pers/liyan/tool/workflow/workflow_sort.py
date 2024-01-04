# -*- coding: UTF-8 -*-
import sys

import pyperclip

from wf_utils import workflow_util
from ualfred import Workflow3


def analysis_operation(txt_list, param):
    """
    分析列表类型, 是否只有数值, 解析操作类型
    :param txt_list: list
    :param param: 用户选项 只有 1,2
    :return:
    """

    if all(map(workflow_util.is_number, txt_list)):
        return 2 if param is None else param
    else:
        return 1


def flow(args, clip_content):
    """
    读取剪贴板, 移除空白行, 排序
    :param args: 命令行参数, 1 - 字符串类型, 2 - 数值类型
    :param clip_content: 剪贴板内容
    :return:
    """
    # 参数
    param = args[1] if len(args) > 1 else None
    if param not in ('1', '2'):
        param = None

    if param is not None:
        param = int(param)

    # 读取剪贴板内容
    txt = clip_content
    txt = workflow_util.remove_blank_exclude_newline(txt)
    txt_list = txt.split('\n')

    param = analysis_operation(txt_list, param)

    # workflow
    wf = Workflow3()

    if param == 1:
        # 字符串排序
        txt_list.sort()
    elif param == 2:
        # 数值排序
        txt_list.sort(key=int)

    # 增加括号
    sorted_list = '\n'.join(txt_list)
    workflow_util.add_wf_item(wf, title=repr(sorted_list), subtitle='sorted_list', arg=sorted_list)

    wf.send_feedback()


def main():
    flow(sys.argv, pyperclip.paste())


if __name__ == '__main__':
    main()
