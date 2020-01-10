"""
登录请求处理
"""

class LoginRequest(object):


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
        callback({'name':'duweihua'}, "成功")

    def get_params_keys(self):
        return LoginRequest.keys
