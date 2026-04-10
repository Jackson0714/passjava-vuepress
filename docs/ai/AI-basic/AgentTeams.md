---
title: Agent Teams
date: 2026-04-10
---

Agent Teams是Claude Code的实验性功能，通过允许多个Claude Code实例作为团队协作来解决复杂问题，Teammates可以互相通信、共享发现、挑战彼此的结论，而非仅向主对话汇报。它支持竞争假设、分层评审、模块化开发和规划-审批等协作模式，适用于需要多视角、高协作度的任务。

### Agent Teams概述

#### 核心概念与启用

- Agent Teams是Claude Code的实验性功能，默认关闭 [citation-1]。
- 启用需在设置文件或shell环境中配置`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`环境变量 [citation-1, citation-10]。
- Agent Teams模式与主会话-子代理模式的关键区别在于Teammates可以互相通信、共享发现和挑战结论 [citation-4]。

#### 核心组件

- 一个Agent Team由Team Lead（团队领导）、Teammates（队友）、共享任务列表和消息系统组成 [citation-8, citation-19]。
- 团队配置和任务数据存储在本地文件，Teammates可读取配置以发现其他成员 [citation-14]。

### Agent Teams与Sub-Agents对比

#### 模式差异

- Sub-Agents模式是主对话委托任务给子代理，子代理只向主对话汇报 [citation-2]。
- Agent Teams模式中，Teammates可以互相发消息、共享发现、挑战彼此的结论 [citation-4]。

#### 选型决策

- 若任务需要多个workers且workers之间需互相通信，选择Agent Teams [citation-17]。
- 若workers不需互相通信，选择Sub-Agents，其成本更低，协调更简单 [citation-17]。

#### 成本考量

- Agent Teams的token消耗显著高于单会话或子代理，因每个Teammate是独立的Claude实例 [citation-18]。
- 适用于并行探索能带来价值、讨论能提高质量、任务复杂度值得额外成本的场景 [citation-18]。

### Agent Teams协作设计模式

#### 竞争假设

- 适用于根因不明确，需多方向验证的场景，避免单个Agent的“锚定效应” [citation-19, citation-20]。
- Teammates各自持有不同假设并互相挑战，最终“存活”的假设更可能是真正的根因 [citation-20]。

#### 分层评审

- 适用于代码审查、PR Review等需多维度评估的任务 [citation-21]。
- 多个Teammates各自负责不同审查维度，并行工作，确保各维度得到充分关注 [citation-21, citation-22]。

#### 模块化开发

- 适用于涉及多个独立模块（前端、后端、数据库）的新功能开发 [citation-23]。
- 每个Teammate拥有一个模块，通过共享任务列表协调工作，关键机制是任务依赖和文件所有权 [citation-23, citation-24]。

#### 规划-审批

- 适用于复杂或高风险任务，需在实施前确认方案，避免因方向错误导致返工 [citation-25]。
- Teammate需先提交计划，Lead根据预设标准审批通过后方可执行 [citation-25, citation-26]。

### 实战项目：全栈Bug猎人

#### 项目场景

- 一个Express.js电商应用中植入多个相互关联的bug，导致会话丢失、API变慢、数据泄漏等症状 [citation-15]。
- Agent Teams通过“Session侦探”、“数据库侦探”、“缓存侦探”和“架构侦探”协作，发现级联故障链 [citation-16]。

#### 协作过程

- Teammates各自调查，分享发现，互相挑战，最终综合所有发现生成调查报告 [citation-16]。
- Agent Teams的优势在于跨视角发现bug关联，通过辩论机制产出更完整的根因链 [citation-15]。

## Sub-Agents 和 Agent Teams 两种模式的差异

![](http://cdn.passjava.cn/uPic/image-20260410140008643O7iZIQ.png)
