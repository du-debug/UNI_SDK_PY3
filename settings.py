"""
uni_sdk配置文件
"""
import pymysql

game_servers = dict(
    production=dict(host='10.68.237.133', port=8885),
    development=dict(host='119.147.215.27', port=8885)
)

# 数据库配置
database_configs = dict(
    development = dict(
        charset = 'utf8',
        database= 'uni_talkingsdk_development',
        username= 'uni_server',
        password= 'uni_2015.password',
        host= '10.68.237.30'
    ),
    production = dict(
        charset = 'utf8',
        database= 'uni_talkingsdk_production',
        username= 'uni_server',
        password= 'uni_2015.password',
        host= '10.68.237.30'
    ),
    local_test = dict(
            db= 'uni_talkingsdk_production',
            user= 'root',
            passwd = 'mysql',
            host= '127.0.0.1',
            cursorclass = pymysql.cursors.DictCursor  # sql查询结果以字典形式输出
        ),

)

daemon = False
webgate=True