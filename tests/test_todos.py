import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_get_all_todos(api_client):
    """测试获取所有待办事项"""
    logger.info("开始测试: 获取所有待办事项")

    response = api_client.get_todos()

    logger.info(f"响应状态码: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    logger.debug(f"返回数据条数: {len(data)}")
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]

    logger.info("测试通过: 成功获取待办事项列表")


@pytest.mark.regression
@pytest.mark.parametrize("todo_id", [1, 2, 3])
def test_get_todo_by_id(api_client, todo_id):
    """测试根据 ID 获取待办事项"""
    logger.info(f"开始测试: 获取待办 ID={todo_id}")

    response = api_client.get_todo(todo_id)

    logger.info(f"响应状态码: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    logger.debug(f"返回数据: {data}")
    assert data["id"] == todo_id
    assert "title" in data
    assert "completed" in data

    logger.info(f"测试通过: 成功获取待办 ID={todo_id}")


@pytest.mark.regression
@pytest.mark.parametrize("test_case", [
    {"userId": 1, "title": "新待办", "completed": False, "expected": 201},
    {"userId": 2, "title": "另一个待办", "completed": True, "expected": 201},
])
def test_create_todo(api_client, test_case):
    """测试创建待办事项"""
    logger.info(f"开始测试: 创建待办, 数据={test_case}")

    response = api_client.create_todo(test_case)

    logger.info(f"响应状态码: {response.status_code}")
    assert response.status_code == test_case["expected"]

    if response.status_code == 201:
        data = response.json()
        logger.debug(f"创建成功, 返回数据: {data}")
        assert data["title"] == test_case["title"]
        assert data["completed"] == test_case["completed"]
        assert "id" in data

    logger.info("测试通过")


@pytest.mark.slow
def test_update_todo(api_client):
    """测试更新待办事项"""
    logger.info("开始测试: 更新待办")

    # 先创建一个待办
    new_todo = {"userId": 1, "title": "待更新", "completed": False}
    create_resp = api_client.create_todo(new_todo)
    assert create_resp.status_code == 201
    todo_id = create_resp.json()["id"]
    logger.info(f"创建待办成功, ID={todo_id}")

    # 更新它
    update_data = {"title": "已更新", "completed": True}
    response = api_client.update_todo(todo_id, update_data)

    logger.info(f"更新响应状态码: {response.status_code}")
    assert response.status_code == 200

    data = response.json()
    logger.debug(f"更新后数据: {data}")
    assert data["title"] == "已更新"
    assert data["completed"] == True

    logger.info("测试通过: 待办更新成功")

'''
添加新的测试用例：

在 test_todos.py 中新增一个测试，如按 userId 过滤待办。

使用参数化测试多组数据。
'''

@pytest.mark.regression
@pytest.mark.parametrize("user_id, expected_min_count, expected_status", [
    (1, 10, 200),  # userId=1 通常有多个待办
    (2, 5, 200),  # userId=2 也有待办
    (10, 0, 200),  # userId=10 可能没有待办
    (999, 0, 200),  # 不存在的 userId，应该返回空列表而非404
])
def test_get_todos_by_user_id(api_client, user_id, expected_min_count, expected_status):
    """
    测试按 userId 过滤待办事项
    验证：/todos?userId={user_id} 接口
    """
    logger.info("=" * 60)
    logger.info(f"开始测试: 按 userId={user_id} 过滤待办")

    # 发送请求，带上 userId 参数
    params = {"userId": user_id}
    logger.debug(f"请求参数: {params}")

    response = api_client.get_todos(params=params)

    # 记录响应信息
    logger.info(f"响应状态码: {response.status_code}")
    assert response.status_code == expected_status, f"预期状态码 {expected_status}，实际 {response.status_code}"

    # 解析响应数据
    data = response.json()
    actual_count = len(data)
    logger.info(f"返回待办数量: {actual_count}")

    # 验证返回的数据都是指定 userId 的
    if actual_count > 0:
        for i, todo in enumerate(data):
            logger.debug(
                f"待办 {i + 1}: userId={todo.get('userId')}, id={todo.get('id')}, title={todo.get('title')[:20]}...")
            assert todo.get("userId") == user_id, f"待办 userId 应为 {user_id}，实际为 {todo.get('userId')}"

    # 验证返回数量符合预期（至少达到预期最小值）
    assert actual_count >= expected_min_count, f"预期至少 {expected_min_count} 条，实际 {actual_count}"

    logger.info(f"测试通过: userId={user_id} 过滤成功，返回 {actual_count} 条待办")
    logger.info("=" * 60)
