# -*- coding: UTF-8 -*-
import getopt
import re
import sys
import time
from datetime import datetime

from wf_utils import workflow_util
from workflow import Workflow3

# 日期格式
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 操作类型, 0 当前时间, 1 时间戳转字符串, 2 字符串转时间戳, 3 多个时间戳批量转换, 4 多个字符串批量转时间戳
OPERATION_TUP = ('0', '1', '2', '3', '4')


def format_time(date_time):
    """
    按照 %Y-%m-%d %H:%M:%S 格式格式化时间
    :param date_time: 时间对象
    :return: 字符串
    """

    if not date_time:
        return None

    return time.strftime(DATE_TIME_FORMAT, date_time)


def parse_time(datetime_str):
    """
    字符串转换为time对象
    兼容类似 yyyy-MM-dd HH:mm:ss 的格式
    先对传入的字符串进行正则替换, 删除所有非数字字符, 字符创长度超过 14 非法数值
    字符串不足14位, 右侧补0到
    :param datetime_str:
    :return: 如果存在异常, 返回 None, 正常返回 时间对象
    """

    if not datetime_str:
        return None

    datetime_str = re.sub(r'\D', '', datetime_str).ljust(14, '0')

    if len(datetime_str) > 14:
        return None

    try:
        return time.strptime(datetime_str, '%Y%m%d%H%M%S')
    except ValueError as e:
        return None


def parse_timestamp_s(date_time):
    """
    time对象转换为 时间戳
    :param date_time: 时间对象
    :return: 返回 s 级时间戳
    """

    return int(time.mktime(date_time))


def duration_of_hour(date_time):
    """
    当前小时开始的时间戳, ms 值 000, 999
    :param date_time: 时间
    :return: 开始时间, 开始时间戳 后三位ms 000, 结束时间, 结束时间戳 后三位 999
    """
    hour_str = time.strftime("%Y-%m-%d %H", date_time)
    start_of_hour_str = hour_str + ':00:00'
    end_of_hour_str = hour_str + ':59:59'
    start_of_hour = time.strptime(start_of_hour_str, DATE_TIME_FORMAT)

    return start_of_hour_str, parse_timestamp_s(start_of_hour) * 1000, end_of_hour_str, parse_timestamp_s(
        start_of_hour) * 1000 + 3600000 - 1


def duration_of_minute(date_time):
    """
    当前分钟的开始结束时间戳, ms
    :param date_time: 时间
    :return:  开始时间, 开始时间戳, 结束时间, 结束时间戳
    """
    minute_str = time.strftime("%Y-%m-%d %H:%M", date_time)
    start_of_minute_str = minute_str + ':00'
    end_of_minute_str = minute_str + ':59'
    start_of_minute = time.strptime(start_of_minute_str, DATE_TIME_FORMAT)

    return start_of_minute_str, parse_timestamp_s(start_of_minute) * 1000, end_of_minute_str, parse_timestamp_s(
        start_of_minute) * 1000 + 60000 - 1


def duration_of_day(date_time):
    """
    当前日期开始的时间戳, ms 值 000, 999
    :param date_time: 时间
    :return: 开始时间, 开始时间戳 后三位ms 000, 结束时间, 结束时间戳 后三位 999
    """
    day_str = time.strftime("%Y-%m-%d", date_time)
    start_of_day_str = day_str + ' 00:00:00'
    end_of_day_str = day_str + ' 23:59:59'
    start_of_day = time.strptime(start_of_day_str, DATE_TIME_FORMAT)

    return start_of_day_str, parse_timestamp_s(start_of_day) * 1000, end_of_day_str, parse_timestamp_s(
        start_of_day) * 1000 + 86400000 - 1


def add_duration_to_workflow(func, date_time, workflow, duration_name):
    """
    在 workflow 增加一个区间的开始时间戳和结束时间戳
    :param func: 返回区间函数的 function, 需要4个返回值, 区间开始时间(文本格式), 开始时间戳(ms), 结束时间(文本), 结束时间戳(ms)
    :param date_time: datetime
    :param workflow: workflow 对象
    :param duration_name: 区间名称 day/hour/minute
    :return:
    """
    start_of_duration, duration_start_ms, end_of_duration, duration_end_ms = func(date_time)
    duration_total = '%s, %s' % (duration_start_ms, duration_end_ms)
    duration_total1 = '%s %s' % (duration_start_ms, duration_end_ms)
    duration_total_between = 'between %s and %s' % (duration_start_ms, duration_end_ms)

    ms_of_duration_item = workflow_util.add_wf_item(workflow, title='ms timestamp of %s' % duration_name,
                                                    subtitle='%s %s (start of %s)'
                                                             % (duration_start_ms, start_of_duration, duration_name),
                                                    arg=duration_start_ms)
    ms_of_duration_item.add_modifier('alt', subtitle='%s %s (end of %s)'
                                                     % (duration_end_ms, end_of_duration, duration_name),
                                     arg=duration_end_ms)
    duration_total_item = workflow_util.add_wf_item(workflow, title='%s [%s, %s]' % (duration_name, start_of_duration,
                                                                                     end_of_duration),
                                                    subtitle=duration_total,
                                                    arg=duration_total)
    duration_total_item.add_modifier('alt', subtitle=duration_total1, arg=duration_total1, valid=True)
    # between and
    duration_total_item.add_modifier('cmd', subtitle=duration_total_between, arg=duration_total_between, valid=True)


def parse_datetime_with_timestamp_s(timestamp):
    """
    字符串格式的时间戳转换为时间类型 秒级时间戳
    尝试输入的字符串为数字, 如果发生异常返回 None
    :param timestamp:
    :return:
    """
    try:
        timestamp = float(timestamp)
    except ValueError as e:
        # print('parse float error str: %s, error: %s' % (timestamp, e))
        return None

    return time.localtime(timestamp)


def parse_datetime_with_timestamp_ms(timestamp):
    """
    字符串格式的时间戳转换为时间类型 毫秒级时间戳
    尝试输入的字符串为数字, 如果发生异常返回 None
    :param timestamp:
    :return:
    """

    try:
        timestamp = float(timestamp)
    except ValueError as e:
        # print('parse float error str: %s, error: %s' % (timestamp, e))
        return None

    timestamp = float(timestamp) / 1000.0
    return time.localtime(timestamp)


def parse_datetime_with_ts_ms_batch(timestamps_str):
    """
    分隔长字符串, 并作为 ms 时间戳转换为时间类型
    :param timestamps_str: 使用逗号,空格,tab分隔的多个时间戳
    :return: list
    """
    timestamp_list = re.sub(r'\D', ' ', timestamps_str).split(' ')
    return list(map(parse_datetime_with_timestamp_ms, timestamp_list))


def parse_ms_timestamp_with_str_batch(datetime_str_lines):
    """
    分隔长字符串, 作为时间字符串转换为
    :param datetime_str_lines: 使用逗号,空格,tab分隔的多个时间戳
    :return: list
    """
    datetime_str_list = datetime_str_lines.split('\n')
    return list(map(parse_time, datetime_str_list))


def analysis_operation(txt_content):
    """
    根据文本内容预测操作类型, 必要的时候处理文本内容
    :param txt_content: 文本内容
    :return: 0, 1, 2 处理后的文本内容
    """
    # 空值, 类型 0
    if not txt_content:
        return '0', txt_content

    # 不存在数字, 无意义
    if re.search(r'\d', txt_content) is None:
        return '0', txt_content

    # 包含非数字字符, 并且替换掉非数字之后长度 >= 8
    if re.search(r'\D', txt_content) is not None:
        # 格式类似 1629648000000	1629676800000	1629707400000
        if re.match(r'(\d+[,\t\n ]+)+\d+', txt_content):
            return '3', txt_content
        # 有超过2个换行, 作为多行时间转时间戳处理
        elif txt_content.count('\n') > 2:
            return '4', txt_content
        # 匹配格式 2.32.12 4:12:23 3.12 当做时分秒处理, 在前面拼接年月日
        elif re.match(r'(\d{1,2}[\\.:])+\d{1,2}', txt_content):
            time_list = re.sub(r'\D', ' ', txt_content).split(' ')
            txt_content = ''.join(list(map(lambda t: t.rjust(2, '0'), time_list)))
            date_str = datetime.now().strftime("%Y-%m-%d")
            return '2', (date_str + txt_content)
        # 匹配格式08-21 8-21, 当做月和日处理, 在前面拼接年份
        elif re.match(r'(\d{1,2}-)+\d{1,2}', txt_content):
            time_list = re.sub(r'\D', ' ', txt_content).split(' ')
            txt_content = ''.join(list(map(lambda t: t.rjust(2, '0'), time_list)))
            return '2', (str(datetime.now().date().year) + txt_content)
        elif len(re.sub(r'\D', '', txt_content)) >= 8:
            # 非数字替换成空白字符, 长度 >= 8 作为字符串转时间戳处理
            return '2', txt_content
        else:
            return '0', txt_content

    # 纯数字长度 < 8 位, 补全为时间格式, 按照字符串转时间戳处理
    txt_len = len(txt_content)
    if txt_len <= 8:
        # 当前时间 到 日, 截取之后和参数拼起来
        today_str = datetime.now().strftime('%Y%m%d')
        merge = today_str[:len(today_str) - txt_len] + txt_content
        return '2', merge

    # 纯数字字符, 长度超过 14 位无意义, 否则按照时间戳处理
    if txt_len <= 14:
        return '1', txt_content

    return '0', txt_content


def analysis_operation_and_data(arg, clip_content):
    """
    分析得到操作类型和数据内容
    :param arg 命令行参数
    :param clip_content 剪贴板内容
    :return: 操作类型, 时间数据
    """

    # 没有传参数
    if not arg:
        # 读取剪贴板
        clip_content = workflow_util.strip(clip_content)
        return analysis_operation(clip_content)

    # 不需要读取剪贴板的情况
    if arg not in OPERATION_TUP:
        arg = workflow_util.strip(arg)
        return analysis_operation(arg)
    else:
        # 使用剪贴板内容
        clip_content = workflow_util.strip(clip_content)
        return arg, clip_content


def flow(args):
    """
    读取剪贴板, 或者从命令行获取参数
    命令行可以指定操作类型(0, 1, 2, 3), 此时时间数据从剪贴板获取
    命令行不指定操作类型时时间数据优先从命令行获取, 命令行为空则使用剪贴板数据
    :param args 命令行参数 包含2个参数, -a 程序的参数, -c 剪贴板内容
    :return:
    """
    opts, _ = getopt.getopt(args, "a:c:")
    opts_dict = dict(opts)
    operation, txt_content = analysis_operation_and_data(opts_dict.get('-a'), opts_dict.get('-c'))

    # workflow
    wf = Workflow3()
    if operation == '0':
        timestamp = time.time()
        timestamp_s = int(timestamp)
        timestamp_ms = int(timestamp * 1000)
        now = time.localtime(timestamp)

        date_str_1 = time.strftime("%Y-%m-%d", now)
        date_str_2 = time.strftime("%Y%m%d", now)

        current_second_1 = time.strftime(DATE_TIME_FORMAT, now)
        current_second_2 = time.strftime("%Y%m%d%H%M%S", now)

        # yyyy-MM-dd 格式
        current_date_item = workflow_util.add_wf_item(wf, title='current date', subtitle=date_str_1,
                                                      arg=date_str_1,
                                                      valid=True)
        # 使用按键切换格式
        # yyyyMMdd 格式
        current_date_item.add_modifier('alt', subtitle=date_str_2, arg=date_str_2, valid=True)
        # yyyy-MM-dd HH:mm:ss 格式
        current_second_item = workflow_util.add_wf_item(wf, title='current second', subtitle=current_second_1,
                                                        arg=current_second_1)
        # yyyyMMddHHmmss 格式
        current_second_item.add_modifier('alt', subtitle=current_second_2, arg=current_second_2, valid=True)

        # 当前时间戳 ms
        current_timestamp_item = workflow_util.add_wf_item(wf, title='current timestamp',
                                                           subtitle='%s(ms)' % timestamp_ms, arg=timestamp_ms)

        # 当天起止时间 ms
        add_duration_to_workflow(duration_of_day, now, wf, "day")

        # 小时的起止时间 ms
        add_duration_to_workflow(duration_of_hour, now, wf, "hour")

        # 分钟的起止时间 ms
        add_duration_to_workflow(duration_of_minute, now, wf, "minute")

        # s 时间戳
        current_timestamp_item.add_modifier('alt', subtitle='%s(s)' % timestamp_s, arg=timestamp_s, valid=True)

    elif operation == '1':
        # ms 时间戳转换为时间
        time_from_ms = parse_datetime_with_timestamp_ms(txt_content)
        time_str_from_ms = format_time(time_from_ms) if time_from_ms else 'Invalid ms timestamp "%s"' % txt_content

        # s 时间戳转换为时间
        time_from_s = parse_datetime_with_timestamp_s(txt_content)
        time_str_from_s = format_time(time_from_s) if time_from_s else 'Invalid second timestamp "%s"' % txt_content

        workflow_util.add_wf_item(wf, title=time_str_from_ms,
                                  subtitle=('time parse from ms timestamp "%s"' % txt_content) if time_from_ms else '',
                                  arg=time_str_from_ms,
                                  valid=(time_from_ms is not None))
        # 当天起止时间 ms
        add_duration_to_workflow(duration_of_day, time_from_ms, wf, "day")

        # 小时的起止时间 ms
        add_duration_to_workflow(duration_of_hour, time_from_ms, wf, "hour")

        # 分钟的起止时间 ms
        add_duration_to_workflow(duration_of_minute, time_from_ms, wf, "minute")

        workflow_util.add_wf_item(wf, title=time_str_from_s,
                                  subtitle='time parse from second timestamp "%s"' % txt_content if time_from_s else '',
                                  arg=time_str_from_s,
                                  valid=(time_from_s is not None))
    elif operation == '2':
        # 时间转换为标准格式
        date_time = parse_time(txt_content)

        if not date_time:
            workflow_util.add_wf_item(wf, title='Invalid datetime str "%s"' % txt_content,
                                      subtitle='',
                                      arg=None,
                                      valid=False)
        else:
            timestamp_s = parse_timestamp_s(date_time)
            date_time_str = format_time(date_time)

            # ms 时间戳 ms 值 000
            second_ms_timestamp_item = workflow_util.add_wf_item(wf, title='ms timestamp of second, "%s"'
                                                                           % date_time_str,
                                                                 subtitle='%s (start of second)' % (timestamp_s * 1000),
                                                                 arg=timestamp_s * 1000)

            # ms 时间戳 ms 值 999
            second_ms_timestamp_item.add_modifier('alt', subtitle='%s (end of second)' % (timestamp_s * 1000 + 999),
                                                  arg=timestamp_s * 1000 + 999, valid=True)

            # 当天起止时间 ms
            add_duration_to_workflow(duration_of_day, date_time, wf, "day")

            # 小时的起止时间 ms
            add_duration_to_workflow(duration_of_hour, date_time, wf, "hour")

            # 分钟的起止时间 ms
            add_duration_to_workflow(duration_of_minute, date_time, wf, "minute")

            # 秒级时间戳
            workflow_util.add_wf_item(wf, title='second timestamp, "%s"' % date_time_str,
                                      subtitle=timestamp_s,
                                      arg=timestamp_s)
    elif operation == '3':
        # 批量将时间戳转换为字符串
        date_time_list = parse_datetime_with_ts_ms_batch(txt_content)
        # 使用逗号分隔
        date_time_sec_str = ', '.join(map(lambda dt: time.strftime(DATE_TIME_FORMAT, dt), date_time_list))
        workflow_util.add_wf_item(wf, title='parse million second datetime batch',
                                  subtitle=date_time_sec_str,
                                  arg=date_time_sec_str)
        # 使用换行分割
        date_time_sec_str_lines = '\n'.join(map(lambda dt: time.strftime(DATE_TIME_FORMAT, dt), date_time_list))
        workflow_util.add_wf_item(wf, title='parse million second datetime batch lines',
                                  subtitle=date_time_sec_str_lines,
                                  arg=date_time_sec_str_lines)
    elif operation == '4':
        # 批量字符串转时间戳
        date_time_list = parse_ms_timestamp_with_str_batch(txt_content)
        # 使用换行分割
        timestamp_ms_lines = '\n'.join(map(lambda dt: str(parse_timestamp_s(dt) * 1000), date_time_list))
        workflow_util.add_wf_item(wf, title='parse to million second batch',
                                  subtitle=timestamp_ms_lines,
                                  arg=timestamp_ms_lines)

    wf.send_feedback()


def main():
    flow(sys.argv[1:])


if __name__ == '__main__':
    main()
