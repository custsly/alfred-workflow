# -*- coding: UTF-8 -*-

import pyperclip

from wf_utils import workflow_util
from workflow import Workflow3

VARCHAR_EXCLUDE_CELL = ('now()',)


def cell_to_column(cell):
    """
    单元格值转换为 insert 语句字段
    :param cell: 单元格值
    :return:
    """
    if cell is None:
        return 'null'
    elif cell in VARCHAR_EXCLUDE_CELL:
        return cell
    else:
        return '\'' + cell + '\''


def row_to_record(row):
    """
    excel行转换为 insert 记录
    :param row: 行
    :return:
    """
    cells = row.split('\t')
    column_list = list(map(cell_to_column, cells))
    return '(' + ', '.join(column_list) + ')'


def main():
    # 读取剪贴板内容
    txt = pyperclip.paste()
    # 替换/r/n 为 /n
    txt = txt.replace('\r\n', '\n')
    rows = txt.split('\n')
    record_list = list(map(row_to_record, rows))
    values_sql = ',\n'.join(record_list)
    # workflow
    wf = Workflow3()
    workflow_util.add_wf_item(wf, title="values SQL", subtitle="total count %s" % len(rows), arg=values_sql)
    wf.send_feedback()


if __name__ == '__main__':
    main()
