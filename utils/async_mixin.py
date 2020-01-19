"""
使用数据库连接池链接数据库,并测试
使用思想：每执行一次sql，就从链接池中取出一个链接，执行完关闭链接
"""
# 参考文档地址：https://blog.csdn.net/daerzei/article/details/83865325
import time
import sys
import pymysql
import threading

from functools import partial
from queue import Queue, Empty
from DBUtils.PooledDB import PooledDB
from functools import wraps, partial
from tornado.ioloop import IOLoop
from utils.log_mixin import LogMixin

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
            **kwargs
        )  # 初始化
        super(DbutilsMySql, self).__init__()

    def query(self, sql_str):
        """查询"""
        db_cursor = self.db_pool.connection().cursor()
        db_cursor.execute(sql_str)
        result = db_cursor.fetchone()

# 正式开发
class AsyncMixin(object):
    def __init__(self,
                 thread_klass=None,
                 thread_klass_args=None,
                 num_threads=10,
                 queue_timeout=1,
                 ioloop=None
                 ):
        super(AsyncMixin, self).__init__()
        self._thread_klass = thread_klass
        self._thread_klass_args = thread_klass_args
        self._ioloop = ioloop or IOLoop.current()
        self._queue = Queue(maxsize=15)
        self._queue_timeout = queue_timeout
        self._threads = []
        self._running = True
        for i in range(num_threads):
            name = "thread_%d" % i
            thread_klass_args['name'] = name
            t = thread_klass(**thread_klass_args)  # 实例化多线程的类和数据库链接初始化
            t.start()
            self._threads.append(t) # TODO 暂且搁置

    def add_task(self, func, callback=None):
        """往队列里面添加任务"""
        self._queue.put((func, callback))

    def stop(self):
        self._running = False

class WorkerThread(threading.Thread, LogMixin):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self._name = kwargs.get('name', None)
        self._pool = kwargs.get('pool', None)
        self.log_info("WorkerThread created: %s" % self._name)

    def run(self):
        """执行队列里面的任务"""
        queue = self._pool._queue
        queue_timeout = self._pool._queue_timeout
        while self._pool._running:
            try:
                (func, callback) = queue.get(True, queue_timeout)
                queue.task_done() # 剪掉任务
                handler = self.get_handler()
                result = None
                ex = None
                if hasattr(handler, func.func.__name__):
                    try:
                        sql_str = func()
                        result = getattr(handler, func.func.__name__)(*sql_str)
                    except Exception as e:
                        ex = sys.exc_info() # 报错信息
                else:
                    raise ValueError("%s not found" % func.func.__name__)
                if callback:
                    # 要为当前io
                    self._pool._ioloop.add_callback(partial(callback, result, ex))
            except Empty:
                pass
        if hasattr(self, 'close'):
            """释放连接池中coon和cursor"""
            print("释放资源")
            self.close()

def async_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]  # obj为AsyncMysql的引用
        if isinstance(obj, AsyncMixin):
            callback = None
            if 'callback' in kwargs:
                callback = kwargs['callback']
            # 添加到队列
            obj.add_task(partial(func, *args, **kwargs), callback)
        else:
            raise ValueError("decorator must apply to a instance of AsyncMixin")
    return wrapper

def async_class(klass):
    if hasattr(klass, '__async_methods__'):
        async_methods = getattr(klass, '__async_methods__')
        for name in async_methods:
            method = getattr(klass, name)
            setattr(klass, name, async_thread(method))  # 重置了查询sql的方法,并且添加到队列里面
    return klass

# 检测数据库链
def check_mysql_coonect(f):
    def in_func(*args, **kwargs):
        handler = args[0]
        try:
            handler.coon.ping()
        except Exception:
            handler.connect()
        return f(*args, **kwargs)
    return in_func


if __name__ == "__main__":

    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'uni_talkingsdk_production',
        'user': 'root',
        'password': 'mysql'
    }

    db_test = DbutilsMySql(**db_config)
    sql_str = "select * from distribution_infos"
    start_time = time.time()
    for i in range(10000):
        db_test.query(sql_str)
    end_time = time.time()
    print("运行时间:{}".format(end_time - start_time))

