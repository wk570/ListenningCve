api_key = "#######################"
GITHUB_TOKEN = "######################"
HOSTNAME = "127.0.0.1"
# Mysql监听的端口号
PORT = 3306
# 连接Mysql的用户名
USERNAME = '####'
# 连接Mysql的密码
PASSWORD = '####'
# Mysql上创建的数据库名称
DATABASE = '####'

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@" \
         f"{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI
