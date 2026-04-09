#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 docs 目录下 markdown 文件的 date 字段：
1. 使用文件的真实创建时间（git首次提交时间或文件系统创建时间）
2. 处理重复的date字段，使用最老的时间值
3. 修复格式不正确的日期（如2025-7-28 -> 2025-07-28）
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
import shutil


def get_file_creation_date(file_path):
    """获取文件的创建日期，优先使用git首次提交时间，其次使用文件系统时间"""

    file_path_obj = Path(file_path)
    repo_root = Path(__file__).parent

    # 尝试使用git获取文件的首次提交日期
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
    except subprocess.TimeoutExpired:
        print(f"  警告: git命令超时")
    except Exception as e:
        # 忽略git错误，继续尝试文件系统时间
        pass

    # 如果git失败，使用文件系统修改时间（因为创建时间可能不准确）
    try:
        stat = os.stat(file_path)
        # 使用修改时间作为近似值
        mtime = stat.st_mtime
        mtime_datetime = datetime.fromtimestamp(mtime)
        return mtime_datetime.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"  警告: 无法获取文件时间: {e}")
        return None


def normalize_date(date_str):
    """规范化日期格式，将2025-7-28转换为2025-07-28"""
    if not date_str:
        return None

    # 移除引号
    date_str = date_str.strip('"').strip("'")

    # 检查是否是有效日期
    if date_str.lower() in ['invalid date', 'null', 'none', '']:
        return None

    # 尝试解析日期
    try:
        # 处理各种日期格式
        date_formats = ['%Y-%m-%d', '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        # 如果上面的格式都不匹配，尝试更灵活的解析
        # 匹配类似 "2025-7-28" 的格式
        match = re.match(r'(\d{4})[-./](\d{1,2})[-./](\d{1,2})', date_str)
        if match:
            year = match.group(1)
            month = match.group(2).zfill(2)
            day = match.group(3).zfill(2)
            return f"{year}-{month}-{day}"

        return None
    except Exception:
        return None


def extract_date_fields(frontmatter_content):
    """从frontmatter中提取所有date字段及其值"""
    date_fields = []
    lines = frontmatter_content.split('\n')

    for i, line in enumerate(lines):
        # 匹配date字段（忽略大小写）
        match = re.match(r'^\s*(date|dae):\s*(.+)$', line, re.IGNORECASE)
        if match:
            field_name = match.group(1).lower()  # 统一为小写
            date_value = match.group(2).strip()
            normalized_date = normalize_date(date_value)

            if normalized_date:
                date_fields.append({
                    'line_index': i,
                    'line': line,
                    'field_name': field_name,
                    'original_value': date_value,
                    'normalized_value': normalized_date,
                    'is_valid': True
                })
            else:
                date_fields.append({
                    'line_index': i,
                    'line': line,
                    'field_name': field_name,
                    'original_value': date_value,
                    'normalized_value': None,
                    'is_valid': False
                })

    return date_fields


def get_oldest_date(date_fields):
    """从date字段列表中找到最老的日期"""
    valid_dates = []

    for field in date_fields:
        if field['is_valid'] and field['normalized_value']:
            try:
                dt = datetime.strptime(field['normalized_value'], '%Y-%m-%d')
                valid_dates.append((dt, field['normalized_value']))
            except ValueError:
                continue

    if not valid_dates:
        return None

    # 返回最老的日期
    oldest_dt, oldest_date_str = min(valid_dates, key=lambda x: x[0])
    return oldest_date_str


def fix_date_fields(file_path):
    """修复单个文件的date字段"""

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否有frontmatter
    if not content.startswith('---'):
        print(f"跳过 {file_path}: 没有frontmatter")
        return False

    # 查找frontmatter的结束位置
    first_end = content.find('---', 3)
    if first_end == -1:
        print(f"跳过 {file_path}: frontmatter格式不正确")
        return False

    frontmatter_content = content[3:first_end]
    rest_content = content[first_end:]

    # 提取所有date字段
    date_fields = extract_date_fields(frontmatter_content)

    # 获取文件的真实创建日期（优先使用git历史）
    git_creation_date = get_file_creation_date(file_path)

    # 确定要使用的日期
    target_date = None

    # 优先使用git历史时间
    if git_creation_date:
        target_date = git_creation_date
        print(f"  使用git历史时间: {git_creation_date}")
    elif date_fields:
        # 如果没有git历史，使用最老的date字段
        oldest_date = get_oldest_date(date_fields)
        if oldest_date:
            target_date = oldest_date
            print(f"  使用最老的date字段: {oldest_date}")
    else:
        print(f"  错误: 无法确定日期")
        return False

    if not target_date:
        print(f"  错误: 无法确定日期")
        return False

    # 重建frontmatter
    lines = frontmatter_content.split('\n')
    new_lines = []

    # 标记是否已经添加了date字段
    date_added = False

    for i, line in enumerate(lines):
        # 检查是否是date或dae字段
        if re.match(r'^\s*(date|dae):', line, re.IGNORECASE):
            if not date_added:
                # 添加正确的date字段
                new_lines.append(f'date: {target_date}')
                date_added = True
            # 跳过其他date/dae字段
            continue

        new_lines.append(line)

    # 如果没有找到title字段，在开头添加date字段
    if not date_added:
        # 查找title字段的位置
        title_found = False
        for i, line in enumerate(new_lines):
            if re.match(r'^\s*title:\s*', line):
                # 在title后添加date字段
                new_lines.insert(i + 1, f'date: {target_date}')
                date_added = True
                title_found = True
                break

        # 如果没有title字段，在开头添加date字段
        if not title_found:
            new_lines.insert(0, f'date: {target_date}')
            date_added = True

    # 重建内容
    new_frontmatter = '\n'.join(new_lines)
    new_content = '---' + new_frontmatter + rest_content

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ 已修复date字段: {file_path}")
    print(f"  - date: {target_date}")

    return True


def main():
    """主函数：遍历docs目录下的所有markdown文件"""

    docs_dir = Path(__file__).parent / 'docs'

    if not docs_dir.exists():
        print(f"错误: 目录 {docs_dir} 不存在")
        return

    # 查找所有markdown文件（排除特定目录）
    exclude_dirs = {'node_modules', '.vuepress', '.obsidian', '.git', 'snippets'}
    md_files = []

    for md_file in docs_dir.rglob('*.md'):
        # 检查路径中是否包含排除的目录
        if not any(exclude_dir in md_file.parts for exclude_dir in exclude_dirs):
            md_files.append(md_file)

    print(f"找到 {len(md_files)} 个markdown文件\n")
    print("="*80)

    success_count = 0
    skip_count = 0
    error_count = 0

    for md_file in sorted(md_files):
        try:
            print(f"\n处理: {md_file.relative_to(docs_dir)}")
            if fix_date_fields(str(md_file)):
                success_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"✗ 处理失败 {md_file}: {e}")
            error_count += 1

    print(f"\n{'='*80}")
    print(f"处理完成!")
    print(f"成功修复date字段: {success_count} 个文件")
    print(f"跳过: {skip_count} 个文件")
    print(f"处理失败: {error_count} 个文件")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()