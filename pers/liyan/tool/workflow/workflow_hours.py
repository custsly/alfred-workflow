# -*- coding: UTF-8 -*-
import re
import sys
from datetime import datetime
from datetime import timedelta

from wf_utils import workflow_util
from workflow import Workflow3


def parse_date_time(datetime_str):
    """
    字符串转换为time对象
    兼容类似 yyyy-MM-dd HH:mm:ss 的格式
    先对传入的字符串进行正则替换, 删除所有非数字字符,
    如果字符串长度 > 14, 认为是非法字符
    兼容格式 H.m
    兼容格式 H.m.s
    :param datetime_str:
    :return: 如果存在异常, 返回 None, 正常返回 是否包含天, 时间对象
    """

    datetime_str = workflow_util.strip(datetime_str)

    if not datetime_str:
        return False, None

    with_day = False

    # 匹配格式 12.30 12:30 2:30 02:30 , 当做 HH:mm:ss 处理, 拼接当前日期
    if re.match(r'^(\d{1,2}[.:])+\d{1,2}?$', datetime_str):
        time_list = re.sub(r'\D', ' ', datetime_str).split(' ')

        datetime_str = datetime.now().strftime('%Y%m%d') + (
            ''.join(list(map(lambda t: t.rjust(2, '0'), time_list[:2]))))
    # 单个数字格式
    elif re.match(r'^\d{1,2}$', datetime_str):
        datetime_str = datetime.now().strftime('%Y%m%d') + datetime_str.rjust(2, '0') + '00'
    else:
        with_day = True
        datetime_str = re.sub(r'\D', '', datetime_str)

    if len(datetime_str) > 14 or len(datetime_str) < 12:
        return False, None

    try:
        # 丢弃 s
        return with_day, datetime.strptime(datetime_str[:12], '%Y%m%d%H%M')
    except ValueError as e:
        return False, None


def flow(args):
    """
    计算给定两个时间之间的小时数, 分钟数 忽略秒, 保留5位小数
    :param args: 命令行参数, -a 最多两个时间, 空格分隔
    :return:
    """

    # workflow
    start_time_with_day, end_time_with_day = False, False
    start_time, end_time = None, None
    wf = Workflow3()
    valid = True

    if len(args) < 2 or not args[1]:
        valid = False
    else:
        arg_arr = args[1].split(' ')
        wf.logger.info('workflow_minutes arg_arr %s' % arg_arr)
        start_time_with_day, start_time = parse_date_time(arg_arr[0])
        end_time_with_day, end_time = parse_date_time(arg_arr[1]) if len(
            arg_arr) > 1 else (False, datetime.now().replace(second=0, microsecond=0))
        if not start_time or not end_time:
            valid = False
        wf.logger.info('start_time %s, end_time %s' % (start_time, end_time))

    if not valid:
        workflow_util.add_wf_item(wf, title='illegal args %s' % args[1:])
    else:
        # 开始时间和结束时间都没有具体的日期, 调整开始和结束时间
        if not start_time_with_day and not end_time_with_day:
            if start_time > end_time:
                # 结束日期加一天
                end_time = end_time + timedelta(days=1)
        elif start_time > end_time:
            start_time, end_time = end_time, start_time
        duration_seconds = (end_time - start_time).seconds
        duration_minutes = format(duration_seconds / 60, '.5f')
        duration_hours = format(duration_seconds / 60 / 60, '.5f')
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M')

        workflow_util.add_wf_item(wf, title='%s hours' % duration_hours, subtitle='hours between (%s, %s]' % (
            start_time_str, end_time_str), copytext=duration_hours, valid=True,
                                  arg=duration_hours)

        workflow_util.add_wf_item(wf, title='%s minutes' % duration_minutes,
                                  subtitle='minutes between [%s, %s]' % (
                                      start_time_str, end_time_str), copytext=duration_minutes, valid=True,
                                  arg=duration_minutes)

    wf.send_feedback()


def main():
    flow(sys.argv)


if __name__ == '__main__':
    main()
