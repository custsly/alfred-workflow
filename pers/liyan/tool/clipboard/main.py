import subprocess
import re


def get_clipboard_content():
    """
    读取剪贴板内容 utf-8
    :return: 剪贴板内容
    """
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    p.wait()
    byte_array = p.stdout.read()
    # 这里的data为bytes类型，之后需要转成utf-8操作
    p.stdout.close()
    return str(byte_array, 'utf-8')


def set_clipboard_content(content):
    """
    文本写入剪贴板
    :param content: 文本内容
    :return: none
    """
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(bytes(content, 'utf-8'))
    p.stdin.close()
    p.communicate()


def remove_blank(content):
    """
    移除空白, /t 空格
    :param content: 字符串
    :return: 移除后的内容
    """
    return content.replace('\t', '')\
        .replace(' ', '')\
        .replace('\r', '')\
        .strip()


if __name__ == '__main__':

    txt = get_clipboard_content()
    txt = remove_blank(txt)

    param_type = input('paramType 1.string 2.number \n')

    if param_type == '1':
        txt = re.sub('\\n', "',\n'", txt)
        txt = "('" + txt + "')"
    elif param_type == '2':
        txt = re.sub('\\n', ",\n", txt)
        txt = "(" + txt + ")"
    else:
        pass
    print(txt)
    set_clipboard_content(txt)
    print('write clipboard finish')
