"""
uni_sdk 启动文件
"""
from tornado.options import define, options
from tornado.web import Application, RequestHandler
from utils.msyql import Mysql
from utils.handler_mixin import HandlerMixin
from common.sign_mixin import SignMixin


import settings
import platform_defines
import tornado.options
import tornado.ioloop


class Web(RequestHandler, HandlerMixin):
    """处理请求公共"""

    def initialize(self, mysql):
        self._mysql = mysql


    def prepare(self):
        pass


    def get(self, app_id, platform, action):

        self.handle_request_with_process(int(app_id), platform, action)


    def post(self):
        pass


class Login(Web, SignMixin):
    """登录"""

    def check_sign(self, params):
        return params['sign'] == self.calc_sign(params) if params['sign'] else False


def start():
    try:
        mysql = Mysql(**settings.database_configs[options.mode])  # 初始化数据库链接
        platform_defines.import_platforms()  # 导入渠道配置
        application = Application([
            (r"/(?P<app_id>[^/]+)/(?P<platform>[^/]+)/(?P<action>login_request)", Login, dict(mysql=mysql)), # 登录模块
        ])
        application.listen(port=options.port, address=options.address)
        tornado.ioloop.IOLoop.current().start()
    except Exception as e:
        tornado.ioloop.IOLoop.current().stop() # 停止当前io循环
        print(e)



def main():
    # 定义全局变量,命令行参数
    define("port", default=8080, help="run on the given port", type=int)
    define("address", default='127.0.0.1', help="run on the default address 127.0.0.1")
    define("daemon", default=settings.daemon, help="run as daemon", type=bool)
    define("webgate", default=settings.webgate, help="run on web gate mode", type=bool)
    define("log_to_file", default=False, help="log to file", type=bool)
    define("game_host", default=settings.game_servers['development']['host'], help="bind address", type=str)
    define("game_port", default=settings.game_servers['development']['port'], help="run on the given port", type=int)
    define("mode", default="local_test", help="default run in development mode", type=str)

    # 从命令行分析全局变量
    tornado.options.parse_command_line(final=False)  # final=False不执行分析回调
    # TODO 有戏服务器暂且搁置
    # game_server = settings.game_servers[options.mode]
    # assert game_server

    if options.daemon:
        pass

    # start
    start()

if __name__ == "__main__":
    main()