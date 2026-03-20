import socket
import time
import pytest
import logging
import os
import json
from utils.api_client import TodoAPIClient
import subprocess
logger = logging.getLogger(__name__)

import mysql.connector
from mysql.connector import Error
import time


def wait_for_mysql(port=3307, host="localhost", timeout=60):
    """等待 MySQL 真正就绪（能执行查询）"""
    import mysql.connector
    from mysql.connector import Error

    start_time = time.time()
    last_error = None

    while time.time() - start_time < timeout:
        try:
            # 尝试建立真实连接并执行查询
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user='root',
                password='123456',
                connection_timeout=3
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result and result[0] == 1:
                print(f"✅ MySQL 已就绪，返回结果: {result[0]}")
                return True
        except Error as e:
            last_error = e
            print(f"⏳ MySQL 未就绪: {e}")
            time.sleep(2)

    # 如果超时，打印容器状态帮助诊断
    print("=" * 50)
    print("MySQL 超时未就绪，检查容器状态：")
    import subprocess
    subprocess.run(["docker", "ps", "|", "findstr", "mysql"])
    print("\nMySQL 容器日志最后20行：")
    subprocess.run(["docker", "logs", "--tail", "20", "todo-mysql"])
    print("=" * 50)

def wait_for_port(port, host="localhost", timeout=30):
    """等待指定端口可连接"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                logger.info(f"✅ 端口 {port} 已就绪")
                return True
        except Exception:
            pass
        time.sleep(1)
    raise TimeoutError(f"端口 {port} 在 {timeout} 秒内未能就绪")


@pytest.fixture(scope="session", autouse=True)
def docker_services():
    """自动启动 Docker Compose 服务，测试结束后自动停止"""
    logger.info("🚀 启动 Docker Compose 服务...")

    # 启动所有服务（-d 后台运行）
    subprocess.run(["docker-compose", "up", "-d"], check=True)
    try:
        # 等待 MySQL (3307) 和 Redis (6379) 就绪
        wait_for_mysql(3307)
        wait_for_port(6379)
        logger.info("✅ 所有服务已就绪，开始执行测试")

        yield  # 执行测试

    finally:
        # 无论测试成功还是失败，都要清理
        logger.info("🧹 停止 Docker Compose 服务...")
        subprocess.run(["docker-compose", "stop"], check=True)
        # logger.info("🧹 清理 Docker Compose 服务...")
        # subprocess.run(["docker-compose", "down"], check=True)
        # , "-v"


@pytest.fixture(scope="session")
def base_url():
    """基础 URL，可从环境变量读取"""
    url = os.environ.get("API_BASE_URL", "https://jsonplaceholder.typicode.com")
    logger.info(f"使用 API 基础 URL: {url}")
    return url

@pytest.fixture(scope="session")
def http_session():
    """HTTP 会话 fixture"""
    import requests
    session = requests.Session()
    session.headers.update({
        "User-Agent": "pytest-todo-api-test",
        "Accept": "application/json"
    })
    logger.info("创建 HTTP 会话")
    yield session
    logger.info("关闭 HTTP 会话")
    session.close()

@pytest.fixture(scope="session")
def api_client(base_url, http_session):
    """API 客户端 fixture"""
    logger.info("初始化 API 客户端")
    return TodoAPIClient(base_url, http_session)

@pytest.fixture
def todo_test_data():
    """加载待办事项测试数据"""
    data_file = os.path.join(os.path.dirname(__file__), "data", "todos.json")
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)

# 自定义报告标题
def pytest_html_report_title(report):
    report.title = "待办事项 API测试报告"

# 添加环境信息
def pytest_configure(config):
    if hasattr(config, '_metadata'):
        config._metadata["项目名称"] = "待办事项 API测试"
        config._metadata["测试环境"] = os.environ.get("TEST_ENV", "测试环境")
        config._metadata["测试负责人"] = "测试团队"