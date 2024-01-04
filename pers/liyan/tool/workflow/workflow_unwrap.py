# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def flow(args):
    """
    删除字符串两端指定的字符, 按照换行 /n 切分之后包装
    :param args 命令行参数, -a 要删除的字符串, 默认 , -c 剪贴板内容
    :return:
    """

    # 参数
    opts, _ = getopt.getopt(args, "a:c:")
    opts_dict = dict(opts)

    # 包装的字符串
    wrapper = ''
    if opts_dict.get('-a'):
        wrapper = args[1]

    # 读取剪贴板内容
    txt = opts_dict.get('-c')
    # 移除回车
    txt = workflow_util.remove_carriage_return(txt)
    txt_list = txt.split('\n')
    # 移除字符串
    txt_list = map(lambda x: x.strip(wrapper), txt_list)

    # workflow
    wf = Workflow3()

    # result
    result = '\n'.join(txt_list)

    workflow_util.add_wf_item(wf, title=result, subtitle="un wrapper with " + wrapper, arg=result, copytext=result)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
