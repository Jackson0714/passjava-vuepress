# 🤖 自定义 Agents 存放位置

## 📂 推荐目录结构

```
00.PassJava-VuePress/
├── agents/                          # Agent 配置和定义目录
│   ├── configs/                     # JSON 配置文件（现有）
│   │   └── file_analyzer.agent.json
│   ├── definitions/                 # ⭐ MD 格式的 Agent 定义（新增）
│   │   └── your-custom-agent.md
│   └── scripts/                     # Agent 执行脚本（可选）
│       └── your-custom-agent.py
├── agent_orchestrator.py            # Agent 编排器
└── file_analyzer.py                 # 示例 Agent
```

## 📝 如何创建自定义 Agent（MD 格式）

### 方式一：使用 Markdown 文件（推荐）

**文件位置**: `agents/definitions/your-agent-name.md`

**示例内容**:

````markdown
---
agent_name: "我的自定义 Agent"
agent_type: "custom_agent"
version: "1.0.0"
enabled: true
---

# Agent 描述

用于...的自定义 Agent

## 能力

- 能力 1
- 能力 2

## 触发关键词

- 关键词 1
- 关键词 2

## 执行方式

```bash
python3 agents/scripts/your-script.py [参数]
```
````

## 示例

用户：分析 XXX
Agent：执行操作...

```

### 方式二：使用 JSON 配置（现有）

**文件位置**: `agents/configs/your-agent-name.agent.json`

## 🚀 快速开始

1. **创建 MD 文件**: 在 `agents/definitions/` 目录下创建 `.md` 文件
2. **定义 Agent**: 按照上述格式编写 Agent 定义
3. **自动发现**: Agent 编排器会自动扫描并加载这些定义

## 📋 可用的 Agents

- ✅ [file_analyzer](file:///Users/wukong/01.PassJava/00.PassJava-VuePress/file_analyzer.py) - 文件分析助手（已实现）
- 🆕 您的自定义 Agent（待添加）
```
