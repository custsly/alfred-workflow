# coding=utf-8
import os
import sys


def format_table_name(file_path, sql):
    """
    格式化表名
    :param file_path: 文件路径
    :param sql: sql语句
    :return: 替换后的sql
    """
    sql_file_name = os.path.splitext(os.path.split(file_path)[1])[0]
    return sql.replace('`Table`', sql_file_name)


def format_column_names(sql):
    """
    格式化values前面的列名
    :param sql:
    :return:
    """
    values_idx = sql.index('VALUES')
    column_names = sql[:values_idx]
    column_names = column_names.replace("'", '')
    return column_names + sql[values_idx:]


if __name__ == '__main__':
    # sql_file_path = '~/Downloads/test.sql'

    sql_file_path = None
    if len(sys.argv) > 1:
        sql_file_path = sys.argv[1]

    if sql_file_path is None or not os.path.isfile(sql_file_path):
        print('请选择一个文件')
        sys.exit(0)

    with open(sql_file_path, 'r') as sql_file:
        insert_sql = sql_file.read()
        insert_sql = format_table_name(sql_file_path, insert_sql)
        insert_sql = format_column_names(insert_sql)
        print(insert_sql)

    if insert_sql is not None:
        with open(sql_file_path, 'w') as sql_file:
            sql_file.write(insert_sql)

    print('Finish...')
