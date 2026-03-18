import pytest
import logging
import os
import json
from utils.api_client import TodoAPIClient

logger = logging.getLogger(__name__)

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