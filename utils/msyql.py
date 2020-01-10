"""
先使用pymsql,简单处理
"""

import pymysql


class  Mysql(object):

    def __init__(self, *args, **kwargs):
        self._client = pymysql.connect(**kwargs)
        self._cursor = self._client.cursor()

    def query(self, sql_str, callback):
        self._cursor.execute(sql_str)
        result = self._cursor.fetchall()
        callback(result)

if __name__ == "__main__":

    client = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db='uni_talkingsdk_production', cursorclass = pymysql.cursors.DictCursor)
    cursor = client.cursor()
    cursor.execute("select * from apps where id = 1")
    print(cursor.fetchall()[0])


