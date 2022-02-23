import os
import time

import requests
from furl import furl


def download_today_wallpaper(dir_path):
    """
    下载当天的 bing 壁纸, UHD 版本
    :param dir_path: 目录
    :return:
    """

    date_suffix = time.strftime("%Y%m%d", time.localtime())
    # 如果文件存在, 不进行下载, return
    file_list = os.listdir(dir_path)
    if any(map(lambda f: date_suffix in f, file_list)):
        print('wallpaper of %s already exist' % date_suffix)
        return

    image_info_json = requests.get('https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN').json()
    image_info = image_info_json['images'][0]

    print('image info %s' % image_info)
    # 标题
    title = image_info['title']
    image_url = 'https://cn.bing.com' + image_info['url'].replace('1920x1080', 'UHD')
    print('title %s, image url %s' % (title, image_url))

    image_furl = furl(image_url)
    # 提取文件名后缀
    image_id = str(image_furl.args['id'])
    ext_name = image_id[image_id.rfind('.'):]
    print('image ext name %s' % ext_name)

    image_file_path = os.path.join(dir_path, '{0}_{1}{2}'.format(title, date_suffix, ext_name))
    print('image file path %s' % image_file_path)
    # 文件存在, 删除
    # if os.path.exists(image_file_path):
    #     print('remove exists image %s' % image_file_path)
    #     os.remove(image_file_path)

    image_response = requests.get(image_url)
    with open(image_file_path, "wb") as attach:
        attach.write(image_response.content)
    print('save download image finish %s' % image_file_path)


if __name__ == '__main__':
    download_today_wallpaper('/Users/shiliyan/Pictures/wallpaper/bing')
