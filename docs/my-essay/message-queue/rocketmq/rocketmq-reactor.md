---
title: RocketMQ Reactor多线程模型流程图
date: 2025-08-01
---

```mermaid
graph TD
    A[客户端请求] --> B[Reactor主线程<br/>NettyBoss_%d<br/>线程数: 1]
    B --> C{操作系统类型}
    C -->|Linux| D[EpollEventLoopGroup]
    C -->|其他| E[NioEventLoopGroup]
    D --> F[监听TCP连接请求]
    E --> F
    F --> G[建立连接<br/>创建SocketChannel<br/>注册到Selector]

    G --> H[Reactor线程池<br/>NettyServerEPOLLSelector_%d_%d<br/>线程数: 3]
    H --> I[监听网络数据]
    I --> J[接收网络数据]

    J --> K[Worker线程池<br/>NettyServerCodecThread_%d<br/>线程数: 8]
    K --> L[SSL验证]
    L --> M[协议编解码]
    M --> N[空闲检查]
    N --> O[网络连接管理]
    O --> P[解析RemotingCommand]

    P --> Q[根据请求码查找Processor]
    Q --> R{请求码类型}

    R -->|SEND_MESSAGE| S[发送消息线程池<br/>sendMessageExecutor]
    R -->|PULL_MESSAGE| T[拉取消息线程池<br/>pullMessageExecutor]
    R -->|ACK_MESSAGE| U[确认消息线程池<br/>ackMessageExecutor]
    R -->|HEART_BEAT| V[心跳处理线程池<br/>heartbeatExecutor]
    R -->|QUERY_MESSAGE| W[查询消息线程池<br/>queryMessageExecutor]
    R -->|其他| X[默认处理器线程池<br/>defaultExecutor]

    S --> Y[SendMessageProcessor<br/>处理发送消息业务]
    T --> Z[PullMessageProcessor<br/>处理拉取消息业务]
    U --> AA[AckMessageProcessor<br/>处理确认消息业务]
    V --> BB[ClientManageProcessor<br/>处理心跳业务]
    W --> CC[QueryMessageProcessor<br/>处理查询消息业务]
    X --> DD[DefaultProcessor<br/>处理默认业务]

    Y --> EE[业务处理完成]
    Z --> EE
    AA --> EE
    BB --> EE
    CC --> EE
    DD --> EE

    EE --> FF[构建响应]
    FF --> GG[编码响应]
    GG --> HH[发送响应给客户端]

    style B fill:#e1f5fe
    style H fill:#f3e5f5
    style K fill:#e8f5e8
    style S fill:#fff3e0
    style T fill:#fff3e0
    style U fill:#fff3e0
    style V fill:#fff3e0
    style W fill:#fff3e0
    style X fill:#fff3e0
```

![](http://cdn.jayh.club/uPic/image-20250801093432971tzRoRR.png)

## 线程池层次结构

```mermaid
graph TB
    subgraph "Reactor主线程层"
        A1[NettyBoss_%d<br/>1个线程<br/>职责: 连接建立]
    end

    subgraph "Reactor线程池层"
        A2[NettyServerEPOLLSelector_%d_%d<br/>3个线程<br/>职责: 网络I/O处理]
    end

    subgraph "Worker线程池层"
        A3[NettyServerCodecThread_%d<br/>8个线程<br/>职责: 协议处理]
    end

    subgraph "业务线程池层"
        A4[sendMessageExecutor<br/>发送消息线程池]
        A5[pullMessageExecutor<br/>拉取消息线程池]
        A6[ackMessageExecutor<br/>确认消息线程池]
        A7[heartbeatExecutor<br/>心跳处理线程池]
        A8[queryMessageExecutor<br/>查询消息线程池]
        A9[其他业务线程池]
    end

    A1 --> A2
    A2 --> A3
    A3 --> A4
    A3 --> A5
    A3 --> A6
    A3 --> A7
    A3 --> A8
    A3 --> A9

    style A1 fill:#e1f5fe
    style A2 fill:#f3e5f5
    style A3 fill:#e8f5e8
    style A4 fill:#fff3e0
    style A5 fill:#fff3e0
    style A6 fill:#fff3e0
    style A7 fill:#fff3e0
    style A8 fill:#fff3e0
    style A9 fill:#fff3e0
```

## 关键配置参数

```mermaid
graph LR
    subgraph "NettyServerConfig配置"
        B1[serverSelectorThreads: 3<br/>Reactor线程池大小]
        B2[serverWorkerThreads: 8<br/>Worker线程池大小]
        B3[serverCallbackExecutorThreads: 0<br/>回调线程池大小]
        B4[serverOnewaySemaphoreValue: 256<br/>单向请求信号量]
        B5[serverAsyncSemaphoreValue: 64<br/>异步请求信号量]
    end

    subgraph "BrokerController业务线程池"
        B6[sendMessageExecutor<br/>发送消息线程池]
        B7[pullMessageExecutor<br/>拉取消息线程池]
        B8[ackMessageExecutor<br/>确认消息线程池]
        B9[heartbeatExecutor<br/>心跳处理线程池]
        B10[queryMessageExecutor<br/>查询消息线程池]
    end

    B1 --> B6
    B2 --> B7
    B3 --> B8
    B4 --> B9
    B5 --> B10

    style B1 fill:#e1f5fe
    style B2 fill:#f3e5f5
    style B3 fill:#e8f5e8
    style B4 fill:#fff3e0
    style B5 fill:#fff3e0
    style B6 fill:#e1f5fe
    style B7 fill:#f3e5f5
    style B8 fill:#e8f5e8
    style B9 fill:#fff3e0
    style B10 fill:#fff3e0
```

## 异常处理流程

```mermaid
graph TD
    A[请求处理] --> B{线程池是否满?}
    B -->|是| C[RejectedExecutionException]
    C --> D[返回SYSTEM_BUSY响应]
    D --> E[记录警告日志]

    B -->|否| F{业务处理是否异常?}
    F -->|是| G[捕获异常]
    G --> H[返回SYSTEM_ERROR响应]
    H --> I[记录错误日志]

    F -->|否| J[正常处理完成]
    J --> K[返回成功响应]

    style C fill:#ffebee
    style G fill:#ffebee
    style D fill:#fff3e0
    style H fill:#fff3e0
    style K fill:#e8f5e8
```

#### 2. **主节点（Master）与从节点（Slave）的关系**

| **机制**     | **说明**                                                                                         |
| :----------- | :----------------------------------------------------------------------------------------------- |
| **数据同步** | 主节点**异步/同步**复制消息到从节点<br>（通过 `brokerRole=ASYNC_MASTER/SYNC_MASTER/SLAVE` 配置） |
| **故障接管** | 主节点宕机时，从节点**不会自动升主**<br>（需运维干预或依赖 RocketMQ 5.0 的 Dledger 自动选主）    |
| **读扩散**   | 消费者默认从主节点读<br>高负载时可配置 `consumeFromWhere=CONSUME_FROM_SLAVE` 从从节点读          |

> ⚠️ **注意**：
>
> - **主从切换非自动**：传统架构需人工介入（如重启 Broker 切换角色）；
> - **5.0 改进**：Dledger 模式支持基于 Raft 协议自动选主（类似 Kafka Controller）。
