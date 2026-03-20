import pytest
import redis
import mysql.connector
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def redis_client():
    """连接 Docker 里的 Redis"""
    client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )
    yield client
    # Redis 连接不需要显式关闭


@pytest.fixture
def mysql_connection():
    """连接 Docker 里的 MySQL"""
    conn = mysql.connector.connect(
        host='localhost',
        port=3307,
        user='root',
        password='123456',
        database='todo_test'
    )
    yield conn
    conn.close()


def test_redis_works(redis_client):
    """测试 Redis 能否正常使用"""
    logger.info("开始测试 Redis...")

    # 写入数据
    redis_client.set("test_key", "pytest_works")

    # 读取数据
    value = redis_client.get("test_key")

    logger.info(f"读取到 Redis 值: {value}")
    assert value == "pytest_works"
    logger.info("✅ Redis 测试通过")


def test_mysql_works(mysql_connection):
    """测试 MySQL 能否正常使用"""
    logger.info("开始测试 MySQL...")

    cursor = mysql_connection.cursor()

    # 创建一个测试表（如果不存在）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

    # 插入测试数据
    cursor.execute("INSERT INTO test_table (name) VALUES ('pytest')")
    mysql_connection.commit()

    # 查询数据
    cursor.execute("SELECT name FROM test_table WHERE name='pytest'")
    result = cursor.fetchone()

    logger.info(f"查询到 MySQL 结果: {result}")
    assert result[0] == "pytest"

    # 清理测试数据
    cursor.execute("DELETE FROM test_table WHERE name='pytest'")
    mysql_connection.commit()

    logger.info("✅ MySQL 测试通过")


def test_combined(redis_client, mysql_connection):
    """测试 Redis 和 MySQL 同时工作"""
    logger.info("开始测试 Redis + MySQL 组合...")

    # Redis 操作
    redis_client.set("combined_test", "redis_ok")
    redis_value = redis_client.get("combined_test")
    assert redis_value == "redis_ok"

    # MySQL 操作
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1

    logger.info("✅ 组合测试通过")