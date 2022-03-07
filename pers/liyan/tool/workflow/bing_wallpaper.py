import getopt
import os
import sys
from datetime import datetime

import requests
from furl import furl

from workflow import Workflow3

wf = Workflow3()


def download_wallpaper(dir_path, date_str):
    """
    下载给定日期的 bing 壁纸, UHD 版本, 按照 给定日期格式 命名文件
    :param dir_path: 目录
    :param date_str: 日期, yyyyMMdd
    :return: 图片路径
    """

    wf.logger.info('start download_wallpaper, dir_path: %s, date_str: %s' % (dir_path, date_str))

    idx = 0
    date_suffix = datetime.today().strftime('%Y%m%d')

    if date_str:
        image_date = datetime.strptime(date_str, '%Y%m%d').date()
        days_offset = (datetime.today().date() - image_date).days
        # 日期限制范围, 否则下载不到
        if 0 <= days_offset <= 7:
            idx = days_offset
            date_suffix = date_str
        else:
            wf.logger.warn('invalid date: %s' % date_str)

    # 如果文件存在, 不进行下载, return
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        if date_suffix in file_name:
            wf.logger.info('wallpaper of %s already exist' % file_name)
            return os.path.join(dir_path, file_name)

    # if any(map(lambda f: date_suffix in f, file_list)):
    #     wf.logger.info('wallpaper of %s already exist' % date_suffix)
    #     return
    image_info_json = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=%s&n=1&mkt=zh-CN' % idx) \
        .json()
    image_info = image_info_json['images'][0]

    wf.logger.info('image info %s' % image_info)
    # 标题
    title = image_info['title']
    image_url = 'https://cn.bing.com' + image_info['url'].replace('1920x1080', 'UHD')
    wf.logger.info('title %s, image url %s' % (title, image_url))

    image_furl = furl(image_url)
    # 提取文件名后缀
    image_id = str(image_furl.args['id'])
    ext_name = image_id[image_id.rfind('.'):]
    wf.logger.info('image ext name %s' % ext_name)

    image_file_path = os.path.join(dir_path, '{0}_{1}{2}'.format(title, date_suffix, ext_name))
    wf.logger.info('image file path %s' % image_file_path)
    # 文件存在, 删除
    # if os.path.exists(image_file_path):
    #     print('remove exists image %s' % image_file_path)
    #     os.remove(image_file_path)

    image_response = requests.get(image_url)
    with open(image_file_path, "wb") as attach:
        attach.write(image_response.content)
    wf.logger.info('save download image finish %s' % image_file_path)
    return image_file_path


def flow_main(args):
    """
    下载 bing 壁纸, 支持指定文件路径和日期
    :param args: -p 文件路径, -d 日期(可以为空, 默认当天)
    :return:
    """
    opts, _ = getopt.getopt(args, "p:d:")
    opts_dict = dict(opts)
    image_dir_path = opts_dict.get('-p')
    image_date_str = opts_dict.get('-d')
    return download_wallpaper(image_dir_path, image_date_str)


if __name__ == '__main__':
    # 阻止换行
    print(flow_main(sys.argv[1:]), end='')
