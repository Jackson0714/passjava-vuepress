---
title: RocketMQ 架构简介
date: 2025-08-14
author: 悟空聊架构
---

大家好，我是悟空。

上一篇我讲解了RabbitMQ架构（可以通过文末的合集查看） ，这次我们继续讲解另外一款消息队列 RocketMQ 的架构。

RocketMQ 在功能、稳定性、性能层面都比 RabbitMQ 的表现更好。

## **1.2.5.1 RocketMQ系统架构简介**

RocketMQ 由 Broker、NamServer、Producer、Consumer 四大组件组成。如下图所示：

![图片](http://cdn.passjava.cn/uPic/640N5hJvN.jpg)

简单概括下四大组件的核心要点：

| 组件       | 技术要点                     |
| :--------- | :--------------------------- |
| NameServer | 轻量级注册中心               |
| Broker     | 消息存储                     |
| Producer   | 同步、异步、单向多种发射方式 |
| Consumer   | Push/Pull 双模式             |

**RocketMQ的NameServer 负责元数据的存储**。它一个独立的进程，扮演着集群“中枢神经系统”的角色，其核心作用是为生产者（Producer）和消费者（Consumer）提供路由信息，帮助它们找到对应的 Broker 地址。

**Broker 在启动的时候会主动连接 NameServer**，将自己的元数据信息上报给 NameServer，每隔30秒还会上报一次元数据（心跳包）。核心内容包含 Broker 的地址、名称、BrokerId、主节点地址、该 Broker 上的所有 Topic 的队列配置等。

**NameServer 会将 Broker 的元数据信息缓存到本地路由表**，供 Producer/Consumer 拉取，实现动态路由与故障感知。生产者在发送数据的时候，会指定Topic或MessageQueue，只指定 Topic 时，Producer用负载均衡算法挑一个 MessageQueue；也可以直接指定 MessageQueue。

Broker 收到消息后，**将消息顺序追加到 CommitLog 文件**，如果文件大小超过固定大小（默认1G），则会生成 CommitLog 文件，避免单个文件过大。MessageQueue 只是逻辑分片，不会存储消息。ConsumeQueue 做逻辑分片，是消息的索引，指向 CommitLog 中消息的具体位置。

Producer发送消息，启动时先跟NameServer集群中的其中一台建立长连接，**并从NameServer中获取当前发送的 Topic 存在哪些 Broker 上**，通过负载均衡从队列列表中选择一个MessageQueue，然后与MessageQueue所在的Broker建立长连接从而向Broker发消息。

**Consumer 跟 Producer类似，跟其中一台 NameServer 建立长连接**，获取当前订阅Topic存在哪些Broker上，然后直接跟Broker建立连接通道，开始消费消息。Consumer 通过声明的 Group进行分组拉取消息，消费者每拉一批消息，SDK 把最新 offset 写回 Broker（定时或手动 commit）。

## **1.2.5.2 RocketMQ的网络协议**

- RocketMQ 5.0 之前： 客户端与 Broker / NameServer 只支持 RocketMQ 私有 Remoting 协议（基于 Netty 的二进制协议，固定帧格式、序列化用 RocketMQ 自己的编码）。
- RocketMQ 5.0 开始： 官方 SDK 新增 gRPC 协议实现，同时保留旧的 Remoting 协议实现。

如下图所示：

![图片](http://cdn.passjava.cn/uPic/640-202508172150124959zUUNZ.jpg)

完整交互流程：

**（1）Broker与NameServer通信**：通过 Remoting 协议向 NameServer（9876 端口）注册和发送心跳。

**（2）客户端启动**：通过Remoting协议连接 NameServer（9876 端口）获取 Broker 路由表。

**（3）客户端与 Broker 通信**：使用 Remoting 协议连接 Broker（10911端口），或者直连Proxy的8081端口，将数据通过 gRPC 协议发送给 Proxy，最后还是通过 Remoting协议转发给 Broker。

值得注意的是Remoting 协议直接基于四层的 TCP 协议通信，gRPC 基于七层的 HTTP2 协议通信，不过 HTTP2 底层也是基于TCP。

**Remoting 协议 和 gRPC 协议对比**：

| 维度       | Remoting（私有协议） | gRPC（开发库丰富，推荐）  |
| :--------- | :------------------- | :------------------------ |
| 性能       | 极致（私有协议优化） | 稍低（HTTP/2 头部开销）   |
| 多语言支持 | 高成本（需重复实现） | 低成本（官方/社区实现）   |
| 云原生集成 | 困难（需额外适配）   | 原生支持（Istio/K8s）     |
| 可观测性   | 需额外开发           | 原生支持（OpenTelemetry） |
| 生态连接   | 封闭                 | 开放（Serivce Mesh等）    |

Remoting 适合 RocketMQ 内部高性能、低延迟的场景（如 Broker 间同步），而 gRPC 更适合面向用户和云原生的场景，两者不是替代关系，而是互补。

## **1.2.5.3 RocketMQ的网络模块**

RocketMQ 是基于 Netty 扩展出来的高性能网络通信框架，接下来我们来看看下面的原理图。

![图片](http://cdn.passjava.cn/uPic/640-202508172150125219mUL7T.jpg)

RocketMQ的RPC通信采用Netty作为底层通信库，并基于Reactor多线程模型进行了深度扩展和优化。

Broker 中有一个 **Reactor 主线程**（Netty BossGroup），Producer和Broker建立TCP长连接时，Reactor 主线程会在端口上监听到客户端建立的请求。然后处理TCP三次握手建立连接，创建并注册SocketChannel将SocketChannel注册到selector上。Producer和Broker里面都通过各自的SocketChannel维持长连接。Producer 通过 SocketChannel发送消息给Broker中的SocketChannel。

Broker 中还有一个 **Reactor线程池**（Netty WorkerGroup），里面的线程会监听到 SocketChannel 的网络数据，并将数据传递给 Woker线程池中的一个线程进行预处理。Reactor线程池默认有三个线程。

Worker 线程池中的线程的核心职责：SSL 加密验证、编解码工作、检查空闲连接、管理网络连接等等。Worker 线程池默认有8个线程。

另外 Broker 有一个业务线程池：**SendMessage线程池**，里面的线程专门用于处理 Woker消息写入到磁盘。该线程池的线程数是动态的，根据服务器的CPU核心数自动调整。这种设计使得RocketMQ能够高效处理大量并发请求，同时保持系统的稳定性和可扩展性。

## **1.2.5.4 RocketMQ的存储模块**

RocketMQ 的数据存储分为元数据存储和消息数据存储。

### **\*\*1.2.5.4.1 元数据存储\*\***

**什么是Broker 的元数据？**

首先元数据是用来描述其他数据的属性的。就像一本书的元数据是用来描述这本书的信息，如书名、作者、出版社、目录等。

那么Broker 的元数据其实就是描述 Broker 中的核心数据的，如 Broker的基础元数据： 名称、ID、集群名称、地址等，另外还有Topic的相关元数据。

如何存储这些Broker 中的这些重要的元数据呢？我们来看下原理图。

![图片](http://cdn.passjava.cn/uPic/640-20250817215012531vNy3PH.jpg)

首先每个Broker节点都会存储自己的元数据，然后他们会将自己的这些元数据上传到每个 NameServer上（如果NameServer 采用集群部署的方式，就会有多个NameServer，各NameServer实例之间不进行相互通讯）。如果Broker有从节点，也会和主节点一样上传元数据。所以每个 NameServer 上都会有所有Broker的元数据。即使某个NameServer宕机了，但其他NameServer有所有Broker元数据信息，整个集群还是能正常对外提供服务的。另外需要注意的是这些数据都是放在 NameServer的内存中，不会持久化存储。

**NameServer如何感知某个Broker宕机了？**

Broker会每隔30秒向所有NameServer发送心跳包，告诉每个NameServer自己还存活着。每个NameServer 在收到心跳包都会更新这个Broker节点的最近一次的心跳时间。NameServer还会每隔10秒运行一个任务，用来检查每个Broker节点最近一次的心跳时间是否超过120秒没有更新过，如果超过了，则说明这个Broker节点宕机了。

Broker主从节点的机制说明：

| 机制     | 说明                                                                            |
| :------- | :------------------------------------------------------------------------------ |
| 数据同步 | 主节点异步/同步复制消息到从节点                                                 |
| 故障接管 | 主节点宕机时，从节点不会自动升主 （需运维干预或依赖 RocketMQ Dledger 自动选主） |
| 读扩散   | 消费者默认从主节点读取，高负载时可配置从从节点读取数据，分担主节点压力。        |

### **\*\*1.2.5.4.2 消息数据存储\*\***

跟RocketMQ 存储相关的有三种文件：CommitLog、ConsumeQueue、IndexFile。如下图所示，CommitLog和Consume

![图片](http://cdn.passjava.cn/uPic/640-202508172150125421ELmkq.jpg)

**（1）CommitLog**：存储消息的主体内容，消息的内容不定长，单个文件默认1G大小。当文件写满后，写入下一个文件。每个 Broker 节点都有各自的 CommitLog 文件。

**（2）ConsumeQueue**：消息消费索引，用于提高消息消费的性能。因 RocketMQ基于主题的订阅模式，消息消息也是针对主题进行的，但是如果每次消费都要遍历 CommitLog文件来检索对应主题的消息是非常低效的，所以才有了基于主题的CommitLog 索引文件，也就是 ConsumeQueue 文件。它的文件夹的组织方式为topic/queue/file三层组织结构。每个文件采取定长设计，每一个条目共20个字节，分别为8字节的CommitLog物理偏移量、4字节的消息长度、8字节tag hashcode，单个文件由30W个条目组成，可以像数组一样随机访问每一个条目，每个ConsumeQueue文件大小约5.72M。

**（3）IndexFile**：索引文件，提供了一种可以通过key或时间区间来查询消息的方法。Index文件的存储位置是：$HOME/store/index/{fileName}，文件名fileName是以创建时的时间戳命名的，固定的单个IndexFile文件大小约为400M，一个IndexFile可以保存 2000W个索引。

### **\*\*1.2.5.4.3 消息的刷盘机制\*\***

(1) 同步刷盘：当Broker端收到消息后，只有将消息真正持久化至磁盘后，Broker端才会真正返回给Producer端一个成功的ACK响应。同步刷盘对MQ消息可靠性来说是一种不错的保障，但是性能上会有较大影响，一般适用于金融业务应用该模式较多。

(2) 异步刷盘：当Broker端收到消息后，只要消息写入PageCache即可将成功的ACK返回给Producer端。消息刷盘采用后台异步线程提交的方式进行，降低了读写延迟，提高了MQ的性能和吞吐量。

## **1.2.5.5 RocketMQ生产消费机制详解**

### **\*\*1.2.5.5.1 Producer生产消息\*\***

Producer启动时先跟NameServer集群中的其中一台建立长连接，当需要发送消息到Topic或MessageQueue时，会根据从NameServer中拿到的路由信息找到要发送给哪个Broker，然后通过负载均衡算法选择一个MessageQueue，然后与队列所在的Broker建立长连接，并将消息发送给该MessageQueue。

Producer支持三种发送消息的形式：

（1）单向发送（Oneway）：发送消息后立即返回，Producer不关心是否发送成功，也不会处理响应。

（2）同步发送（Sync）：发送消息后，Producer等待响应。

（3）异步发送（Async）：发送消息后立即返回，Producer会在自己提供的回调方法中处理响应。

### **\*\*1.2.5.5.2 Consumer 消费消息\*\***

Consumer跟Producer类似，也是和NameServer建立长连接，获取路由信息，然后通过 订阅的Topic找到对应了哪些Broker，然后直接跟Broker建立连接，开始消费消息，最后通过提交消费位点的形式来保存消费进度。

**Consumer 支持三种消费消息的模式**

**（1）拉取模式（Pull）**：消费者主动向Broker发送拉取请求，指定要拉取的消息数量和偏移量（或时间戳），Broker 响应包含消息或空结果。

**（2）推模式（Push）**：客户端与 Broker 建立长连接，**并发送拉取消息的请求**。如果当前没有新消息，Broker 不会立即响应，而是等待一段时间或直到有新消息到达再返回。

**（3）无状态模式（Pop）**：在 RocketMQ 5.0 中，Pop 消费模式的设计核心在于将重平衡、位点管理及消息重试等任务转移至服务端处理，有效避免单点故障引起的消息积压，优化了整体消息处理效率和系统的水平扩展能力，且提升了系统的灵活性和扩展性。

消费者组概念

在消费者中消费组的有非常重要的作用，如果多个消费者设置了相同的Consumer Group，我们认为这些消费者在同一个消费组内。

**Apache RocketMQ 支持两种消费模式**

**（1）集群消费模式**：当使用集群消费模式时，RocketMQ 认为任意一条消息只需要被消费组内的任意一个消费者处理即可。可以通过扩缩消费者数量，来提升或降低消费能力。

**（2）广播消费模式**：当使用广播消费模式时，RocketMQ会将每条消息推送给消费组所有的消费者，保证消息至少被每个消费者消费一次。即使扩缩消费者数量也无法提升或降低消费能力。

## **1.2.5.6 RocketMQ事务消息**

RocketMQ 提供了事务消息的功能，采用 2PC (两段式协议) + 补偿机制（事务回查）的分布式事务功能，通过这种方式能达到分布式事务的最终一致。原理如下图所示：

![图片](http://cdn.passjava.cn/uPic/640-202508172150125540JFnoj.jpg)

事务消息发送步骤如下：

（1）发送方将半事务消息发送至消息队列 RocketMQ 版服务端。

（2）消息队列 RocketMQ 版服务端将消息持久化成功之后，向发送方返回 Ack 确认消息已经发送成功，此时消息为半事务消息。

（3）发送方开始执行本地事务逻辑。

（4）发送方根据本地事务执行结果向服务端提交二次确认（Commit 或是 Rollback），服务端收到 Commit 状态则将半事务消息标记为可投递，订阅方最终将收到该消息；服务端收到 Rollback 状态则删除半事务消息，订阅方将不会接受该消息。 事务消息回查步骤如下：

（5）在断网或者是应用重启的特殊情况下，上述步骤 4 提交的二次确认最终未到达服务端，经过固定时间后服务端将对该消息发起消息回查。

（6）发送方收到消息回查后，需要检查对应消息的本地事务执行的最终结果。

（7）发送方根据检查得到的本地事务的最终状态再次提交二次确认，服务端仍按照步骤 4 对半事务消息进行操作。

## **1.2.5.7 RocketMQ架构小结**

（1）RocketMQ协议层支持Remoting和gRPC协议。

（2）RocketMQ网络层是基于Netty扩展出来的高性能网络通信框架。

（3）RocketMQ存储层也是采用将消息顺序存储到同一个文件，支持分段存储。

（4）Broker需要向NameServer上传自己的元数据信息。

（5）生产者通过NameServer获取Broker的元数据信息，然后选择直连哪Broker，最后发送到具体的MessageQueue。

（6）消费者需要从NameServer获取Broker的元数据信息，然后选择直连哪台Broker 进行消费。

（7）RocketMQ还有消费者组的概念，在集群消费模式下，消费者会通过负载均衡来消费消息，最后通过提交消费位点的形式来保存消费进度。

## **在键盘与烟火之间**

上周六，家里的娃和小区的一个小朋友一起约了 5 点起来看日出，然后我们家长 4 点多就起来带他们去看日出，感觉小孩子们好浪漫，好疯狂啊。

![图片](http://cdn.passjava.cn/uPic/640-20250817215012572NCSOQm.jpg)

为了给他们的童年留下一点美好的事情，两家的家长也很配合，在键盘与烟火之间，感受烟火的寥寥升起，将自己的年龄倒带，回到童年中，用心陪孩子玩耍。

看完日出，骑着电动车在径河公园溜达了一圈，发现了一个超级大的草坪，放风筝绝对给力。

然后为了让孩子们体验摘果子，又骑电动车到了一个野果园，采摘了“小苹果”。接着又沿着金银湖畔溜达了一圈，在一个商圈找了一家热干面馆，号称武汉市第二届热干面大赛第一名的面馆，在这家面馆，小娃喜欢上了吃有“汤汤水水”的细粉～

然后我们一起去了图书馆陪着娃 1 个半小时的书，上午的旅程愉快的结束了。

第二天傍晚，又去了花田水世界玩水，前一个月就订好了票，但看到差评很多就没去。另外一家来了个突袭，问我们家去不去，没有过多考虑，直接冲，他们算是我们的一个推力。小娃从最开始不敢下水，到后面的 pk 游泳，有了很大的进步～

我是悟空，在键盘与烟火之间，记录生活的点点滴滴～
