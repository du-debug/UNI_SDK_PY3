"""
使用数据库连接池链接数据库,并测试
"""

# 参考文档地址：https://blog.csdn.net/daerzei/article/details/83865325
import time
import datetime
import pymysql
from DBUtils.PooledDB import PooledDB
from utils.async_mixin import check_mysql_coonect

# 测算时间装饰器
def run_time(f):
    def in_func(*args, **kwargs):
        start_time = time.time()
        f(*args, **kwargs)
        end_time = time.time()
        print("运行时间:{}".format(end_time-start_time))
    return in_func


class DbutilsMySql(object):

    def __init__(self, *args, **kwargs):
        self.db_pool = PooledDB(
            creator=pymysql,  # 指定数据库驱动
            maxconnections=3,  # 连接池允许的最大连接数,0和None表示没有限制
            mincached=3,  # 初始化时,连接池至少创建的空闲连接,0表示不创建
            maxcached=3,  # 连接池中空闲的最多连接数,0和None表示没有限制
            maxshared=3,  # 连接池中最多共享的连接数量
            blocking=True,  # 连接池中如果没有可用共享连接后,是否阻塞等待,True表示等等
            setsession=[],  # 开始会话前执行的命令列表
            ping=0,  # ping Mysql服务器检查服务是否可用
            **args[0]
        )  # 初始化
        super(DbutilsMySql, self).__init__()

    def connect(self):
        self.coon = self.db_pool.connection()
        self.cursor = self.coon.cursor()

    # @check_mysql_coonect
    def query_hash(self, sql_str):
        self.connect()
        try:
            self.cursor.execute(sql_str)
            result = self.cursor.fetchall()
        except Exception as e:
            pass
        return result

    def close(self):
        """释放连接池中的coon和cursor"""
        self.cursor.close()
        self.coon.close()


class PymsqlTest(object):
    def __init__(self, *args, **kwargs):
        pymysql.connect(**args[0])

    def query_hash(self, sql_str):
        return [{'a':1}]


if __name__ == "__main__":

    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'uni_talkingsdk_production',
        'user': 'root',
        'password': 'mysql'
    }
    start_time = datetime.datetime.now()
    for thread_num in range(10):
        db_pool = DbutilsMySql(**db_config)
        db_pool.start()
    end_time = datetime.datetime.now()
    print("总共话费时间:{}".format(end_time-start_time))

