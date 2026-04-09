---
title: TiDB 线上数据库和工具
date: 2025-09-08
---

你好，我是悟空。

## 背景

在学习 TiDB 的过程中，发现了一个新大陆，TiDB 官方支持免费创建在线的 TiDB 数据库，省去了本地部署 TiDB 的麻烦。

今天就带着大家一起看看如何创建一个 TiDB 的在线环境 TiDB Cloud，以及如何用在线的数据库连接工具，尤其是 AI 功能。

## TiDB Cloud 简介

> [!NOTE]
>
> TiDB Cloud 是由 PingCAP 公司提供的全托管云数据库服务（DBaaS），基于开源分布式关系型数据库 TiDB 构建，兼具传统关系型数据库的强一致性与 SQL 兼容性，以及 NoSQL 系统的水平扩展能力。它采用云原生架构，将计算与存储分离，支持在 AWS 和 Google Cloud 上一键部署，用户无需管理底层基础设施，即可快速获得高可用、高性能、弹性伸缩的数据库服务。

### 核心特性

- **MySQL 兼容**：支持 MySQL 协议，现有应用可零改造迁移。
- **HTAP 一体化**：同一套引擎同时处理在线事务（TP）与实时分析（AP），无需 ETL。
- **Serverless & 专有双模式**
  - Serverless：按请求与存储量计费，自动扩缩容，适合开发测试或流量波动场景。
  - 专有：预留资源，性能稳定，适合生产级长期负载。
- **AI 增强**：内置 Chat2Query 自然语言生成 SQL、AI 辅助调优、向量搜索与全文检索，方便构建生成式 AI 应用。
- **多云多区域**：已上线 AWS、GCP 多个 Region，支持跨云灾备与就近接入。
- **企业级安全合规**：提供 VPC 隔离、加密存储、自动备份、细粒度 RBAC，满足金融级合规要求。

## 注册 TiDB 在线账户

注册地址：https://auth.tidbcloud.com/login

注册界面如下图所示：

![image-20250908112412529a898zL.png](http://cdn.passjava.cn/uPic/image-20250908112412529a898zL-1757336009842-20250908212446862xqlsmT.png)

然后用邮箱登录，登录后，选择作为个人学习项目来创建账号。

![image-20250908112919905luiXMW.png](http://cdn.passjava.cn/uPic/image-20250908112919905luiXMW-1757336022407-20250908212446912BegCuN.png)

选择你在线的工作角色：

![image-20250908112951575HGyYYB.png](http://cdn.passjava.cn/uPic/image-20250908112951575HGyYYB-1757336049508-20250908212446954AuNmS2.png)

选择你现在用的数据库管理系统：

![image-20250908113032056BQ5T7Y.png](http://cdn.passjava.cn/uPic/image-20250908113032056BQ5T7Y-1757336063570-202509082124470012VyAa5.png)

选择你工作中用得最多的编程语言：

![image-20250908113116047wsWflz.png](http://cdn.passjava.cn/uPic/image-20250908113116047wsWflz-1757336098466-20250908212447055ZmzqlN.png)

然后填入公司名，选择用样例数据库还是稍后导入数据。

![image-20250908113223699su66Cj.png](http://cdn.passjava.cn/uPic/image-20250908113223699su66Cj-1757336107028-202509082124470958Gt888.png)

等待几秒就可以创建成功了。

![image-20250908113244762zHexgL.png](http://cdn.passjava.cn/uPic/image-20250908113244762zHexgL-1757336114626-20250908212447154Tu8xGG.png)

### 连接数据库

初始化数据库连接配置：

![image-20250908113356801pJIfzP.png](http://cdn.passjava.cn/uPic/image-20250908113356801pJIfzP-1757336124188-20250908212447207gGJrpg.png)

在弹框中点击生成密码，就会生成数据库密码了。后续可以用 navicat 等工具连接在线数据库，或者用在 mcp server 的配置中。

![image-20250908113420240pgfbWJ.png](http://cdn.passjava.cn/uPic/image-20250908113420240pgfbWJ-1757336132082-20250908212447261DCQM3z.png)

## 数据库操作

### AI 功能说明

当带你左侧 SQL Editor 时，会提示你是否用 AI 工具。

![image-20250908200848914j3b7HN.png](http://cdn.passjava.cn/uPic/image-20250908200848914j3b7HN-1757336139471-202509082124473263SvIxy.png)

翻译过来就是这个意思：

欢迎来到 TiDB Cloud 的 **Chat2Query** 功能！ Chat2Query 让你在 **SQL 编辑器** 和 **开放 API** 两端都能用“说人话”的方式操作数据库： 输入自然语言，它就能**自动生成、重写或优化 SQL 语句**。

要开启 Chat2Query，请先阅读并同意我们的隐私政策：

> 我们使用 AI 来提升你的体验。继续即表示你同意 **PingCAP** 通过 AI 功能处理你的代码片段，以持续改进我们的服务。 详细说明请见《AI 功能隐私声明》。

那肯定得勾选下这个功能，体验下 AI 的强大。

创建账号后，会自动创建样例数据库，如果没有创建，我们也可以自己创建数据库、表等。如下方所示，自动创建了 github_sample 和 test 数据库。

![image-202509081143560044uEfWW.png](http://cdn.passjava.cn/uPic/image-202509081143560044uEfWW-1757336196230-20250908212447389fTCKJN.png)

可以用该网站的 SQL Editor 在线编写 SQL、执行 SQL，还可以利用 AI 来纠错。

### AI 纠错

下面写一个创建表的语句，但是语法是有问题的。

```
USE test;
CREATE table1 {
  a int,
  b STARTING
}
```

执行后报错信息如下：

![image-20250908200848914j3b7HN.png](http://cdn.passjava.cn/uPic/image-20250908200848914j3b7HN-1757336209767-20250908212447436dZF5rD.png)

可以直接用该网站的 AI 工具自动修复：

![image-202509082010240044IGm6k.png](http://cdn.passjava.cn/uPic/image-202509082010240044IGm6k-1757336221043-20250908212447483zMyMUB.png)

我们可以点击 Accept 接收 AI 编写的 SQL 语句，也可以点击 Discard 拒绝，或者用 AI 重新生成 SQL 语句。

点击 Accept 接受该请求，再次运行，执行成功。

![image-20250908201317844.png](http://cdn.passjava.cn/uPic/image-20250908201317844-1757336231716-20250908212447528Jk9Pvs.png)

我们可以看到 table1 已经创建出来了。

![image-20250908201548601.png](http://cdn.passjava.cn/uPic/image-20250908201548601-1757336241881-20250908212447576F3hhnV.png)

### 测试执行计划

我们还可以在上面测试执行计划，点击 Explain 即可查看选中的 SQL 语句的执行计划结果。

![image-20250908201909471.png](http://cdn.passjava.cn/uPic/image-20250908201909471-1757336253392-20250908212447632eSzdHV.png)

还可以用图表的方式展示执行计划结果。

![image-20250908202008665.png](http://cdn.passjava.cn/uPic/image-20250908202008665-1757336263087-20250908212447678ZCNoKv.png)

### 创建分支

我们还可以基于当前的数据库创建多个分支，类似 gitlab 上创建分支一样简单。但是目前没有看到合并的功能，处于 beta 测试阶段。

![image-20250908202132795.png](http://cdn.passjava.cn/uPic/image-20250908202132795-1757336273711-20250908212447725eXsIB5.png)

### 导入数据

导入数据分为导入本地 csv 文件、从云存储导入、用第三方工具导入。

![image-20250908202215493.png](http://cdn.passjava.cn/uPic/image-20250908202215493-1757336281993-20250908212447787EOuIAz.png)

### 数据库备份

可以定时备份数据库。

![image-20250908202336899.png](http://cdn.passjava.cn/uPic/image-20250908202336899-1757336291009-20250908212447826SLuFi4.png)

### 慢查询监控

可以统计出有哪些慢查询。

![image-20250908202416060.png](http://cdn.passjava.cn/uPic/image-20250908202416060-1757336301716-20250908212447870TfHEDS.png)

## 监控

### SQL 语句记录

![image-20250908202508680.png](http://cdn.passjava.cn/uPic/image-20250908202508680-1757336311404-20250908212447926mwcW6W.png)

### 指标分析

分析数据库的指标，如 QPS、TPS 等。

![image-20250908202529782.png](http://cdn.passjava.cn/uPic/image-20250908202529782-1757336319784-20250908212447985oaNzCE.png)

### 事件记录

记录所有的操作事件。

![image-20250908202716471.png](http://cdn.passjava.cn/uPic/image-20250908202716471-1757336329910-2025090821244805339jp65.png)

## 网络设置

可以设置防火墙规则。

![image-20250908202802641.png](http://cdn.passjava.cn/uPic/image-20250908202802641-1757336343329-202509082124481130Z3uzZ.png)

### 使用 navicat 客户端连接在线的 TiDB 数据库

![image-20250908114841510TIxDKB.png](http://cdn.passjava.cn/uPic/image-20250908114841510TIxDKB-1757336360211-20250908212448176ueCkYD.png)

![image-20250908114855620IuBMHR.png](http://cdn.passjava.cn/uPic/image-20250908114855620IuBMHR-1757336374436-20250908212448221a6w5xm.png)

## 集群管理

### 创建集群

分为免费版和专用版，专用版是需要付费的，每小时 7 美元多。

![image-20250908203212807.png](http://cdn.passjava.cn/uPic/image-20250908203212807-1757336385816-20250908212448283xyVPmP.png)

### 数据服务

TiDB Cloud Data Service 是一项**全托管、低代码的后端即服务（Backend-as-a-Service）**解决方案。 它让后端开发化繁为简，帮助开发者快速构建**高可扩展、高安全、数据驱动**的应用。

在 Data Service 中，一切从**“Data App”**开始： Data App 是一个容器，用来托管一组 RESTful 端点（Endpoints），也是你整个项目的基石。

![image-20250908203747721.png](http://cdn.passjava.cn/uPic/image-20250908203747721-1757336394722-20250908212448350TFsbJM.png)

### 恢复 Group

![image-20250908203724309.png](http://cdn.passjava.cn/uPic/image-20250908203724309-1757336402342-202509082124484064Ho04p.png)

## 总结

TiDB Cloud 把“部署、运维、调优”三件事浓缩成“注册-建库-开写”三步：

1. 一分钟完成账号，自动生成样例数据；
2. SQL Editor 自带 Chat2Query，自然语言⇋SQL 双向转换，报错一键 AI 修复，Explain 图形化执行计划即刻看性能；
3. 分支、备份、慢查询、QPS/TPS 曲线、防火墙规则全图形化，支持 CSV/云存储/第三方工具秒级导入，Navicat 直连，免费额度足够开发测试，付费版本可弹到分布式集群；
4. 另赠低代码 Data Service，把表直接 RESTful 化，前端秒调接口。 至此，本地装 TiDB、写后端、调优、监控的历史全部进入“浏览器时代”。
