import os
import sys
import time

import requests
from furl import furl

from workflow import Workflow3

wf = Workflow3()


def download_today_wallpaper(dir_path):
    """
    下载当天的 bing 壁纸, UHD 版本
    :param dir_path: 目录
    :return: 图片路径
    """

    date_suffix = time.strftime("%Y%m%d", time.localtime())
    # 如果文件存在, 不进行下载, return
    file_list = os.listdir(dir_path)
    for file_name in file_list:
        if date_suffix in file_name:
            wf.logger.info('wallpaper of %s already exist' % file_name)
            return os.path.join(dir_path, file_name)

    # if any(map(lambda f: date_suffix in f, file_list)):
    #     wf.logger.info('wallpaper of %s already exist' % date_suffix)
    #     return
    image_info_json = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN').json()
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


if __name__ == '__main__':
    # 阻止换行
    print(download_today_wallpaper(sys.argv[1]), end='')
