---
doc_type: weread-highlights-reviews
bookId: "26793754"
reviewCount: 3
noteCount: 3
author: CloudMan
cover: https://wfqqreader-1252317822.image.myqcloud.com/cover/754/26793754/t7_26793754.jpg
readingStatus: 在读
progress: 11%
totalReadDay: 5
readingTime: 1小时4分钟
readingDate: 2022-05-28
isbn: 9787302496670
lastReadDate: 2023-05-18

---
# 元数据
> [!abstract] 每天5分钟玩转Kubernetes
> - ![ 每天5分钟玩转Kubernetes|200](https://wfqqreader-1252317822.image.myqcloud.com/cover/754/26793754/t7_26793754.jpg)
> - 书名： 每天5分钟玩转Kubernetes
> - 作者： CloudMan
> - 简介： Kubernetes 是容器编排引擎的事实标准，是继大数据、云计算和 Docker 之后又一热门技术，而且未来相当一段时间内都会非常流行。对于IT行业来说，这是一项非常有价值的技术。对于IT从业者来说，掌握容器技术既是市场的需要，也是提升自我价值的重要途径。 《每天5分钟玩转Kubernetes》共15章，系统介绍了 Kubernetes 的架构、重要概念、安装部署方法、运行管理应用的技术、网络存储管理、集群监控和日志管理等重要内容。书中通过大量实操案例深入浅出地讲解 Kubernetes 核心技术，是一本从入门到进阶的实用Kubernetes 操作指导手册。读者在学习的过程中，可以跟着教程进行操作，在实践中掌握 Kubernetes 的核心技能。在之后的工作中，则可以将本教程作为参考书，按需查找相关知识点。 《每天5分钟玩转 Kubernetes》主要面向微服务软件开发人员，以及 IT 实施和运维工程师等相关人员，也适合作为高等院校和培训学校相关专业的教学参考书。
> - 出版时间： 2018-04-01 00:00:00
> - ISBN： 9787302496670
> - 分类： 计算机-计算机综合
> - 出版社： 清华大学出版社
> - PC地址：https://weread.qq.com/web/reader/4e7320a07198d71a4e7b700

# 高亮划线

### 1.3 部署应用

> 📌 这里Deployment是Kubernetes的术语，可以理解为应用。 ^26793754-10-1146-1181
- 💭 k8s deployment 代表应用 - ⏱ 2023-05-18 15:37:02 

> 📌 Pod是Kubernetes调度的最小单位，同一Pod中的容器始终被一起调度。
   
   运行kubectl get pods，查看当前的Pod，如图1-7所示。
   
   [插图]
   
   图1-7
   
   kubernetes-bootcamp-390780338-q9p1t就是应用的Pod。 
> ⏱ 2023-05-15 23:21:43 ^26793754-10-1293

> 📌 Pod是Kubernetes调度的最小单位，同一Pod中的容器始终被一起调度。 ^26793754-10-1394-1433
- 💭 K8s pod 概念
    - ⏱ 2023-05-18 15:28:08 

### 1.5 Scale应用

> 📌 [插图] 
> ⏱ 2022-05-31 06:26:55 ^26793754-12-1966-1967

# 读书笔记

## 1.3 部署应用

### 划线评论
> 📌 这里Deployment是Kubernetes的术语，可以理解为应用。  ^37992928-7IiJ1AjWF
    - 💭 k8s deployment 代表应用
    - ⏱ 2023-05-18 15:37:15

### 划线评论
> 📌 Pod是Kubernetes调度的最小单位，同一Pod中的容器始终被一起调度。  ^37992928-7IiIrSgSh
    - 💭 K8s pod 概念

    - ⏱ 2023-05-18 15:28:27
   
## 1.5 Scale应用

### 划线评论
> 📌 [插图]  ^37992928-7zEIp1zx6
    - 💭 一个命令就可以扩容了，确实很方便。有几个疑惑的点。
那么问题来了：
1.这几个节点是对等的，端口映射是自动的随机分配吗？
2.主从复制的实例是否能通过这种方式?应该不能吧，有些配置是针对不同的节点类型的。
3.是否能实现分片?比如启动了 3 个 ES 副本，怎么让它们组成集群模式且是分片的?
    - ⏱ 2022-05-31 06:32:19
   
# 本书评论

