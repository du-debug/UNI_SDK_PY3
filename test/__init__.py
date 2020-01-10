"""
从这里导入模块里面的具体内容
使用相对路径导报,可能会发报错
"""

from test.login_request import LoginRequest

handlers = {
    "login_request": LoginRequest
}

def get_handlers():
    """返回具体处理类对象"""
    return handlers
