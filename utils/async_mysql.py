"""
使用数据库连接池链接数据库
使用思想：
每次执行sql任务添加到队列里面,使用装饰器实现.
开启多线程执行队列里面的任务.
每执行一次sql,就从链接池中取出一个链接,执行完关闭链接
参考文档地址：https://blog.csdn.net/daerzei/article/details/83865325
"""
from utils.async_mixin import AsyncMixin
from utils.async_mixin import WorkerThread
from utils.msyql import DbutilsMySql, PymsqlTest
from utils.async_mixin import async_class
from utils.aio_pymsql_test import AioMysqlPoll

class MysqlThread(WorkerThread):

    def __init__(self, *args, **kwargs):
        self._mysql = AioMysqlPoll(kwargs['db_config'])
        super(MysqlThread, self).__init__(*args, **kwargs)
        self.daemon = True

    def get_handler(self):
        return self._mysql

    def close(self):
        """释放连接池coon"""
        self._mysql.close()

@async_class
class AsyncMysql(AsyncMixin):
    """
    使用装饰器的目的将执行sql的任务添加对立里面,并会重处理回调函数
    AsyncMixin:开启多个线程,调用start
    init方法里:数据库链接和线程初始化
    """
    __async_methods__ = ['query_hash','select','insert','update','count','delete']

    def __init__(self, db_config, **kwargs):
        kwargs['thread_klass'] = MysqlThread  # 初始化数据库链接和多线程初始化
        kwargs['thread_klass_args'] = dict(pool=self, db_config=db_config)
        super(AsyncMysql, self).__init__(**kwargs)


    def get_thread_pool(self):
        return self

    def query_hash(self,sql, **kwargs):
        return (sql,)

    def select(self,sql,how=1):
        return (sql,)

    def insert(self,sql):
        return (sql,)

    def update(self,sql):
        return (sql, )

    def count(self,sql,field):
        return (sql, field)

    def delete(self,sql):
        return (sql, )

    def close(self):
        # TODO 后续实现
        pass

if __name__ == "__main__":
    from settings import database_configs
    test = AsyncMysql(**database_configs['local_test'])
    # sql_str = '123123'
    # ret = test.query_hash(sql_str, callback=123123)
    pass
