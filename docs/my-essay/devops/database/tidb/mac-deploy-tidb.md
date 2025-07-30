---
title: Mac M1 部署 TiDB
date: 2025-07-30
---

## 背景

之前在腾讯云上通过 TEM 部署了 TiDB 集群，但是腾讯云是按量计费的，普通平民真的用不起。所以想在本地 Mac 电脑上部署一套 TiDB 集群测试环境。

> 平凯数据库**企业级运维管理平台**（简称：TEM）是一款为 TiDB 打造的一站式全生命周期管理平台。
>
> TEM 现已在腾讯云上提供服务（TEM on Cloud），可以实现现有机房及公有云主机规划统一数据库资源池管理，无需迁移、无需改造，打开浏览器即可一站式在线管理 TiDB 集群。

## MacOS 部署本地测试集群

TiDB 是一个分布式系统。最基础的 TiDB 测试集群通常由 2 个 TiDB 实例、3 个 TiKV 实例、3 个 PD 实例和可选的 TiFlash 实例构成。通过 TiUP Playground，可以快速搭建出上述的一套基础测试集群。

### 安装环境

电脑芯片：Mac M1 Max, ARM 64 位

内存：32 GB

操作系统：MacOS 13.3.1

### 安装 TiUP

首先需要安装一个 TiUP，TiUP 又是啥？

> TiUP（TiDB Unified Platform）是 PingCAP 官方推出的开源命令行工具，用于简化 TiDB 生态组件的部署、管理与运维。

安装命令：

```SH
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

安装完成后如下图所示：

![](http://cdn.jayh.club/uPic/image-20250730103112345o8khOc.png)

根据上面的提示还需要声明全局环境变量。

```SH
source /Users/wukong/.zshrc
```

### 启动集群

在当前 session 执行以下命令启动集群。

直接执行 `tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

```SH
tiup playground
```

''也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

```SH
tiup playground v7.1.2 --db 2 --pd 3 --kv 3
```

启动成功后如下图所示：

![](http://cdn.jayh.club/uPic/image-20250730103608065RaYfGg.png)

执行该命令时，建议使用内存 10 GiB、4 CPU 及以上配置。配置过低可能会导致系统崩溃。

### 连接 TiDB 数据库

新开启一个 session，使用 TiUP 或 MySQL 客户端连接 TiDB。

- 使用 TiUP `client` 连接 TiDB：

  ```sh
  tiup client
  ```

- 或者使用 MySQL 客户端连接 TiDB：

  ```sh
  mysql --host 127.0.0.1 --port 4000 -u root
  ```

> 当我使用 tiup client 命令时，提示需要执行 tiup playground，但是执行这个命令又会安装 tidb 集群，未找到解决方案。
>
> ![](http://cdn.jayh.club/uPic/image-20250730104422373U8Fulw9j5wdI.png)

使用 Navicat 连接 TiDB 数据库。

![image-20250730104612331](http://cdn.jayh.club/uPic/image-20250730104612331zk43ya.png)

![](http://cdn.jayh.club/uPic/image-20250730111917591nN0aWR.png)

### 访问 Prometheus 页面

访问 Prometheus 管理界面：[http://127.0.0.1:9090](http://127.0.0.1:9090/)。

### 访问 TiDB Dashboard 页面

访问 [TiDB Dashboard](https://docs.pingcap.com/zh/tidb/stable/dashboard-intro/) 页面：http://127.0.0.1:2379/dashboard，默认用户名为 `root`，密码为空。

![image-20250730104829000](http://cdn.jayh.club/uPic/image-20250730104829000NYdE1i.png)

### 访问 Grafana 界面

- 访问 Grafana 界面：[http://127.0.0.1:3000](http://127.0.0.1:3000/)，默认用户名和密码都为 `admin`。

![](http://cdn.jayh.club/uPic/image-202507301050373764zat10.png)

### 清理

测试完成之后，可以通过执行以下步骤来清理集群：

1. 按下 `Control`+`C` 键停掉上述启用的 TiDB 服务。

2. 等待服务退出操作完成后，执行以下命令：

   ```sh
   tiup clean --all
   ```

## 总结

整体安装过程比较简单，耗时几分钟就安装好了。

Mac M1 上装 TiUP → `tiup playground` 一键拉起 TiDB+TiKV+PD+TiFlash → Navicat/MySQL 客户端连 4000 端口 → Prometheus(9090)、Grafana(3000)、TiDB Dashboard(2379/dashboard) 全都能看。
