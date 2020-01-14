"""
渠道参数定义在此
"""
from tornado.util import import_object

ePlatform_test = 428  # 测试渠道

__name_to_id__ = dict(
    test = ePlatform_test,
)

__actives__ = [
    "test"
]

__platform_configs__ = []
__platform_id_to_handler__ = {}  # 包含了模块各个处理类对象

def get_platform_by_id(_id):
    return __platform_id_to_handler__.get(_id,None)

def name_to_id(name):
    return __name_to_id__.get(name, None)

def import_platforms():
    for p in __actives__:
        old_p = p
        index = p.find("_")
        if index != -1:
            p = p[:index]
            pInfo = dict(nPlatformID=name_to_id(old_p), szPrefix=old_p + '_')
        else:
            # TODO 业务逻辑待完善
            pInfo = dict(nPlatformID=name_to_id(old_p), szPrefix=old_p + '_')
        pm = import_object(p)
        __platform_id_to_handler__[name_to_id(old_p)] = getattr(pm, 'get_handlers')()
        __platform_configs__.append(pInfo)



if __name__ == "__main__":

    def do_import_platforms():
        import_platforms()
        for p in __platform_configs__:
            print(p['szPrefix'])

    do_import_platforms()
    print(get_platform_by_id(0))