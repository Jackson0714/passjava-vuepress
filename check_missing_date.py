#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计 docs 目录下所有缺少 date 字段或 date 字段为空的 markdown 文件
"""

import os
import re
from pathlib import Path


def has_valid_date_field(content):
    """检查文件内容中是否有有效的 date 字段"""
    
    # 查找 frontmatter
    if not content.startswith('---'):
        return None, "没有 frontmatter"
    
    # 找到第二个 --- 的位置（frontmatter 结束）
    first_end = content.find('---', 3)
    if first_end == -1:
        return None, "frontmatter 格式不正确"
    
    frontmatter_content = content[3:first_end]
    
    # 匹配 date 字段
    date_match = re.search(r'^date:\s*(.+)$', frontmatter_content, re.MULTILINE)
    
    if not date_match:
        return False, "date 字段不存在"
    
    date_value = date_match.group(1).strip()
    
    # 检查 date 值是否为空或无效
    if not date_value or date_value in ['', '""', "''", 'null', 'None']:
        return False, f"date 字段为空或无效: '{date_value}'"
    
    return True, f"date 字段有效: {date_value}"


def check_markdown_file(file_path):
    """检查单个 markdown 文件的 date 字段"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_date, message = has_valid_date_field(content)
        return has_date, message
    except Exception as e:
        return None, f"读取文件失败: {e}"


def main():
    """主函数：遍历 docs 目录下的所有 markdown 文件并统计"""
    
    docs_dir = Path(__file__).parent / 'docs'
    
    if not docs_dir.exists():
        print(f"错误: 目录 {docs_dir} 不存在")
        return
    
    # 查找所有 markdown 文件（排除 node_modules、.vuepress、snippets 等目录）
    exclude_dirs = {'node_modules', '.vuepress', '.obsidian', '.git', 'snippets'}
    md_files = []
    
    for md_file in docs_dir.rglob('*.md'):
        # 检查路径中是否包含排除的目录
        if not any(exclude_dir in md_file.parts for exclude_dir in exclude_dirs):
            md_files.append(md_file)
    
    print(f"扫描目录: {docs_dir}")
    print(f"找到 {len(md_files)} 个 markdown 文件\n")
    print("="*80)
    
    # 分类统计
    files_without_date = []  # 没有 date 字段
    files_with_empty_date = []  # date 字段为空
    files_with_valid_date = []  # date 字段有效
    files_error = []  # 处理出错的文件
    
    for md_file in sorted(md_files):
        has_date, message = check_markdown_file(str(md_file))
        
        relative_path = md_file.relative_to(docs_dir)
        
        if has_date is None:
            files_error.append((str(relative_path), message))
        elif has_date is False:
            if "不存在" in message:
                files_without_date.append(str(relative_path))
            else:
                files_with_empty_date.append((str(relative_path), message))
        else:
            files_with_valid_date.append(str(relative_path))
    
    # 输出统计结果
    print(f"\n📊 统计结果:")
    print(f"{'='*80}")
    print(f"✅ 有有效 date 字段的文件: {len(files_with_valid_date)} 个")
    print(f"❌ 缺少 date 字段的文件: {len(files_without_date)} 个")
    print(f"⚠️  date 字段为空的文件: {len(files_with_empty_date)} 个")
    print(f"💥 处理出错的文件: {len(files_error)} 个")
    print(f"{'='*80}\n")
    
    # 详细列出缺少 date 字段的文件
    if files_without_date:
        print(f"\n❌ 缺少 date 字段的文件列表 ({len(files_without_date)} 个):")
        print("-" * 80)
        for i, file_path in enumerate(files_without_date, 1):
            print(f"{i:3d}. {file_path}")
        print()
    
    # 详细列出 date 字段为空的件
    if files_with_empty_date:
        print(f"\n⚠️  date 字段为空的件列表 ({len(files_with_empty_date)} 个):")
        print("-" * 80)
        for i, (file_path, message) in enumerate(files_with_empty_date, 1):
            print(f"{i:3d}. {file_path}")
            print(f"     {message}")
        print()
    
    # 列出处理出错的文件
    if files_error:
        print(f"\n💥 处理出错的文件列表 ({len(files_error)} 个):")
        print("-" * 80)
        for i, (file_path, error) in enumerate(files_error, 1):
            print(f"{i:3d}. {file_path}")
            print(f"     {error}")
        print()
    
    # 总结
    total_issues = len(files_without_date) + len(files_with_empty_date)
    if total_issues > 0:
        print(f"\n{'='*80}")
        print(f"🔧 需要处理的文件总数: {total_issues} 个")
        print(f"提示: 可以运行 python3 add_date_to_frontmatter.py 自动添加 date 字段")
        print(f"{'='*80}")
    else:
        print(f"\n{'='*80}")
        print(f"✨ 所有文件都有有效的 date 字段！")
        print(f"{'='*80}")


if __name__ == '__main__':
    main()
