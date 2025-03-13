---
Title: AI 基础知识
date: 2025-03-13
---

资料来源极客时间。

## Function Calling

1. 大模型在日常生活中的影响：大模型改变了人们的提问方式，技术对日常生活产生深远影响，从以前的“有问题，Google一下”到现在的“先问问大模型”。 
2. 大模型的局限性：大模型并非万能，有时会给出错误答案，可能源于训练数据的有限性和模型无法处理特定领域或实时性问题。 
3.  Function Calling 机制：OpenAI 公司发明了 Function Calling 机制，使大模型能够根据需要自行选择合适的工具，从而解决问题。
4.   Chat Completions：OpenAI SDK 提供了一次性对话的方法，通过 Chat Completions 可以完成和大模型的对话，包括系统角色、人类角色和AI角色，以实现多轮对话效果。
5.   模型环境变量配置：在使用OpenAI SDK初始化大模型客户端时，需要填充token和baseurl两项，用于客户端与大模型服务器的连接。 
6. 通义千问大模型开通：阿里云通义千问提供了丰富的大模型产品供用户使用，且其请求方式兼容OpenAI SDK。
7.  Function Calling规范：包含了工具类型Type和工具定义Function两个部分，工具类型是写死的 "function"，工具定义包含名称、描述和参数三个部分。 
8. 工具的使用：定义了一个加法工具，给出了工具的作用、例子和参数，以便大模型理解和使用。
9.  工具调用机制：大模型只能选择使用工具，而不能调用工具，真正调用工具的仍然是人类。 
10. 大模型与工具交互：人类可以调用工具，并将结果反馈给大模型，从而辅助大模型完成任务。



我们可以初步理解所谓大模型“调用”工具的机制。其实就是将工具用文字描述清楚，并和问题一起发送给大模型，由大模型判断选择哪个工具能解决问题。因此其实 Function Calling 这个表述我个人感觉并不准确，或许叫 Function Selecting 会更加没有歧义。

## Agent

在论文《The Rise and Potential of Large Language Model Based Agents: A Survey》中，有一幅非常经典的图片为我们展示了 Agent 在处理问题时的思考过程。可以看到，图片中将 Agent 拆分成了感知（Perception）、大脑（Brain）以及行动（Action）三部分。

![img](http://cdn.jayh.club/uPic/5e8b8393926006193c04aeaefe5a8e20dMYkrY.png)

![img](http://cdn.jayh.club/uPic/6e87f9684c0c879f0ffe005152562259aH7Dso.png)

1. AI Agent是一个计算实体，可以通过传感器感知环境，自主作出决策，并通过执行器采取行动。 2. AI Agent的需求源于大模型的局限性，包括产生“幻觉”、缺乏垂直领域数据的训练、对实时了解有限或一无所知以及对复杂的数学计算无法完成等问题。 3. AI Agent的实现包括感知、大脑和行动三部分，其中大脑的工作包括自然语言的处理、存储和决策。


