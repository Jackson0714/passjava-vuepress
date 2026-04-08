---
title: Claude Code 接入 DeepSeek 完整指南
date: 2026-04-08
---

> 让 Claude Code 拥抱 DeepSeek 的强大能力，实现开发工作流的无缝切换

你好，我是悟空。

## 📝 前言

Claude Code 作为强大的 AI 编程助手，原本仅支持 Anthropic 的官方模型。但通过巧妙的配置，我们可以让它接入 DeepSeek，享受更灵活的模型选择和更具性价比的 API 服务。本文将带你一步步完成这个配置过程。

## 🚀 第一步：创建配置文件，指向 DeepSeek

在用户目录下的 `~./claude` 文件夹中，新建 `settings.json` 配置文件：

**MacOS 文件路径：**

```
~/.claude/settings.json`
```

> 💡 **小提示**：如果 `.claude` 文件夹不存在，请手动创建它。

### 基础配置（使用推理模型）

将以下 JSON 配置粘贴到文件中（**请务必将 `sk-XXX` 替换成你自己的 DeepSeek API Key**）：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的 api key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "deepseek-reasoner",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-reasoner",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-reasoner",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-reasoner",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-reasoner",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "32000"
  },
  "permissions": {
    "allow": [],
    "deny": []
  },
  "alwaysThinkingEnabled": false
}
```

### 📋 配置参数详解

| 参数                             | 说明              | 备注                                             |
| -------------------------------- | ----------------- | ------------------------------------------------ |
| `ANTHROPIC_AUTH_TOKEN`           | DeepSeek API 密钥 | 用于身份认证，请妥善保管                         |
| `ANTHROPIC_BASE_URL`             | API 接口地址      | **核心配置**！DeepSeek 提供的 Anthropic 兼容接口 |
| `ANTHROPIC_MODEL`                | 默认模型          | 指定使用的 DeepSeek 模型                         |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | 最复杂任务模型    | 适用于架构设计等高难度任务                       |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 日常编码模型      | 平衡性能与成本                                   |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | 简单任务模型      | 快速响应，成本更低                               |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | 子代理模型        | 自动化子任务使用的模型                           |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`  | 最大输出长度      | 可根据需求调整，最高支持 32K                     |

### 🎯 模型选择策略

- **`deepseek-reasoner`**：推理增强模型，适合复杂逻辑分析和架构设计
- **`deepseek-chat`**：标准对话模型，性价比高，适合日常编码

> 💡 **设计理念**：通过区分不同场景下的默认模型，可以在保证质量的同时优化成本。例如，日常编码使用经济型模型，只有复杂架构任务才启用推理模型。

### 🤔 为什么可以这样配置？

DeepSeek 提供了与 Anthropic API 格式完全兼容的接口。这意味着：

1. **协议兼容**：DeepSeek 的 API 响应格式与 Anthropic 一致
2. **无缝切换**：只需修改 `BASE_URL` 和认证 Token，无需修改任何代码
3. **功能完整**：支持流式输出、函数调用等核心特性

## ✨ 第二步：运行验证

完成配置后，重新启动 Claude Code，你会看到成功接入 DeepSeek 的提示：

![Claude Code 成功接入 DeepSeek 界面](http://cdn.passjava.cn/uPic/image-20260408155048073zLaCCzCtbWXr.png)

如图所示，Claude Code 已经成功连接到 DeepSeek 服务，可以开始使用了！

## 💰 第三步：优化配置，降低成本（可选）

如果你的使用场景主要是日常编码，建议将默认模型切换为 `deepseek-chat`，以获得更好的性价比：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "deepseek-chat",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-reasoner",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-chat",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-chat",
    "CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-chat",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "32000"
  },
  "permissions": {
    "allow": [],
    "deny": []
  },
  "alwaysThinkingEnabled": false
}
```

**混合策略优势**：

- 日常编码：使用 `deepseek-chat`，成本降低约 70%
- 复杂推理：自动切换为 `deepseek-reasoner`，保证质量
- 子代理任务：使用经济模型，优化整体开销

## 四、用 claude 验证子代理的权限边界

在 claude 中输入以下提示词：

> 让 code-reviewer 修复 auth.js 中的硬编码密钥问题

![image-20260408155645347](http://cdn.passjava.cn/uPic/image-20260408155645347D5Bo4h.png)

因为 code-reviewer 子代理没有 Edit/Write 权限，所以无法修改 auth.js 文件。

## ⚠️ 注意事项

### 1. 🔐 API Key 安全

- **切勿**将包含 API Key 的配置文件上传到公开仓库
- 建议将 `.claude` 文件夹添加到 `.gitignore`
- 定期更换 API Key，降低泄露风险

### 2. 🧠 模型选择

DeepSeek 提供多种模型，可根据场景灵活选择：

| 模型                | 特点       | 适用场景                     |
| ------------------- | ---------- | ---------------------------- |
| `deepseek-chat`     | 快速、经济 | 日常编码、问答、文档生成     |
| `deepseek-reasoner` | 推理能力强 | 算法设计、Bug 分析、架构决策 |

### 3. 💵 费用说明

- DeepSeek API 按使用量收费，具体价格请参考[官方定价](https://platform.deepseek.com/pricing)
- 建议设置预算告警，避免意外超支
- 可以通过配置中的 Token 限制控制单次请求成本

### 4. 🔧 故障排查

如果遇到连接问题，请检查：

- API Key 是否有效且余额充足
- 网络是否能正常访问 `api.deepseek.com`
- 配置文件 JSON 格式是否正确

## 📚 总结

通过以上配置，你就可以在 Claude Code 中享受 DeepSeek 带来的：

- ✅ 更灵活的模型选择
- ✅ 更具性价比的 API 服务
- ✅ 完全兼容的使用体验

现在，开始你的 DeepSeek + Claude Code 开发之旅吧！🚀

---
