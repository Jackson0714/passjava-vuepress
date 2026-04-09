#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

def get_git_creation_date(file_path):
    """获取文件的git首次提交日期"""
    try:
        # 使用绝对路径
        abs_path = Path(file_path).resolve()
        repo_root = Path(__file__).parent.resolve()

        # 相对于仓库根目录的路径
        rel_path = abs_path.relative_to(repo_root)

        cmd = ['git', 'log', '--follow', '--format=%ad', '--date=short', '--reverse', '--', str(rel_path)]
        print(f"执行命令: {' '.join(cmd)}")
        print(f"工作目录: {repo_root}")

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root)

        print(f"返回码: {result.returncode}")
        print(f"标准输出: {result.stdout.strip()}")
        print(f"标准错误: {result.stderr.strip()}")

        if result.returncode == 0 and result.stdout.strip():
            # 获取第一行（最早的提交日期）
            first_date = result.stdout.strip().split('\n')[0]
            if first_date:
                return first_date
    except Exception as e:
        print(f"异常: {e}")

    return None

# 测试
date = get_git_creation_date('docs/ai/AI-basic/ai-10-picture.md')
print(f"\nGit创建日期: {date}")