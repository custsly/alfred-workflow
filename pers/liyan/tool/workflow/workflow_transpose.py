# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from ualfred import Workflow3


def analysis_operation(clip_content):
    if clip_content.count('\n') > 0:
        return 'r'
    elif clip_content.count('\t') > 0:
        return 'c'

    return 'c'


def flow(args):
    """
    读取剪贴板, 转置 参数
    :param args 命令行参数, -c 剪贴板的内容
    :return:
    """

    # workflow
    wf = Workflow3()

    # 参数
    opts, _ = getopt.getopt(args, "o:c:")
    opts_dict = dict(opts)

    # 读取剪贴板内容
    txt = workflow_util.remove_return(opts_dict.get('-c'))

    # 操作类型, r列转行, c行转列, 默认列转行
    operation = opts_dict.get('-o') if opts_dict.get('-o') else analysis_operation(opts_dict.get('-c'))

    wf.logger.info('transpose operation %s, txt %s' % (operation, txt))
    operation_name = 'row to column' if operation == 'c' else 'column to row'
    spliter = '\t' if operation == 'c' else '\n'
    new_spliter = '\n' if operation == 'c' else '\t'

    txt_list = txt.split(spliter)

    transpose_result = new_spliter.join(txt_list)

    # split 得到的结果
    workflow_util.add_wf_item(wf, title=operation_name, subtitle=repr(transpose_result), arg=transpose_result)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
