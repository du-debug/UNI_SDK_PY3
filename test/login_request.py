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

        return True

    def get_params_keys(self):
        return LoginRequest.keys
