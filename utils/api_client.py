import requests
import logging

logger = logging.getLogger(__name__)


class TodoAPIClient:
    """待办事项 API 客户端封装"""

    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = session or requests.Session()

    def get_todos(self, params=None):
        """获取所有待办事项"""
        url = f"{self.base_url}/todos"
        logger.debug(f"GET {url}, params={params}")
        return self.session.get(url, params=params)

    def get_todo(self, todo_id):
        """获取单个待办事项"""
        url = f"{self.base_url}/todos/{todo_id}"
        logger.debug(f"GET {url}")
        return self.session.get(url)

    def create_todo(self, data):
        """创建待办事项"""
        url = f"{self.base_url}/todos"
        logger.debug(f"POST {url}, data={data}")
        return self.session.post(url, json=data)

    def update_todo(self, todo_id, data):
        """更新待办事项"""
        url = f"{self.base_url}/todos/{todo_id}"
        logger.debug(f"PUT {url}, data={data}")
        return self.session.put(url, json=data)

    def delete_todo(self, todo_id):
        """删除待办事项"""
        url = f"{self.base_url}/todos/{todo_id}"
        logger.debug(f"DELETE {url}")
        return self.session.delete(url)

    def get_userid(self, userid):
        """获取单个待办事项"""
        url = f"{self.base_url}/users/"
        params = {'userId': userid}
        logger.debug(f"GET {url}")
        return self.session.get(url, params=params)