---
doc_type: weread-highlights-reviews
bookId: "3300151914"
reviewCount: 0
noteCount: 3
author: 朱忠华
cover: https://cdn.weread.qq.com/weread/cover/19/cpplatform_pazk5jjlgrkr5cea7kewyr/t6_cpplatform_pazk5jjlgrkr5cea7kewyr1751968559.jpg
progress: 0%
readingTime: 0小时12分钟
readingDate: 2025-07-28
isbn: 9787121329913
lastReadDate: 2025-07-28
---

# 元数据

> [!abstract] RabbitMQ实战指南
>
> - ![ RabbitMQ实战指南|200](https://cdn.weread.qq.com/weread/cover/19/cpplatform_pazk5jjlgrkr5cea7kewyr/t6_cpplatform_pazk5jjlgrkr5cea7kewyr1751968559.jpg)
> - 书名： RabbitMQ实战指南
> - 作者： 朱忠华
> - 简介： 本书从消息中间件的概念和RabbitMQ的历史切入，主要阐述RabbitMQ的安装、使用、配置、管理、运维、原理、扩展等方面的细节。本书大致可以分为基础篇、进阶篇和高阶篇三个部分。基础篇首先介绍RabbitMQ的基本安装及使用方式，方便零基础的读者以最舒适的方式融入到RabbitMQ之中。其次介绍RabbitMQ的基本概念，包括生产者、消费者、交换器、队列、绑定等。之后通过Java语言讲述了客户端如何与RabbitMQ建立（关闭）连接、声明（删除）交换器、队列、绑定关系，以及如何发送和消费消息等。进阶篇讲述RabbitMQ的 TTL、死信、延迟队列、优先级队列、RPC、消息持久化、生产端和消费端的消息确认机制等内容，以期读者能够掌握RabbitMQ的使用精髓。本书中间篇幅主要从RabbitMQ 的管理、配置、运维这三个角度来为读者提供帮助文档及解决问题的思路。高阶篇主要阐述RabbitMQ的存储机制、流控及镜像队列的原理，深入地讲述RabbitMQ的一些实现细节，便于读者加深对RabbitMQ的理解。本书还涉及网络分区的概念，此内容可称为魔鬼篇，需要掌握前面的所有内容才可理解其中的门道。本书最后讲述的是RabbitMQ的一些扩展内容及附录，供读者参考之用。
> - 出版时间： 2017-11-01 00:00:00
> - ISBN： 9787121329913
> - 分类： 计算机-计算机综合
> - 出版社： 电子工业出版社
> - PC地址：https://weread.qq.com/web/reader/81b32a60813aba1d7g014fa9

# 高亮划线

### 4.9 消费端要点介绍

> 📌 RabbitMQ队列拥有多个消费者时，队列收到的消息将以轮询(round-robin)的分发方式发送给消费者。每条消息只会发送给订阅列表里的一个消费者。这种方式非常适合扩展，而且它是专门为并发程序设计的。如果现在负载加重，那么只需要创建更多的消费者来消费处理消息即可。
> ⏱ 2025-07-28 14:57:01 ^3300151914-31-894-1028

> 📌 考虑一种情形，如果消息设置了优先级，那么消费者消费到的消息也必然不是顺序性的。
> ⏱ 2025-07-28 14:50:49 ^3300151914-31-4839-4878

### 4.10 消息传输保障

> 📌 消息可靠传输一般是业务系统接入消息中间件时首要考虑的问题，一般消息中间件的消息传输保障分为三个层级。
> At most once：最多一次。消息可能会丢失，但绝不会重复传输。
> At least once：最少一次。消息绝不会丢失，但可能会重复传输。
> Exactly once：恰好一次。每条消息肯定会被传输一次且仅传输一次。
> RabbitMQ支持其中的“最多一次”和“最少一次”。
> ⏱ 2025-07-28 14:51:28 ^3300151914-32-455-756

# 读书笔记

# 本书评论
