# -*- coding: UTF-8 -*-


def add_wf_item(wf, title, subtitle=None, copytext=None, valid=True):
    """
    workflow 增加 item
    :param wf: workflow
    :param title: title
    :param subtitle: subtitle
    :param copytext: copytext
    :param valid: valid
    :return:
    """
    wf.add_item(title=title, subtitle=subtitle, valid=valid, copytext=copytext)


def remove_blank_exclude_newline(content):
    """
    移除空白, \t 空格, 保留 \n
    :param content: 字符串
    :return: 移除后的内容
    """
    if content is None:
        return ''
    return content.replace('\t', '') \
        .replace(' ', '') \
        .replace('\r', '') \
        .strip()


def remove_blank(content):
    """
    移除空白, \t 空格, \n
    :param content: 字符串
    :return: 移除后的内容
    """
    if content is None:
        return ''
    return content.replace('\t', '') \
        .replace(' ', '') \
        .replace('\r', '') \
        .replace('\n', '') \
        .strip()


def un_wrap_brackets(text):
    """
    移除两端的括号
    :param text:
    :return:
    """
    if text is None:
        return ''
    return text.strip('(').strip(')')


def un_wrap_quote(text):
    """
    移除两端的单引号
    :param text:
    :return:
    """
    if text is None:
        return ''
    return text.strip("'")
