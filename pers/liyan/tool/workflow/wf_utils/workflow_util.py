# -*- coding: UTF-8 -*-


def add_wf_item(wf, title, subtitle=None, copytext=None, valid=True, arg=None, icon=None, icontype=None):
    """
    workflow 增加 item
    :param wf: workflow
    :param title: title
    :param subtitle: subtitle
    :param copytext: copytext, 复制到剪贴板的内容, 最好不要设置, 把输出参数设置到 arg 即可, 更灵活
    :param valid: valid
    :param arg 输出参数
    :param icon icon
    :param icontype icontype
    :return: add_item 方法的返回值
    """
    if copytext is None:
        copytext = arg
    return wf.add_item(title=title, subtitle=subtitle, valid=valid, copytext=copytext, arg=arg, icon=icon,
                       icontype=icontype)


def remove_carriage_return(content):
    """
    移除回车
    :param content: 字符串
    :return: 移除后的内容
    """
    if content is None:
        return ''
    return content.replace('\r', '')


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


def strip(content):
    """
    移除两侧空白字符
    :param content: 字符串
    :return: 移除后的内容
    """
    if content is None:
        return ''
    return content.strip()


def wrap_with_symbol(txt_list, symbol="'"):
    """
    使用符号包装
    :param symbol: 包装的符号
    :param txt_list: 文本内容list
    :return: 返回
    """

    return list(map(lambda txt: symbol + txt + symbol, txt_list))


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


def remove_blank_element(text_list):
    """
    删除集合中的空字符串
    :param text_list: 字符串 list
    :return: list
    """

    return [text for text in text_list if text.strip()]


def build_cookie_dict(browser_cookies):
    """
    browser_cookie3 获取到的cookie转换为dict
    :param browser_cookies: cookie 集合
    :return:
    """
    if not browser_cookies:
        return {}
    else:
        return {c.name: c.value for c in browser_cookies}


def filter_and_convert_cookies(browser_cookies, cookie_domains):
    """
    根据domain过滤cookie, 转换为字典
    :param browser_cookies:
    :param cookie_domains:
    :return:
    """
    if not browser_cookies:
        return {}
    return build_cookie_dict(filter(lambda c: c.domain in cookie_domains, browser_cookies))


def chrome_cookies(cookie_domains):
    """
    通过 browser_cookie3 获取 chrome 的cookie, 转换为字典返回
    :param cookie_domains: domains
    :return:
    """
    # 动态导入, 使用缓存时可以加快速度, 加载 browser_cookie3 模块耗时较长
    browser_cookie3 = __import__('browser_cookie3')
    return filter_and_convert_cookies(browser_cookie3.chrome(), cookie_domains)


def is_number(s):
    """
    判断字符串是否是 数字
    :param s: 字符串
    :return: true/false
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def is_integer(s):
    """
    判断字符串是否是 整数
    :param s: 字符串
    :return: true/false
    """
    try:
        int(s)
        return True
    except ValueError:
        pass
