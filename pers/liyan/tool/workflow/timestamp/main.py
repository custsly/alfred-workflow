# -*- coding: UTF-8 -*-
import sys

sys.path.append(r'/Users/shiliyan/Workspace/python/tools/lib')
import time
import re
import pyperclip
from workflow import Workflow3
from wf_utils import workflow_util

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 操作类型, 0 当前时间, 1 时间戳转字符串, 2 字符串转时间戳
OPERATION_TUP = ('0', '1', '2')


def format_time(datetime):
    """
    按照 %Y-%m-%d %H:%M:%S 格式格式化时间
    :param datetime: 时间对象
    :return: 字符串
    """

    if not datetime:
        return None

    return time.strftime(DATE_TIME_FORMAT, datetime)


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
        # print('strptime error str: %s, error: %s' % (datetime_str, e))
        return None


def parse_timestamp_s(datetime):
    """
    time对象转换为 时间戳
    :param datetime: 时间对象
    :return: 返回 s 级时间戳
    """

    return int(time.mktime(datetime))


def duration_of_hour(datetime):
    """
    当前小时开始的时间戳, ms 值 000, 999
    :param datetime: 时间
    :return: 开始时间, 开始时间戳 后三位ms 000, 结束时间, 结束时间戳 后三位 999
    """
    hour_str = time.strftime("%Y-%m-%d %H", datetime)
    start_of_hour_str = hour_str + ':00:00'
    end_of_hour_str = hour_str + ':59:59'
    start_of_hour = time.strptime(start_of_hour_str, DATE_TIME_FORMAT)

    return start_of_hour_str, parse_timestamp_s(start_of_hour) * 1000, end_of_hour_str, parse_timestamp_s(
        start_of_hour) * 1000 + 3600000 - 1


def duration_of_minute(datetime):
    """
    当前分钟的开始结束时间戳, ms
    :param datetime: 时间
    :return:  开始时间, 开始时间戳, 结束时间, 结束时间戳
    """
    minute_str = time.strftime("%Y-%m-%d %H:%M", datetime)
    start_of_minute_str = minute_str + ':00'
    end_of_minute_str = minute_str + ':59'
    start_of_minute = time.strptime(start_of_minute_str, DATE_TIME_FORMAT)

    return start_of_minute_str, parse_timestamp_s(start_of_minute) * 1000, end_of_minute_str, parse_timestamp_s(
        start_of_minute) * 1000 + 60000 - 1


def duration_of_day(datetime):
    """
    当前日期开始的时间戳, ms 值 000, 999
    :param datetime: 时间
    :return: 开始时间, 开始时间戳 后三位ms 000, 结束时间, 结束时间戳 后三位 999
    """
    day_str = time.strftime("%Y-%m-%d", datetime)
    start_of_day_str = day_str + ' 00:00:00'
    end_of_day_str = day_str + ' 23:59:59'
    start_of_day = time.strptime(start_of_day_str, DATE_TIME_FORMAT)

    return start_of_day_str, parse_timestamp_s(start_of_day) * 1000, end_of_day_str, parse_timestamp_s(
        start_of_day) * 1000 + 86400000 - 1


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


def analysis_operation(txt_content):
    """
    根据文本内容预测操作类型
    :param txt_content: 文本内容
    :return: 0, 1, 2
    """
    # 空值, 类型 0
    if not txt_content:
        return '0'

    # 包含非数字字符
    if re.search(r'\D', txt_content) is not None:
        return '2'

    # 纯数字字符, 长度超过 14 位无意义
    if len(txt_content) <= 14:
        return '1'

    return '0'


def analysis_operation_and_data():
    """
    分析得到操作类型和数据内容
    :return: 操作类型, 时间数据
    """

    # 取命令行参数
    arg = None
    if len(sys.argv) > 1 and sys.argv[1]:
        arg = sys.argv[1]

    # 没有传参数
    if arg is None:
        # 读取剪贴板
        clip_content = workflow_util.remove_blank(pyperclip.paste())
        return analysis_operation(clip_content), clip_content

    # 不需要读取剪贴板的情况
    if arg not in OPERATION_TUP:
        arg = workflow_util.remove_blank(arg)
        return analysis_operation(arg), arg
    else:
        # 读取剪贴板
        clip_content = workflow_util.remove_blank(pyperclip.paste())
        return arg, clip_content


def main():
    """
    读取剪贴板, 或者从命令行获取参数
    命令行可以指定操作类型(0, 1, 2), 此时时间数据从剪贴板获取
    命令行不指定操作类型时时间数据优先从命令行获取, 命令行为空则使用剪贴板数据
    :return:
    """

    operation, txt_content = analysis_operation_and_data()

    # workflow
    wf = Workflow3()
    if operation == '0':
        timestamp = time.time()
        timestamp_s = int(timestamp)
        timestamp_ms = int(timestamp * 1000)
        now = time.localtime(timestamp)

        date_str_1 = time.strftime("%Y-%m-%d", now)
        date_str_2 = time.strftime("%Y%m%d", now)

        current_second_1 = time.strftime("%Y-%m-%d %H:%M:%S", now)
        current_second_2 = time.strftime("%Y%m%d%H%M%S", now)

        workflow_util.add_wf_item(wf, title=date_str_1, subtitle='current date', copytext=date_str_1, valid=True)

        workflow_util.add_wf_item(wf, title=current_second_1, subtitle='current second', copytext=current_second_1)

        workflow_util.add_wf_item(wf, title=date_str_2, subtitle='current date', copytext=date_str_2, valid=True)

        workflow_util.add_wf_item(wf, title=current_second_2, subtitle='current second', copytext=current_second_2)

        workflow_util.add_wf_item(wf, title=timestamp_s, subtitle='current second timestamp', copytext=timestamp_s)

        workflow_util.add_wf_item(wf, title=timestamp_ms, subtitle='current ms timestamp', copytext=timestamp_ms)

    elif operation == '1':
        # ms 时间戳转换为时间
        time_from_ms = parse_datetime_with_timestamp_ms(txt_content)
        time_str_from_ms = format_time(time_from_ms) if time_from_ms else 'Invalid ms timestamp "%s"' % txt_content

        # s 时间戳转换为时间
        time_from_s = parse_datetime_with_timestamp_s(txt_content)
        time_str_from_s = format_time(time_from_s) if time_from_s else 'Invalid second timestamp "%s"' % txt_content

        workflow_util.add_wf_item(wf, title=time_str_from_ms,
                                  subtitle=('time parse from ms timestamp "%s"' % txt_content) if time_from_ms else '',
                                  copytext=time_str_from_ms,
                                  valid=(time_from_ms is not None))

        workflow_util.add_wf_item(wf, title=time_str_from_s,
                                  subtitle='time parse from second timestamp "%s"' % txt_content if time_from_s else '',
                                  copytext=time_str_from_s,
                                  valid=(time_from_s is not None))
    elif operation == '2':
        # 时间转换为标准格式
        date_time = parse_time(txt_content)

        if not date_time:
            workflow_util.add_wf_item(wf, title='Invalid datetime str "%s"' % txt_content,
                                      subtitle='',
                                      copytext=None,
                                      valid=False)
        else:
            timestamp_s = parse_timestamp_s(date_time)
            date_time_str = format_time(date_time)

            # ms 时间戳 ms 值 000
            workflow_util.add_wf_item(wf, title=timestamp_s * 1000,
                                      subtitle='ms timestamp start of second from "%s"' % date_time_str,
                                      copytext=timestamp_s * 1000)

            # ms 时间戳 ms 值 999
            workflow_util.add_wf_item(wf, title=timestamp_s * 1000 + 999,
                                      subtitle='ms timestamp end of second from "%s"' % date_time_str,
                                      copytext=timestamp_s * 1000 + 999)

            # 当天起止时间 ms
            start_of_day, day_start_ms, end_of_day, day_end_ms = duration_of_day(date_time)
            workflow_util.add_wf_item(wf, title=day_start_ms,
                                      subtitle='start of day(ms), "%s"' % start_of_day, copytext=day_start_ms)
            workflow_util.add_wf_item(wf, title=day_end_ms,
                                      subtitle='end of day(ms), "%s"' % end_of_day, copytext=day_end_ms)

            # 小时的起止时间 ms
            start_of_hour, hour_start_ms, end_of_hour, hour_end_ms = duration_of_hour(date_time)
            workflow_util.add_wf_item(wf, title=hour_start_ms,
                                      subtitle='start of hour(ms), "%s"' % start_of_hour, copytext=hour_start_ms)
            workflow_util.add_wf_item(wf, title=hour_end_ms,
                                      subtitle='end of hour(ms), "%s"' % end_of_hour, copytext=hour_end_ms)

            # 分钟的起止时间 ms
            start_of_minute, minute_start_ms, end_of_minute, minute_end_ms = duration_of_minute(date_time)
            workflow_util.add_wf_item(wf, title=minute_start_ms,
                                      subtitle='start of minute(ms), "%s"' % start_of_minute, copytext=minute_start_ms)
            workflow_util.add_wf_item(wf, title=minute_end_ms,
                                      subtitle='end of minute(ms), "%s"' % end_of_minute, copytext=minute_end_ms)

            # 秒级时间戳
            workflow_util.add_wf_item(wf, title=timestamp_s,
                                      subtitle='second timestamp from "%s"' % date_time_str,
                                      copytext=timestamp_s)

    wf.send_feedback()


if __name__ == '__main__':
    main()
