"""
分发到具体模块mixin
"""
import platform_defines
import json
import constant


class HandlerMixin(object):


    def find_app(self, app_id, on_app_found):
        """查apps表"""
        if not app_id:
            # TODO 处理逻辑为如果没有app_id怎么返回
            pass
        sql_str = "select * from apps where id={}".format(app_id)

        def callback(result):
            if not result:
                # TODO 查询结果为空怎么处理
                pass
            app_params = result[0]
            on_app_found(app_params)

        self._mysql.query(sql_str, callback)

    def find_handler(self, app_params, platform_id, handler_name, on_find_handler):
        if not app_params:
            # TODO 查询结果为空怎么处理
            pass
        # 老sdk业务逻辑保留
        if  int(app_params['id']) == 300 and platform_id == 0:
            platform_id = 72
        where = " app_id=%s AND distributor_id=%s " % (int(app_params['id']), platform_id)
        # 添加 登录和支付 限制
        if handler_name == "login_request":
            where += " AND nologin=0 "
        elif handler_name == "create_order":
            where += " AND norecharge=0 "
        sql_str = "SELECT * FROM distribution_infos WHERE %s" % where

        def callback(result):
            handler = None
            if not result:
                # TODO 查询结果为空怎么处理
                pass
            # 实名认证
            elif handler_name == 'check_real_name':
                if result[0]['check_real_name'] == '0':
                    # 返回数据不需要开启实名认证
                    data = {
                        'real_name_on': 0
                    }
                elif result[0]['check_real_name'] == '1':
                    # 返回数据开启实名认证
                    data = {
                        'real_name_on': 1
                    }
                self.write(json.dumps(data))
                self.finish()
            else:
                handlers = platform_defines.get_platform_by_id(platform_id)
                if handlers and handler_name in handlers:
                    # 再次实例化对象
                    handler = handlers[handler_name](mysql=self._mysql, platform_info=result[0], app=app_params)
                    # 给login添加属性platform_info
                    self.platform_info = result[0]
            on_find_handler(handler)

        self._mysql.query(sql_str, callback)

    def handle_request_with_process(self, app_id, platform, handler_name):
        """
        :param app_id: 有戏sdk方id
        :param plat_id: 渠道id或者渠道名称
        :param action: 请求分类
        """
        platform_id = int(platform) if platform.isdigit() else platform_defines.name_to_id(platform)
        if not platform_id:
            # TODO 处理逻辑为如果没有渠道id怎么返回
            pass

        def on_app_found(app_params):
            self._app = app_params
            self.find_handler(app_params, platform_id, handler_name, self.on_find_handler)

        self.find_app(app_id, on_app_found)

    def collect_params(self, keys):
        """同时搜索查询和正文参数"""
        params = {}
        for key in keys:
            p = self.get_argument(key, None)
            if p:
                params[key] = p
        return params

    def on_find_handler(self, handler):
        self.handler, handler_by_handler = handler, False
        if self.handler:
            if hasattr(self.handler, 'parse_params'):
                params = self.handler.parse_params(self)
            elif hasattr(self.handler, 'collect_params'):
                params = self.handler.collect_params(self)
            elif hasattr(self, 'get_params_keys'):
                params = self.collect_params(self.get_params_keys())
            else:
                params = self.collect_params(self.handler.get_params_keys())

            #校验参数
            checked = self.check_sign(params) if hasattr(self, 'check_sign') else self.handler.check_sign(params)
            if checked and self.handler.process(self, params):
                """由此进入具体模块处理业务逻辑"""
                handler_by_handler = True

        if not handler_by_handler:
            self.set_status(constant.HTTP_401, reason='sign not match')
            if not self._finished:
                self.finish()
