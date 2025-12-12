# -*- coding: UTF-8 -*-
import csv
import hashlib
import os
import sys
import pickle
from functools import lru_cache
from typing import List, Optional, Tuple

# from fuzzywuzzy import fuzz
from ualfred import Workflow3


class WebServer(object):
    __slots__ = ['server_env', 'server_name', 'server_url', 'server_icon', '_ratio', '_search_text']

    def __init__(self, server_env: str, server_name: str, server_url: str, ratio: int, server_icon: str):
        self.server_env = server_env
        self.server_name = server_name
        self.server_url = server_url
        self.server_icon = server_icon
        self._ratio = ratio
        # 预计算搜索文本，避免重复拼接
        self._search_text = f"{server_env} {server_name} {server_url}".lower()

    @property
    def ratio(self) -> int:
        return self._ratio

    @ratio.setter
    def ratio(self, value: int):
        self._ratio = value

    @property
    def search_text(self) -> str:
        return self._search_text

    def __str__(self) -> str:
        return f'[{self.server_env}, {self.server_name}, {self.server_url}]'

    def __hash__(self) -> int:
        return hash((self.server_env, self.server_name, self.server_url))

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return (self.server_env, self.server_name, self.server_url) == \
                (other.server_env, other.server_name, other.server_url)
        return False


class ServerCache:
    """服务器数据缓存管理器"""

    def __init__(self, csv_file_path: str, cache_file_path: str):
        self.csv_file_path = csv_file_path
        self.cache_file_path = cache_file_path
        self._servers: List[WebServer] = []
        self._csv_mtime = 0

    def _get_csv_mtime(self) -> float:
        """获取CSV文件修改时间"""
        try:
            return os.path.getmtime(self.csv_file_path)
        except OSError:
            return 0

    def _load_from_csv(self) -> List[WebServer]:
        """从CSV文件加载服务器数据"""
        servers = []
        os_cwd = os.path.dirname(self.csv_file_path)

        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                server_csv_list = list(reader)

                for server_attr in server_csv_list[1:]:  # 跳过标题行
                    if len(server_attr) < 4:
                        continue

                    icon_name = server_attr[0] if server_attr[0] else 'default.ico'
                    icon_path = os.path.join(os_cwd, 'icons', icon_name)

                    # 预验证图标文件是否存在
                    if not os.path.exists(icon_path):
                        icon_path = os.path.join(os_cwd, 'icons', 'default.ico')

                    servers.append(WebServer(
                        server_attr[1], server_attr[2], server_attr[3], 0, icon_path
                    ))
        except (IOError, csv.Error) as e:
            print(f"Error reading CSV file: {e}")
            return []

        return servers

    def _save_cache(self, servers: List[WebServer], mtime: float):
        """保存缓存到文件"""
        try:
            cache_data = {
                'servers': servers,
                'mtime': mtime
            }
            with open(self.cache_file_path, 'wb') as f:
                pickle.dump(cache_data, f)
        except (IOError, pickle.PickleError):
            pass  # 缓存失败不影响主要功能

    def _load_cache(self) -> Tuple[List[WebServer], float]:
        """从缓存文件加载数据"""
        try:
            with open(self.cache_file_path, 'rb') as f:
                cache_data = pickle.load(f)
                return cache_data.get('servers', []), cache_data.get('mtime', 0)
        except (IOError, pickle.PickleError):
            return [], 0

    def get_servers(self) -> List[WebServer]:
        """获取服务器列表，优先使用缓存"""
        current_mtime = self._get_csv_mtime()

        # 如果内存中有数据且CSV未修改，直接返回
        if self._servers and self._csv_mtime == current_mtime:
            return self._servers

        # 尝试从缓存文件加载
        cached_servers, cached_mtime = self._load_cache()
        if cached_servers and cached_mtime == current_mtime:
            self._servers = cached_servers
            self._csv_mtime = cached_mtime
            return self._servers

        # 从CSV重新加载
        self._servers = self._load_from_csv()
        self._csv_mtime = current_mtime

        # 保存到缓存
        self._save_cache(self._servers, current_mtime)

        return self._servers


@lru_cache(maxsize=128)
def calculate_match_score(search_keyword_lower: str, server_search_text: str,
                          server_env: str, server_name: str, server_url: str) -> int:
    """计算匹配分数，使用LRU缓存避免重复计算"""
    # 基础模糊匹配分数
    fuzz = __import__('fuzzywuzzy.fuzz', fromlist=['fuzz'])
    token_set_ratio = fuzz.token_set_ratio(search_keyword_lower, server_search_text)

    # 精确匹配加分
    if search_keyword_lower in server_env.lower():
        token_set_ratio += 150  # 环境名精确匹配权重最高
    elif search_keyword_lower in server_name.lower():
        token_set_ratio += 120  # 服务器名精确匹配
    elif search_keyword_lower in server_url.lower():
        token_set_ratio += 100  # URL匹配

    return token_set_ratio


def search_servers(search_keyword: str, wf: Workflow3, server_cache: ServerCache) -> Optional[List[WebServer]]:
    """搜索服务器"""
    if not search_keyword.strip():
        return None

    search_keyword_lower = search_keyword.lower().strip()
    servers = server_cache.get_servers()

    if not servers:
        return None

    matched_servers = []

    # 使用生成器表达式和早期过滤来提升性能
    for server in servers:
        score = calculate_match_score(
            search_keyword_lower,
            server.search_text,
            server.server_env,
            server.server_name,
            server.server_url
        )

        if score > 30:  # 提高阈值，过滤低质量匹配
            server.ratio = score
            matched_servers.append(server)

            # 如果找到足够多的高质量匹配，可以提前结束
            if len(matched_servers) >= 20 and score > 150:
                break

    if not matched_servers:
        return None

    # 使用更高效的排序
    matched_servers.sort(key=lambda x: x.ratio, reverse=True)

    # 记录日志
    for server in matched_servers[:5]:  # 只记录前5个结果的日志
        wf.logger.info('server: %s, score: %s', server, server.ratio)

    return matched_servers[:10]


def flow(search_keyword: str):
    """主流程"""
    # workflow
    wf = Workflow3()
    wf.logger.info('server search_keyword: %s', search_keyword)

    # 初始化缓存管理器
    os_cwd = os.getcwd()
    csv_file_path = os.path.join(os_cwd, 'servers.csv')
    cache_file_path = os.path.join(os_cwd, '.server_cache.pkl')
    server_cache = ServerCache(csv_file_path, cache_file_path)

    # 使用Alfred的缓存机制，但缓存时间延长到5分钟
    cache_key = f"server_search_{hashlib.md5(search_keyword.encode('utf-8')).hexdigest()}"

    try:
        server_list = wf.cached_data(
            cache_key,
            lambda: search_servers(search_keyword, wf, server_cache),
            max_age=300  # 5分钟缓存
        )

        if server_list:
            for item in server_list:
                wf.add_item(
                    title=f'{item.server_env}-{item.server_name}',
                    subtitle=item.server_url,
                    arg=item.server_url,
                    valid=True,
                    icon=item.server_icon
                )
        else:
            wf.add_item(
                title='No servers found',
                subtitle=f'No servers match "{search_keyword}"',
                valid=False
            )

    except Exception as e:
        wf.logger.error('Error in search: %s', str(e))
        wf.add_item(
            title='Search Error',
            subtitle='An error occurred while searching',
            valid=False
        )

    wf.send_feedback()


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python script.py <search_keyword>")
        sys.exit(1)

    flow(sys.argv[1])


if __name__ == '__main__':
    main()
