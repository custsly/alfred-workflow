# -*- coding: UTF-8 -*-
import sys

sys.path.append(r'/Users/shiliyan/Workspace/python/tools/lib')
import pyperclip
from workflow import Workflow3
from wf_utils import workflow_util


def partition_by(init_list, partition_size):
    """
    分割 list
    :param init_list: 原始 list
    :param partition_size: 分区大小
    :return:
    """
    groups_list = zip(*(iter(init_list),) * partition_size)
    partition_list = [list(i) for i in groups_list]
    count = len(init_list) % partition_size
    partition_list.append(init_list[-count:]) if count != 0 else partition_list
    return partition_list


def main():
    """
    读取剪贴板, 移除空白行, 按照 \n 拆分之后对 list 进行分割
    :return:
    """

    # 默认大小 100
    size = 100
    if len(sys.argv) > 1:
        try:
            size = int(sys.argv[1])
        except ValueError as e:
            pass
    # 非法参数, 暂不处理

    # 读取剪贴板内容
    txt = pyperclip.paste()
    txt = workflow_util.remove_blank_exclude_newline(txt)
    txt_list = txt.split('\n')
    # 拆分 list
    partition_list = partition_by(txt_list, size)
    partition_str_list = map(lambda l: '\n'.join(l), partition_list)

    # workflow
    wf = Workflow3()
    workflow_util.add_wf_item(wf, title='split to %s partitions' % len(partition_list),
                              subtitle='total count %s' % len(txt_list),
                              # 两个 partition 之间使用两个换行分割
                              copytext='\n\n'.join(partition_str_list))

    wf.send_feedback()


if __name__ == '__main__':
    main()
