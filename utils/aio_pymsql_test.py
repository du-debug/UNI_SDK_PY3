"""
异步数据库链接aio_mysql测试
"""
import settings
import asyncio
import aiomysql
loop = asyncio.get_event_loop()


class AioMysqlTest(object):

    async def connect(self, *args, **kwargs):
        kwargs['loop'] = loop
        coon = await aiomysql.connect(**kwargs)
        cur = await coon.cursor()
        await cur.execute("select * from apps")
        print(cur.description)
        r = await cur.fetchall()
        print(r)
        await cur.close()
        coon.close()
if __name__ == "__main__":
    test = AioMysqlTest()
    loop.run_until_complete(test.connect(**settings.database_configs['aio_local_test']))
    # print(settings.database_configs['aio_local_test'])

