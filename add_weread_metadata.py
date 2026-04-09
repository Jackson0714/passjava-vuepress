#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 weread 目录下的所有 markdown 文件添加 title 和 date 字段
- title: 使用文件名（不含扩展名）
- date: 从 readingDate 字段获取
"""

import os
import re
from pathlib import Path


def process_markdown_file(file_path):
    """处理单个 markdown 文件，添加 title 和 date 字段"""
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取文件名（不含扩展名）作为 title
    title = Path(file_path).stem
    # 移除双引号，避免与 frontmatter 的引号冲突
    title = title.replace('"', '')
    
    # 检查是否已经有 title 或 date 字段
    if re.search(r'^title:', content, re.MULTILINE):
        print(f"跳过 {file_path}: 已存在 title 字段")
        return False
    
    # 提取 readingDate
    reading_date_match = re.search(r'^readingDate:\s*(.+)$', content, re.MULTILINE)
    if not reading_date_match:
        print(f"跳过 {file_path}: 未找到 readingDate 字段")
        return False
    
    reading_date = reading_date_match.group(1).strip()
    
    # 在 frontmatter 开头添加 title 和 date
    # 查找 frontmatter 的开始位置 (---)
    frontmatter_start = content.find('---')
    if frontmatter_start == -1:
        print(f"跳过 {file_path}: 未找到 frontmatter")
        return False
    
    # 在 --- 之后插入 title 和 date
    insert_position = frontmatter_start + 3  # 跳过 ---
    
    # 构建要插入的内容
    new_fields = f"\ntitle: \"{title}\"\ndate: {reading_date}"
    print(f"构建要插入的内容 {title} {reading_date}: 未找到 frontmatter")
    
    # 插入新字段
    new_content = content[:insert_position] + new_fields + content[insert_position:]
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 处理成功: {file_path}")
    print(f"  - title: {title}")
    print(f"  - date: {reading_date}")
    return True


def main():
    """主函数：遍历 weread 目录下的所有 markdown 文件"""
    
    weread_dir = Path(__file__).parent / 'docs' / 'weread'
    
    if not weread_dir.exists():
        print(f"错误: 目录 {weread_dir} 不存在")
        return
    
    # 查找所有 markdown 文件
    md_files = list(weread_dir.rglob('*.md'))
    print(f"找到 {len(md_files)} 个 markdown 文件\n")
    
    success_count = 0
    skip_count = 0
    
    for md_file in sorted(md_files):
        try:
            if process_markdown_file(str(md_file)):
                success_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"✗ 处理失败 {md_file}: {e}")
            skip_count += 1
    
    print(f"\n{'='*60}")
    print(f"处理完成!")
    print(f"成功: {success_count} 个文件")
    print(f"跳过: {skip_count} 个文件")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
