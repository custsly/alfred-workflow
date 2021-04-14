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
    # iter() 函数得到一个迭代器
    # * partition_size 迭代器复制 partition_size 个
    # 使用 * 解包为 a=<list_iterator ...>, b=<list_iterator ...>, c=<list_iterator ...> a,b,c 指向同一个迭代器对象
    # zip 函数依次执行 a, b, c 的 __next__() 方法, 直到 list 没有剩余元素
    # 实现按照 partition_size 分组的效果, 直到剩余元素个数不足 partition_size 个
    groups_list = zip(*(iter(init_list),) * partition_size)
    partition_list = [list(i) for i in groups_list]
    count = len(init_list) % partition_size
    # 此处作用类比三目运算符
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

    # 第一种格式, 按照原有顺序保持一列的格式, 在不同组之间使用多个 \n 分隔
    partition_str_list = map(lambda l: '\n'.join(l), partition_list)
    one_column_result = '\n\n'.join(partition_str_list)

    # 第二种格式, 拆分成多列, 可以直接粘贴到 excel 中
    # 扩充一下最后一个 list 的长度, 方便统一使用 zip 函数处理
    last_partition = partition_list[-1]
    partition_list[-1] = last_partition + [''] * (size - len(last_partition))
    row_list = zip(*partition_list)
    multi_column_result = '\n'.join(map(lambda t: '\t'.join(t), row_list))

    # workflow
    wf = Workflow3()
    workflow_util.add_wf_item(wf, title='split to %s partitions, one column' % len(partition_list),
                              subtitle='total count %s' % len(txt_list),
                              copytext=one_column_result)

    workflow_util.add_wf_item(wf, title='split to %s partitions, multi column' % len(partition_list),
                              subtitle='total count %s' % len(txt_list),
                              copytext=multi_column_result)

    wf.send_feedback()


if __name__ == '__main__':
    main()
