#!/usr/bin/env python
"""运行所有测试并生成报告"""
import os
import sys
import subprocess
import datetime


def main():
    # 创建必要的目录
    os.makedirs("reports", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # 生成带时间戳的报告文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/todo_api_report_{timestamp}.html"

    # 设置环境变量（可选）
    env = os.environ.copy()
    env["TEST_ENV"] = "测试环境"

    # 运行 pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        f"--html={report_file}",
        "--self-contained-html"
    ]

    print(f"运行测试，报告将保存到: {report_file}")
    result = subprocess.run(cmd, env=env)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()