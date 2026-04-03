#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件分析助手 - File Analysis Agent
用于分析本地文件的大小和基础信息
可被 AI 助手自动调用的 Agent 系统
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime


class FileAnalyzer:
    """文件分析器类"""
    
    def __init__(self, file_path):
        """
        初始化文件分析器
        
        Args:
            file_path (str): 要分析的文件路径
        """
        self.file_path = Path(file_path)
        
    def check_file_exists(self):
        """检查文件是否存在"""
        return self.file_path.exists()
    
    def get_file_size(self):
        """
        获取文件大小
        
        Returns:
            dict: 包含不同单位的文件大小信息
        """
        if not self.check_file_exists():
            return None
            
        size_bytes = self.file_path.stat().st_size
        
        # 转换为不同单位
        size_kb = size_bytes / 1024
        size_mb = size_kb / 1024
        size_gb = size_mb / 1024
        
        return {
            'bytes': size_bytes,
            'KB': round(size_kb, 2),
            'MB': round(size_mb, 2),
            'GB': round(size_gb, 2)
        }
    
    def get_line_count(self):
        """
        获取文件行数（仅适用于文本文件）
        
        Returns:
            int: 文件行数，如果读取失败则返回 None
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return sum(1 for _ in f)
        except Exception as e:
            return None
    
    def get_file_info(self):
        """
        获取文件的完整信息
        
        Returns:
            dict: 包含文件的所有基础信息
        """
        if not self.check_file_exists():
            return {'error': f'文件不存在：{self.file_path}'}
        
        stat_info = self.file_path.stat()
        
        return {
            'file_path': str(self.file_path.absolute()),
            'file_name': self.file_path.name,
            'extension': self.file_path.suffix,
            'size': self.get_file_size(),
            'is_file': self.file_path.is_file(),
            'is_directory': self.file_path.is_dir(),
            'created_time': datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified_time': datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'accessed_time': datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'line_count': self.get_line_count()
        }
    
    def analyze(self, output_format='json'):
        """
        分析文件并返回结果
        
        Args:
            output_format (str): 输出格式，支持 'json' 或 'text'
            
        Returns:
            str/dict: 分析结果
        """
        info = self.get_file_info()
        
        if 'error' in info:
            return info
        
        if output_format == 'json':
            return info
        else:
            return self._format_text(info)
    
    def _format_text(self, info):
        """格式化为文本输出"""
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("📄 文件分析报告")
        lines.append("=" * 60)
        
        for key, value in info.items():
            if key == 'size':
                lines.append(f"文件大小:")
                lines.append(f"  • {value['bytes']:,.0f} 字节")
                lines.append(f"  • {value['KB']:,.2f} KB")
                lines.append(f"  • {value['MB']:,.2f} MB")
                lines.append(f"  • {value['GB']:,.6f} GB")
            elif value is not None:
                lines.append(f"{key}: {value}")
            else:
                lines.append(f"{key}: 无法读取（可能是二进制文件）")
        
        lines.append("=" * 60 + "\n")
        return "\n".join(lines)


def analyze_file(file_path, output_format='json'):
    """
    分析文件的便捷函数
    
    Args:
        file_path (str): 文件路径
        output_format (str): 输出格式 ('json' 或 'text')
        
    Returns:
        dict/str: 分析结果
    """
    analyzer = FileAnalyzer(file_path)
    return analyzer.analyze(output_format)


def main():
    """主函数 - 命令行模式"""
    if len(sys.argv) < 2:
        print("使用方法：python file_analyzer.py <文件路径> [输出格式]")
        print("示例：python file_analyzer.py ./README.md json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'text'
    
    analyzer = FileAnalyzer(file_path)
    result = analyzer.analyze(output_format)
    
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)


if __name__ == "__main__":
    main()
