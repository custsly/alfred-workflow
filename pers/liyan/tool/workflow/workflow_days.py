# -*- coding: UTF-8 -*-
import re
import sys
from datetime import datetime

from wf_utils import workflow_util
from workflow import Workflow3


def parse_date(datetime_str):
    """
    字符串转换为time对象
    兼容类似 yyyy-MM-dd 的格式
    先对传入的字符串进行正则替换, 删除所有非数字字符, 字符串长度超过 8 非法数值
    :param datetime_str:
    :return: 如果存在异常, 返回 None, 正常返回 时间对象
    """

    if not datetime_str:
        return None

    # 匹配格式 08-21 8-21, 当做 MMdd 处理, 拼接当前年份
    if re.match(r'(\d{1,2}[-])+\d{1,2}', datetime_str):
        time_list = re.sub(r'\D', ' ', datetime_str).split(' ')

        datetime_str = str(datetime.now().date().year) + (''.join(list(map(lambda t: t.rjust(2, '0'), time_list))))
    else:
        datetime_str = re.sub(r'\D', '', datetime_str)

    if len(datetime_str) > 14 or len(datetime_str) < 8:
        return None

    try:
        return datetime.strptime(datetime_str, '%Y%m%d').date()
    except ValueError as e:
        return None


def flow(args, clip_content):
    """
    计算给定两个日期之间的天数
    :param args: 命令行参数, 最多两个日期, 空格分隔
    :param clip_content:
    :return:
    """

    # workflow
    start_date, end_date = None, None
    wf = Workflow3()
    valid = True

    if len(args) < 2 or not args[1]:
        valid = False
    else:
        arg_arr = args[1].split(' ')
        wf.logger.info('workflow_days arg_arr %s' % arg_arr)
        start_date = parse_date(arg_arr[0])
        end_date = parse_date(arg_arr[1]) if len(arg_arr) > 1 else datetime.now().date()
        if not start_date or not end_date:
            valid = False

    if not valid:
        workflow_util.add_wf_item(wf, title='illegal args %s' % args[1:])
    else:
        duration_days = abs((start_date - end_date).days)
        workflow_util.add_wf_item(wf, title='%s days' % duration_days, subtitle='days between %s and %s' % (
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')), copytext=duration_days, valid=True,
                                  arg=duration_days)

    wf.send_feedback()


def main():
    flow(sys.argv, None)


if __name__ == '__main__':
    main()