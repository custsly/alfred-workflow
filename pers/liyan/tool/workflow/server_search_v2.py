import hashlib
import os
import sqlite3
import sys
from sqlite3 import Error

import nltk
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
from ualfred import Workflow3

# 检查并下载 NLTK 数据
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def create_connection(db_file, wf):
    """ 创建一个数据库连接 """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        wf.logger.info(f"成功连接到数据库 {db_file}")
    except Error as e:
        wf.logger.error(e)
    return conn


def create_table(conn, wf):
    """ 创建书签表 """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY,
        icon TEXT,
        environment TEXT,
        title TEXT,
        url TEXT,
        keywords TEXT,
        description TEXT
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        wf.logger.info("表创建成功")
    except Error as e:
        wf.logger.error(e)


def insert_bookmark(conn, bookmark, wf):
    """ 插入一条书签记录 """
    sql = """
    INSERT INTO bookmarks (icon, environment, title, url, keywords, description)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    cur = conn.cursor()
    cur.execute(sql, bookmark)
    conn.commit()
    wf.logger.info(f"书签插入成功，ID: {cur.lastrowid}")


def tokenize_query(query):
    """ 使用 NLTK 进行分词 """
    tokens = word_tokenize(query)
    return [token.lower() for token in tokens]


def calculate_match_score(keyword, fields, weights):
    """ 计算关键词在各字段中的匹配度 """
    match_score = 0
    for field, weight in zip(fields, weights):
        match_score += fuzz.partial_ratio(keyword, str(field).lower()) * weight
    return match_score


def search_bookmarks(conn, query, wf):
    """ 根据查询字符串搜索书签，并要求所有关键词尽量匹配 """
    # 使用 NLTK 分词
    keywords = tokenize_query(query)

    # 获取所有书签记录
    cur = conn.cursor()
    cur.execute("SELECT * FROM bookmarks")
    rows = cur.fetchall()

    # 计算每个记录的匹配度
    results = []
    for row in rows:
        fields = [row[1], row[2], row[3], row[4], row[6]]  # environment, title, url, keywords, description
        weights = [1, 2, 2, 1, 1]  # 赋予不同字段不同的权重
        match_score = sum(calculate_match_score(keyword, fields, weights) for keyword in keywords)
        wf.logger.info(f'{row[6]} score {match_score}')
        if match_score > 0:
            results.append((row, match_score))

    # 按匹配度排序
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]


def flow(search_keyword):
    # workflow
    wf = Workflow3()
    wf.logger.info('server search_keyword %s', search_keyword)

    database = "bookmarks.db"

    # 创建数据库连接
    conn = create_connection(database, wf)

    # 创建表
    if conn is not None:
        # 使用缓存, 1min
        cache_key = f"server_{hashlib.md5(search_keyword.encode('utf-8')).hexdigest()}"
        bookmark_list = wf.cached_data(cache_key, lambda: search_bookmarks(conn, search_keyword, wf), max_age=1)
        os_cwd = os.getcwd()
        for item in bookmark_list:
            wf.logger.info('add bookmark %s', item)
            item_data = item[0]
            icon_name = item_data[1] if item_data[1] else 'default.ico'
            icon_path = os.path.join(os_cwd, 'icons', icon_name)
            wf.add_item(title=item_data[6], subtitle=item_data[4], arg=item_data[4], valid=True, icon=icon_path)
        wf.send_feedback()
    else:
        wf.logger.error("无法创建数据库连接")


def main():
    flow(sys.argv[1])


if __name__ == '__main__':
    main()
