import pymysql
from src.database_setup import get_engine, DatabaseManager
from src.config import get_db_config

def create_database():
    """根据 `.env` 中的配置，创建 MySQL 数据库（如果不存在）。

    该函数会加载环境变量，然后以不指定数据库的方式连接 MySQL，执行
    `CREATE DATABASE IF NOT EXISTS ...`。调用者可在程序启动时先调用此函数。
    """
    cfg = get_db_config()
    host = cfg['host']
    port = cfg['port']
    user = cfg['user']
    password = cfg['password']
    dbname = cfg['database']

    conn = pymysql.connect(host=host, port=port, user=user, password=password, autocommit=True)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
    finally:
        conn.close()

    print("数据库创建完成（若不存在）。")


def initialize_database():
    """初始化数据库表结构（如果尚未创建）。

    先确保数据库存在（调用 `create_database()`），再通过 SQLAlchemy 创建表结构。
    """
    print("正在检查数据库表结构...")
    # 确保数据库已创建
    create_database()

    engine = get_engine()
    with engine.connect() as conn:
        with conn.begin():
            db_manager = DatabaseManager()
            db_manager.init_all_tables(conn)

    print("数据库表结构初始化完成。")


def create_test_data():
    """创建测试数据（可选）"""
    print("正在创建测试数据...")
    engine = get_engine()
    with engine.connect() as conn:
        with conn.begin():
            db_manager = DatabaseManager()
            db_manager.create_test_data(conn)
    print("测试数据创建完成。")