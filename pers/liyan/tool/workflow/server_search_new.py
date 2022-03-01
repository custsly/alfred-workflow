# -*- coding: UTF-8 -*-
import csv
import hashlib
import os
import sys

from fuzzywuzzy import fuzz
from workflow import ICON_WEB
from workflow import Workflow3


class WebServer(object):

    def __init__(self, server_env, server_name, server_url, ratio, server_icon):
        self.server_env = server_env
        self.server_name = server_name
        self.server_url = server_url
        self.server_icon = server_icon
        self._ratio = ratio

    @property
    def ratio(self):
        return self._ratio

    def __str__(self):
        return '[%s, %s, %s]' % (self.server_env, self.server_name, self.server_url)

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(id(self)) == hash(id(other))
        else:
            return False


def search_servers(search_keyword, wf):
    csv_file_path = os.path.join(os.getcwd(), 'servers.csv')

    web_server_list = []

    # 读取 csv 文件
    with open(csv_file_path, 'r') as f:
        reader = csv.reader(f)
        server_csv_list = list(reader)
        for server_attr in server_csv_list[1:]:

            if len(server_attr) < 3:
                continue
            # wf.logger.info('server search_servers start cut')
            # cut_search_keyword = ' '.join(jieba.cut(search_keyword))
            # wf.logger.info('server search_servers cut finish...')

            # 如果包含, 匹配度设置为 100
            if search_keyword in server_attr[2:]:
                token_set_ratio = 100
            else:
                # 去重子集匹配
                token_set_ratio = fuzz.partial_token_set_ratio(search_keyword, ' '.join(server_attr))

                wf.logger.info('server: %s, token_set_ratio: %s', server_attr, token_set_ratio)

            if token_set_ratio > 0:
                icon_name = server_attr[1] if server_attr[1] else 'default.ico'
                icon_path = os.path.join(os.getcwd(), 'icons', icon_name)
                web_server_list.append(
                    WebServer(server_attr[0], server_attr[2], server_attr[3], token_set_ratio, icon_path))

        web_server_list.sort(key=lambda x: x.ratio, reverse=True)

    return web_server_list if len(web_server_list) > 0 else None


def flow(search_keyword):
    # workflow
    wf = Workflow3()
    wf.logger.info('server search_keyword %s', search_keyword)

    # 使用缓存, 1min
    cache_key = 'server_%s' % hashlib.md5(search_keyword.encode('utf-8')).hexdigest()
    server_list = wf.cached_data(cache_key, lambda: search_servers(search_keyword, wf), max_age=60)

    for item in server_list:
        wf.logger.info('add server %s', item)
        wf.add_item(title='%s-%s' % (item.server_env, item.server_name), subtitle=item.server_url, arg=item.server_url,
                    valid=True, icon=item.server_icon)

    wf.send_feedback()


def main():
    flow(sys.argv[1])


if __name__ == '__main__':
    main()
