---
title: A2A 基础
date: 2025-05-19
---

## 参考链接

加餐｜前沿速递：如何学习与理解Google智能体协议A2A？

https://time.geekbang.com/column/article/870723

## A2A 原理

### MCP

![mcp](http://cdn.jayh.club/uPic/daa68f3cae4628966f0eb0b2c514e7e0vDy5eP.jpg)

### A2A

![img](http://cdn.jayh.club/uPic/d76754941f1353003fa166013f3b0af8n0k8mP.jpg)

![](http://cdn.jayh.club/uPic/1528c3a411598210ccc7a6b31c2e2b1bALAo0D.png)

![](http://cdn.jayh.club/uPic/387f9d49b956871991d79d76ee6d4623Aa86Ii.jpg)

## 总结

```SH
1. A2A协议是一个C-S架构的HTTP协议，通过在Agent端使用HTTP Server封装，然后在请求端通过规定的协议进行HTTP Client请求来实现Agent之间的通信。

2. 学习A2A协议时，重点在于掌握协议调用的套路，而不是深究底层原理和源码实现，因为协议是不断变化的，新的协议出现后旧的协议可能会被废弃。

3. A2A协议的学习重点包括Agent Card和Task的概念，以及如何邀请甲方等动作的接口，需要直接看源码并上手写Demo进行测试来加深理解。

4. A2A协议与MCP是不同层面的协议，解决的问题也不同，可以互补。MCP解决的是如何标准化封装与发布工具的问题，而A2A解决的是Agent间互相通信，形成多Agent的问题，比MCP的维度更高。

5. A2A协议的实现需要关注Agent Card的描述和能力，以及如何在客户端调用Server端Agent的过程，需要在Linux上运行并注意A2A的SDK、目录结构和Agent的实现逻辑。

6. A2A协议的实现涉及A2A Server和A2A Client端的代码，其中A2A Server端的实现需要根据Agent的实际情况进行描述，而A2A Client端的代码相对简单，主要是获取Agent的名片并发送消息给服务端Agent。

7. A2A协议的出现可能导致后续基础通用的Agent和工具变得不那么值钱，因为开源的会越来越多，社区中已经有很多通用Agent可供使用。

8. A2A协议的实现需要实际编写代码体验，通过查阅文档、分析源码并自己写代码实现，来加深对A2A协议的理解。

9. A2A协议的实现需要注意Agent的能力描述和工具描述，以及如何组织请求服务端Agent的数据格式，通过向服务端发送消息并接收返回来验证A2A协议的使用。

10. A2A协议的学习重点在于掌握协议调用的套路，而不是深究底层原理和源码实现，因为协议是不断变化的，新的协议出现后旧的协议可能会被废弃。
```
