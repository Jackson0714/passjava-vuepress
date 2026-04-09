#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门修复date字段为2026-04-09的文件，替换为git历史时间
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime


def get_git_creation_date(file_path):
    """获取文件的git首次提交日期"""
    file_path_obj = Path(file_path)
    repo_root = Path(__file__).parent

    try:
        # 获取相对于仓库根目录的路径
        rel_path = file_path_obj.relative_to(repo_root)

        cmd = ['git', 'log', '--follow', '--format=%ad', '--date=short', '--reverse', '--', str(rel_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=repo_root, timeout=5)

        if result.returncode == 0 and result.stdout.strip():
            # 获取第一行（最早的提交日期）
            lines = result.stdout.strip().split('\n')
            if lines:
                first_date = lines[0].strip()
                if first_date and re.match(r'^\d{4}-\d{2}-\d{2}$', first_date):
                    return first_date
    except Exception:
        return None

    return None


def fix_file_date(file_path):
    """修复单个文件的date字段"""

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否有frontmatter
    if not content.startswith('---'):
        return False

    # 查找frontmatter的结束位置
    first_end = content.find('---', 3)
    if first_end == -1:
        return False

    frontmatter_content = content[3:first_end]
    rest_content = content[first_end:]

    # 检查是否包含date: 2026-04-09
    if 'date: 2026-04-09' not in frontmatter_content:
        return False

    # 获取git历史时间
    git_date = get_git_creation_date(file_path)
    if not git_date:
        print(f"跳过 {file_path}: 无法获取git历史时间")
        return False

    # 如果git时间也是2026-04-09，则跳过
    if git_date == '2026-04-09':
        return False

    # 替换date字段
    new_frontmatter = frontmatter_content.replace('date: 2026-04-09', f'date: {git_date}')

    # 重建内容
    new_content = '---' + new_frontmatter + rest_content

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ 已修复: {file_path}")
    print(f"  - 从: date: 2026-04-09")
    print(f"  - 到: date: {git_date}")

    return True


def main():
    """主函数：查找并修复date字段为2026-04-09的文件"""

    docs_dir = Path(__file__).parent / 'docs'

    if not docs_dir.exists():
        print(f"错误: 目录 {docs_dir} 不存在")
        return

    # 查找所有markdown文件
    exclude_dirs = {'node_modules', '.vuepress', '.obsidian', '.git', 'snippets'}
    md_files = []

    for md_file in docs_dir.rglob('*.md'):
        if not any(exclude_dir in md_file.parts for exclude_dir in exclude_dirs):
            md_files.append(md_file)

    print(f"扫描 {len(md_files)} 个markdown文件，查找date: 2026-04-09...\n")
    print("="*80)

    fixed_count = 0
    total_count = 0

    for md_file in sorted(md_files):
        # 读取文件内容检查是否有date: 2026-04-09
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read(500)  # 只读取前500个字符，应该足够包含frontmatter

            if 'date: 2026-04-09' in content:
                total_count += 1
                print(f"\n发现date: 2026-04-09: {md_file.relative_to(docs_dir)}")
                if fix_file_date(str(md_file)):
                    fixed_count += 1
        except Exception as e:
            print(f"错误读取文件 {md_file}: {e}")

    print(f"\n{'='*80}")
    print(f"处理完成!")
    print(f"找到 {total_count} 个包含date: 2026-04-09的文件")
    print(f"成功修复 {fixed_count} 个文件")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()