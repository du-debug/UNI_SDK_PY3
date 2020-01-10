"""
登录请求处理
"""

class LoginRequest(object):


    keys = ('account', 'session', 'ext', 'sign')

    def __init__(self, *args, **kwargs):
        pass

    def process(self, request_handler, params):
        """由此处理具体业务逻辑"""
        print(params)
        return True

    def get_params_keys(self):
        return LoginRequest.keys
