# -*- coding: UTF-8 -*-
import getopt
import sys

from wf_utils import workflow_util
from workflow import Workflow3


def flow(args):
    """
    workflow主要逻辑, 从SQL平台查询结果中提取一列数据
    :param args: -a 命令行参数, 1 - 字符串类型, 2 - 数值类型, -c 剪贴板内容
    :return:
    """
    # 参数
    opts, _ = getopt.getopt(args, "a:c:")
    opts_dict = dict(opts)

    param = args[1] if opts_dict.get('-a') else '2'
    clip_content = opts_dict.get('-c')

    if not clip_content:
        return

    # 根据 \n 拆分成行
    row_list = clip_content.split('\n')

    # 按照列拆分
    row_list = list(map(lambda r: r.split('\t'), row_list))

    # 存储最后的结果
    column_value_list = []
    # 如果行数少于 3 行, 无法确定一行的列数, 取第 1 行的第一个元素和第 2 行的最后一个元素作为结果
    if len(row_list) <= 2:
        column_value_list.append(row_list[0][0])
        if len(row_list) > 1:
            column_value_list.append(row_list[1][-1])
        pass
    else:
        # 一行的列数
        column_count = len(row_list[1])
        # 选中的列范围(包含)
        start_column_index = column_count - len(row_list[0])
        end_column_index = len(row_list[-1]) - 1

        for i, row in enumerate(row_list):
            # 第1行取第1列
            if i == 0:
                # 列数过少不处理
                if len(row) <= end_column_index - start_column_index:
                    continue
                column_value_list.append(
                    '\t'.join(row[: end_column_index - start_column_index + 1]))
            # 列数过少, 跳过
            elif len(row) <= end_column_index:
                continue
            # 按照索引获取
            else:
                column_value_list.append('\t'.join(row[start_column_index: end_column_index + 1]))

    # workflow
    wf = Workflow3()

    if param == '1':
        column_values_str = '\n'.join(map(lambda c: "'" + c + "'", column_value_list))
    else:
        column_values_str = '\n'.join(column_value_list)

    workflow_util.add_wf_item(wf, title=repr(column_values_str), subtitle=r'column values', arg=column_values_str,
                              valid=True)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
