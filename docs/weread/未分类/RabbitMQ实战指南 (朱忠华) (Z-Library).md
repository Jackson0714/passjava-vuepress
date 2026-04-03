---
doc_type: weread-highlights-reviews
bookId: CB_ESv0LZ0NgCeU6vO6svBeU3Ut
reviewCount: 2
noteCount: 9
author: 朱忠华
cover: https://res.weread.qq.com/wrepub/CB_Cvy9fe9gIA2r6iP6gZFOR8ih_parsecover
progress: 46%
readingTime: 1小时34分钟
readingDate: 1970-01-01
isbn:
lastReadDate: 2025-04-21
---

# 元数据

> [!abstract] RabbitMQ实战指南 (朱忠华) (Z-Library)
>
> - ![ RabbitMQ实战指南 (朱忠华) (Z-Library)|200](https://res.weread.qq.com/wrepub/CB_Cvy9fe9gIA2r6iP6gZFOR8ih_parsecover)
> - 书名： RabbitMQ实战指南 (朱忠华) (Z-Library)
> - 作者： 朱忠华
> - 简介：
> - 出版时间：
> - ISBN：
> - 分类：
> - 出版社： 电子工业出版社
> - PC地址：https://weread.qq.com/web/reader/f74423f3643425f455376304c5a304e6743655536764f36737642655533557419e

# 高亮划线

## 第7章 RabbitMQ运维

> 📌 RabbitMQ集群对延迟非常敏感，应当只在本地局域网内使用。在广域网中不应该使用集群，而应该使用Federation或者Shovel来代替。
> ⏱ 2025-04-16 09:25:14 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-2640-2711

> 📌 如果关闭了集群中的所有节点，则需要确保在启动的时候最后关闭的那个节点是第一个启动的。如果第一个启动的不是最后关闭的节点，那么这个节点会等待最后关闭的节点启动。这个等待时间是30秒，如果没有等到，那么这个先启动的节点也会失败。在最新的版本中会有重试机制，默认重试10次30秒以等待最后关闭的节点启动
> ⏱ 2025-04-16 09:32:07 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-6278-6426

> 📌 在重试失败之后，当前节点也会因失败而关闭自身的应用。
> ⏱ 2025-04-16 09:32:15 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-6671-6697

> 📌 鲁棒性 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-23856-23859

- 💭 在分布式系统中，​​鲁棒性（Robustness）​​指系统在异常或故障情况下仍能维持正常运行或快速恢复的能力。 - ⏱ 2025-04-16 14:14:49

> 📌 注意，如果新集群有数据与metadata.json中的数据相冲突，对于交换器、队列及绑定关系这类非可变对象而言会报错，而对于其他可变对象如Parameter、用户等则会被覆盖，没有发生冲突的则不受影响。如果过程中发生错误，则导入过程终止，导致metadata.json中只有部分数据加载成功。
> ⏱ 2025-04-16 14:56:41 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-26896-27042

> 📌 我们可以采取一个通用的备份任务，在元数据有变更或者达到某个存储周期时将最新的metadata.json备份至另一处安全的地方。这样在遇到需要集群迁移时，可以获取到最新的元数据。
> ⏱ 2025-04-21 09:22:17 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-27160-27248

> 📌 第二个问题是，如果新旧集群的 RabbitMQ 版本不一致时会出现异常情况，比如新建立了一个 3.6.10 版本的集群，旧集群版本为 3.5.7，这两个版本的元数据就不相同。
> ⏱ 2025-04-21 09:36:53 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-27537-27624

> 📌 以将 3.6.10 的元数据从 queues 这一项前面的内容，包括rabbit_version、users、vhosts、permissions、parameters、global_parameters和policies这几项内容复制后替换3.5.7版本中的queues这一项前面的所有内容，然后再保存。之后将修改并保存过后的3.5.7版本的元数据JSON文件上传到新集群3.6.10版本的Web管理界面中，至此就完成了集群的元数据重建
> ⏱ 2025-04-21 09:37:28 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-28664-28884

> 📌 第三个问题就是如果采用上面的方法将元数据在新集群上重建，则所有的队列都只会落到同一个集群节点上，而其他节点处于空置状态，这样所有的压力将会集中到这单台节点之上。
> ⏱ 2025-04-21 09:36:35 ^CB-ESv0LZ0NgCeU6vO6svBeU3Ut-10-28937-29017

# 读书笔记

## 第7章 RabbitMQ运维

### 划线评论

> 📌 鲁棒性 ^37992928-7ZrTWavN3

    - 💭 在分布式系统中，​​鲁棒性（Robustness）​​指系统在异常或故障情况下仍能维持正常运行或快速恢复的能力。
    - ⏱ 2025-04-16 14:14:43

### 划线评论

> 📌 当然对于日志的监控处理也可以采用第3方工具实现，如Logstash[2]等，有兴趣的读者可以进行拓展学习。 ^37992928-7ZrU12APB

    - 💭 交给 ELK 日志平台，强大
    - ⏱ 2025-04-16 14:15:55

# 本书评论
