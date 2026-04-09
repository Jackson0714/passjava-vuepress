#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 docs 目录下所有 markdown 文件的 frontmatter 添加缺失的 date 字段
- 如果 date 字段不存在或为空，则使用文件的创建日期
- date 字段值不加双引号（纯日期格式）
- 保持幂等性：已有有效 date 字段的文件不会被修改
- 排除 snippets、node_modules、.vuepress、.obsidian、.git 目录
"""

import os
import re
from pathlib import Path
from datetime import datetime


def get_file_creation_date(file_path):
    """获取文件的创建日期（macOS）或最早的状态改变时间（Linux）"""
    stat = os.stat(file_path)
    
    # macOS 使用 st_birthtime 获取创建时间
    if hasattr(stat, 'st_birthtime'):
        creation_time = stat.st_birthtime
    else:
        # Linux 系统使用 st_ctime（状态改变时间，最接近的替代）
        creation_time = stat.st_ctime
    
    # 转换为 datetime 对象并格式化为 YYYY-MM-DD
    creation_datetime = datetime.fromtimestamp(creation_time)
    return creation_datetime.strftime('%Y-%m-%d')


def has_valid_date_field(frontmatter_content):
    """检查 frontmatter 中是否有有效的 date 字段"""
    # 匹配 date 字段（允许前面有空格）
    pattern = r'^date:\s*(.+)$'
    date_match = re.search(pattern, frontmatter_content, re.MULTILINE | re.IGNORECASE)

    if not date_match:
        return False

    date_value = date_match.group(1).strip()

    # 移除可能的引号
    date_value = date_value.strip('"').strip("'")

    # 检查字段值是否为空或无效
    if not date_value or date_value in ['', 'null', 'None']:
        return False

    # 检查日期格式是否有效（YYYY-MM-DD）
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, date_value):
        return False

    return True


def remove_invalid_date_fields(frontmatter_content):
    """移除无效的 date 字段（空值或无效格式）"""
    lines = frontmatter_content.split('\n')
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        # 检查是否是 date 字段
        if re.match(r'^\s*date:\s*', line, re.IGNORECASE):
            # 提取 date 值
            match = re.match(r'^\s*date:\s*(.+)$', line, re.IGNORECASE)
            if match:
                date_value = match.group(1).strip()
                date_value = date_value.strip('"').strip("'")

                # 检查是否为空或无效
                if not date_value or date_value in ['', 'null', 'None']:
                    # 跳过这个无效的 date 字段
                    i += 1
                    continue

                # 检查日期格式是否有效
                date_pattern = r'^\d{4}-\d{2}-\d{2}$'
                if not re.match(date_pattern, date_value):
                    # 跳过这个无效的 date 字段
                    i += 1
                    continue

        new_lines.append(line)
        i += 1

    return '\n'.join(new_lines)

def add_date_to_frontmatter(file_path):
    """为单个 markdown 文件添加缺失的 date 字段"""

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否有 frontmatter
    if not content.startswith('---'):
        print(f"跳过 {file_path}: 没有 frontmatter")
        return False

    # 查找 frontmatter 的结束位置
    first_end = content.find('---', 3)
    if first_end == -1:
        print(f"跳过 {file_path}: frontmatter 格式不正确")
        return False

    frontmatter_content = content[3:first_end]

    # 检查是否已有有效的 date 字段
    if has_valid_date_field(frontmatter_content):
        print(f"跳过 {file_path}: 已存在有效的 date 字段")
        return False

    # 获取文件创建日期
    creation_date = get_file_creation_date(file_path)

    # 移除无效的 date 字段
    frontmatter_content = remove_invalid_date_fields(frontmatter_content)

    # 查找 title 字段的位置
    title_pattern = r'^title:\s*(.+)$'
    title_match = re.search(title_pattern, frontmatter_content, re.MULTILINE)

    if title_match:
        # 在 title 字段后添加 date 字段
        title_line = title_match.group(0)
        title_end_pos = frontmatter_content.find(title_line) + len(title_line)

        # 在 title 行后添加 date 字段
        new_frontmatter = (
            frontmatter_content[:title_end_pos] +
            f'\ndate: {creation_date}' +
            frontmatter_content[title_end_pos:]
        )
    else:
        # 如果没有 title 字段，在 frontmatter 开头添加
        new_frontmatter = f'\ndate: {creation_date}' + frontmatter_content

    new_content = '---' + new_frontmatter + content[first_end:]

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ 已添加 date: {file_path}")
    print(f"  - date: {creation_date} (文件创建日期)")

    return True


def main():
    """主函数：遍历 docs 目录下的所有 markdown 文件"""

    # 使用测试目录或实际目录
    test_mode = False
    if test_mode:
        docs_dir = Path(__file__).parent / 'test_docs'
    else:
        docs_dir = Path(__file__).parent / 'docs'

    if not docs_dir.exists():
        print(f"错误: 目录 {docs_dir} 不存在")
        return

    # 查找所有 markdown 文件（排除特定目录）
    exclude_dirs = {'node_modules', '.vuepress', '.obsidian', '.git', 'snippets'}
    md_files = []

    for md_file in docs_dir.rglob('*.md'):
        # 检查路径中是否包含排除的目录
        if not any(exclude_dir in md_file.parts for exclude_dir in exclude_dirs):
            md_files.append(md_file)
    
    print(f"找到 {len(md_files)} 个 markdown 文件\n")
    print("="*80)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for md_file in sorted(md_files):
        try:
            if add_date_to_frontmatter(str(md_file)):
                success_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"✗ 处理失败 {md_file}: {e}")
            error_count += 1
    
    print(f"\n{'='*80}")
    print(f"处理完成!")
    print(f"成功添加 date: {success_count} 个文件")
    print(f"跳过（已有有效 date）: {skip_count} 个文件")
    print(f"处理失败: {error_count} 个文件")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
