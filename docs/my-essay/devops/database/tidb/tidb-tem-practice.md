---
title: 运维管理平台（TEM）腾讯云安装 + TiDB 集群实践
date: 2025-07-28
---

## 背景

### TEM 介绍

平凯数据库**企业级运维管理平台**（简称：TEM）是一款为 TiDB 打造的一站式全生命周期管理平台，面向 TiDB（平凯数据库 v7.1 及 TiDB 社区版 v6.5 以上版本）提供，让用户在一个 Web 界面内即可完成 TiDB 集群**部署/纳管/升级**、参数配置、节点扩缩容、综合监控、告警、自动化备份策略、故障自愈与性能诊断、任务定时执行、服务器/集群 CPU、内存、磁盘 I/O 等资源利用实时可视化。实现数据库统一资源池建设，彻底告别多集群、多组件来回切换及复杂命令行，让大规模、多集群场景下的运维更简单、更安全、更自动化。

TEM 现已在腾讯云上提供服务（TEM on Cloud），可以实现现有机房及公有云主机规划统一数据库资源池管理，无需迁移、无需改造，打开浏览器即可一站式在线管理 TiDB 集群。

### TEM 功能 & 架构介绍

[![TEM 功能 & 架构介绍](http://cdn.jayh.club/uPic/95078221a2cf55309aa8f61ea193788ad6e58596_2_526x500D8VBY4.png)

## 创建 Tem 服务器的入口

https://app.cloud.tencent.com/detail/SPU_BHEHDBABGB3181

![image-20250728215611303](http://cdn.jayh.club/uPic/image-20250728215611303Xpowwc.png)

## 选购软件、云资源

![](http://cdn.jayh.club/uPic/image-20250728215544765q5BmyU.png)

## 安装部署

![image-20250728215123314](http://cdn.jayh.club/uPic/image-2025072821512331443gXFN.png)

![image-20250728215137952](http://cdn.jayh.club/uPic/image-20250728215137952MId0hD.png)

### 创建成功

### 概览

![image-20250728215749369](http://cdn.jayh.club/uPic/image-20250728215749369H390Fu.png)

### 应用信息

![image-20250728215826841](http://cdn.jayh.club/uPic/image-20250728215826841Nhzxgj.png)

### 应用资源

![image-20250728215847961](http://cdn.jayh.club/uPic/image-20250728215847961ianCtW.png)

### 应用配置

![image-20250728215937729](http://cdn.jayh.club/uPic/image-20250728215937729pIg11n.png)

### 安装日志

![](http://cdn.jayh.club/uPic/image-20250728220002433jhCvS1.png)

## 节点管理

![image-20250728221330516](http://cdn.jayh.club/uPic/image-2025072822133051626lstr.png)

### 免密登录服务器

![image-20250728221204769](http://cdn.jayh.club/uPic/image-20250728221204769Irz4e6.png)

## 打开 Tem 站点

http://<ip>:32000/login

![image-20250728221947758](http://cdn.jayh.club/uPic/image-202507282219477582RxbFQ.png)

![image-20250728222010943](http://cdn.jayh.club/uPic/image-20250728222010943rFIHgI.png)

![image-20250728222034336](http://cdn.jayh.club/uPic/image-202507282220343367snCJ0.png)

### 确认被控主机上已经安装 TiUP 组件

![image-20250728223734677](http://cdn.jayh.club/uPic/image-20250728223734677tG2llG29ZvaH.png)

### 添加凭证

![image-20250728222933646](http://cdn.jayh.club/uPic/image-20250728222933646cDGoQL.png)

凭证密码在这里：

![image-20250728224306500](http://cdn.jayh.club/uPic/image-20250728224306500dIybl6.png)

### 添加中控机

![image-20250728224336275](http://cdn.jayh.club/uPic/image-20250728224336275X4Gb2w.png)

### 添加主机

![image-20250728224613173](http://cdn.jayh.club/uPic/image-20250728224613173zTMQku.png)

![image-20250728224747018](http://cdn.jayh.club/uPic/image-20250728224747018bnhC5l.png)

### 创建集群

![image-20250728225108697](http://cdn.jayh.club/uPic/image-20250728225108697Y3OYJI.png)

### 添加节点

![image-20250728225136107](http://cdn.jayh.club/uPic/image-20250728225136107dH8Sw3.png)

![image-20250728225202096](http://cdn.jayh.club/uPic/image-202507282252020969JhkZU.png)

![image-20250728225522486](http://cdn.jayh.club/uPic/image-20250728225522486aBGqwJ.png)

![image-20250728225542059](http://cdn.jayh.club/uPic/image-20250728225542059DHvLkH.png)

注意端口冲突问题。

![image-20250728225803765](http://cdn.jayh.club/uPic/image-20250728225803765YfBrXw.png)

![image-20250728225823770](http://cdn.jayh.club/uPic/image-20250728225823770ER1pjF.png)

![image-20250728225841796](http://cdn.jayh.club/uPic/image-20250728225841796bVrm7a.png)

创建集群成功

![image-20250728230128790](http://cdn.jayh.club/uPic/image-20250728230128790e93ssn.png)

## 纳管集群

![image-20250728230204940](http://cdn.jayh.club/uPic/image-20250728230204940sZIvgc.png)

## 集群状态

### 概述

![image-20250728230242471](http://cdn.jayh.club/uPic/image-20250728230242471oDymzH.png)

访问 Grafna

http://132.232.206.246:3000/login

![image-20250728230519319](http://cdn.jayh.club/uPic/image-20250728230519319WeOz6j.png)

### 拓扑

![image-20250728230304810](http://cdn.jayh.club/uPic/image-20250728230304810d5se88.png)

### 监控

![image-20250728230339086](http://cdn.jayh.club/uPic/image-20250728230339086SrsBmK.png)

### 诊断

![image-20250728230843304](http://cdn.jayh.club/uPic/image-20250728230843304uthMQa.png)

### SQL 编辑器

![image-20250728231034145](http://cdn.jayh.club/uPic/image-20250728231034145KznnKF.png)

## 应用

### 新建应用

![image-20250728220225671](http://cdn.jayh.club/uPic/image-20250728220225671RxSBsi.png)

![image-20250728220437585](http://cdn.jayh.club/uPic/image-20250728220437585nay1Or.png)

参考：https://tidb.net/blog/3cb0dabf
