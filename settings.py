"""
uni_sdk配置文件
"""
import pymysql
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
log_rotating_when='midnight' # 日志时间切割点
"""
“S”: Seconds
“M”: Minutes
“H”: Hours
“D”: Days
“W”: Week day (0=Monday)
“midnight”: Roll over at midnight
"""
log_backup_count = 100 # 保留日志的个数
log_base_dir= os.path.join(ROOT,'logs')
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

if __name__ == "__main__":
    ROOT = os.path.dirname(os.path.abspath(__file__))
    LOG = os.path.join(ROOT, 'log')

