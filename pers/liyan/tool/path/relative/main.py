# encoding:utf-8
import os
import sys


def relative_git_path(absolute_path, break_path):
    """

    :param absolute_path: 绝对路径
    :param break_path: 跳出路径
    :return: 相对于git根目录的相对路径/查找不到.git目录返回原始的输入
    """
    os.path.abspath("~")
    dir_name = absolute_path
    while dir_name != break_path and dir_name != '/':
        dir_name = os.path.dirname(dir_name)
        # print('dir_name %s' % dir_name)
        if os.path.exists(os.path.join(dir_name, '.git')):
            break

    if dir_name == '/':
        return absolute_path
    else:
        return '.' + absolute_path.replace(dir_name, '')


if __name__ == '__main__':

    absolute_file_path = None

    if len(sys.argv) > 1:
        absolute_file_path = sys.argv[1]
    else:
        absolute_file_path = os.getcwd()

    print(relative_git_path(absolute_file_path, r'/Users/shiliyan/'))
