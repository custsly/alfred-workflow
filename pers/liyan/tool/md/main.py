# encoding:utf-8
import base64
import os
import sys


def image_to_base64(image_path):
    """
    图片转换为 base64
    :param image_path: 图片文件路径
    :return: 文件名称(不含扩展名) 格式化后的base64字符串
    """
    # 获取文件扩展名
    name_ext = os.path.splitext(os.path.basename(image_path))
    image_name = name_ext[0]
    image_ext = name_ext[-1][1:]

    # 判断是否是图片文件
    if image_ext.upper() not in ('PNG', 'JPG', 'JPEG', 'BMP', 'GIF'):
        return '未知图片文件格式', image_ext

    # 读取文件内容，转换为base64编码
    with open(image_path, 'rb') as image_file:
        image_base64 = str(base64.b64encode(image_file.read()), 'utf-8')
        return image_name, r'data:image/jpeg;base64,{0}'.format(image_base64)


def build_md_var(image_name, image_base64):
    """
    构建 markdown 变量, 变量名为图片名称, 变量值为图片的 base64 编码
    :param image_name:
    :param image_base64:
    :return:
    """
    return r'[{0}]: {1}'.format(image_name, image_base64)


def build_md_image_tag(image_file_path):
    """
    构建md格式
    ![image_name][image_name]

    image_base64_var
    :param image_file_path: 图片文件路径
    :return:
    """
    image_name, image_base64 = image_to_base64(image_file_path)
    image_base64_var = build_md_var(image_name, image_base64)

    return '![{0}][{1}]\n\n{2}'.format(image_name, image_name, image_base64_var)


if __name__ == '__main__':

    absolute_file_path = None
    # 命令行参数 图片文件路径
    if len(sys.argv) > 1:
        absolute_file_path = sys.argv[1]
        print(build_md_image_tag(absolute_file_path))
    else:
        print('请选择一个图片文件')
