"""
tornado提供的异步客户端
"""
import asyncio
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPClient

class HttpMixin(object):

    async def async_request_get(self, url, params, callback, user_data=None):
        url = url_concat(url, params)
        client = AsyncHTTPClient()
        request = HTTPRequest(url, connect_timeout=10)
        resp = await client.fetch(request)
        callback(user_data, resp)

    async def async_request_post(self,url,body,callback,user_data=None):
        client = AsyncHTTPClient()
        if isinstance(url, HTTPRequest):
            request = url
            url = request.url
        else:
            request = HTTPRequest(url, method="POST", body=body, connect_timeout=10)
        resp = await client.fetch(request)
        callback(user_data, resp)

    def request_get(self, url, params, callback, user_data=None):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.async_request_get(url, params, callback, user_data), loop)


    def request_post(self, url,body,callback,user_data=None):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.async_request_post(url,body,callback,user_data), loop)
        loop.close()


if __name__ == "__main__":

    test = HttpMixin()
    url = 'http://www.google.com'
    def callback(user_data, result):
        print(user_data)
        print(result.body)
    test.request_get(url, {}, callback, {})
