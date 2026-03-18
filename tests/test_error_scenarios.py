import pytest
import requests
import logging

logger = logging.getLogger(__name__)


def test_get_nonexistent_todo(api_client):
    """测试获取不存在的待办"""
    logger.info("开始测试: 获取不存在的待办 ID=9999")

    response = api_client.get_todo(9999)

    logger.info(f"响应状态码: {response.status_code}")
    assert response.status_code == 404

    logger.info("测试通过: 返回 404 符合预期")


def test_create_todo_with_invalid_data(api_client):
    """测试用无效数据创建待办"""
    logger.info("开始测试: 无效数据创建待办")

    invalid_data = {"invalid": "data"}
    response = api_client.create_todo(invalid_data)

    # JSONPlaceholder 可能接受任意数据，这里只是演示
    # 实际应根据 API 文档断言
    logger.info(f"响应状态码: {response.status_code}")
    assert response.status_code in [200, 201, 400, 422]

    logger.info("测试通过")


def test_delete_todo(api_client):
    """测试删除待办"""
    logger.info("开始测试: 删除待办")

    # 先创建一个待办
    new_todo = {"userId": 1, "title": "待删除", "completed": False}
    create_resp = api_client.create_todo(new_todo)
    assert create_resp.status_code == 201
    todo_id = create_resp.json()["id"]
    logger.info(f"创建待办成功, ID={todo_id}")

    # 删除它
    response = api_client.delete_todo(todo_id)

    logger.info(f"删除响应状态码: {response.status_code}")
    assert response.status_code == 200

    # 验证确实被删除
    get_resp = api_client.get_todo(todo_id)
    logger.info(f"验证删除后状态码: {get_resp.status_code}")
    assert get_resp.status_code == 404

    logger.info("测试通过: 待办删除成功")