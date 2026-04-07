#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 add_weread_metadata.py 中的正则表达式逻辑
"""

import re

print("=" * 70)
print("测试新的正则表达式逻辑")
print("=" * 70)

test_cases = [
    ("date: 2024-01-15", True, "有值的 date"),
    ("date:", False, "空的 date（无空格）"),
    ("date: ", False, "空的 date（有空格）"),
    ("date:  ", False, "空的 date（多个空格）"),
    ("title: \"测试\"", True, "有值的 title"),
    ("title:", False, "空的 title"),
    ("title: ", False, "空的 title（有空格）"),
]

all_passed = True

for test_str, expected, description in test_cases:
    if test_str.startswith("date"):
        result = bool(re.search(r'^date:\s*\S', test_str, re.MULTILINE))
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result != expected:
            all_passed = False
        print(f"{status} | {description:25s} | '{test_str}' | 结果:{result}")
    
    elif test_str.startswith("title"):
        result = bool(re.search(r'^title:\s*\S', test_str, re.MULTILINE))
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result != expected:
            all_passed = False
        print(f"{status} | {description:25s} | '{test_str}' | 结果:{result}")

print("=" * 70)
if all_passed:
    print("✓ 所有测试通过！")
else:
    print("✗ 存在失败的测试")
print("=" * 70)
