"""
登录请求处理
"""
from utils.http_mixin import HttpMixin

class LoginRequest(HttpMixin):


    keys = ('account', 'session', 'ext', 'sign')

    def __init__(self, *args, **kwargs):
        super(LoginRequest, self).__init__()
        self._app = kwargs['app']
        self._mysql = kwargs['mysql']
        self._platform_info = kwargs['platform_info']
        pass

    def process(self, request_handler, params):
        """由此处理具体业务逻辑"""
        self.verify_session(params, request_handler.on_login_callback)
        return True

    def verify_session(self, params, callback):

        def on_request(user_data, resp):
            print("发送请求：{}".format(user_data))

        self.request_get(url="http://www.baidu.com", params={}, callback=on_request, user_data="duweihua")
        callback({'name':'duweihua'}, "成功")

    def get_params_keys(self):
        return LoginRequest.keys
