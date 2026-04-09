---
title: how to check mss
date: 2024-08-18
---

什么？你是怎么从数据包看出 MTU 异常的

**一. 背景**

近期有部分用户反馈我司某款 APP 内容一直加载失败，我们进行了排查与记录，并分享给大家

在开始正文之前，我们先来回顾一些基础知识：

1. MTU 是二层协议里面的最大传输单元，指帧内容的最大值，不包括帧头和 FCS。以太网 MTU 标准是 1500 bytes
2. MSS 是指 TCP 最大有效载荷，通常会在 SYN 包中宣告。中间设备可以修改 MSS 大小，专业术语称为 MSS Clamping
3. 在实践中，传输大量数据时，TCP 倾向于发送满载的数据包
4. Wireshark 中展示的帧长度不包括 4 bytes 的 FCS

![img](http://cdn.passjava.cn/uPic/640jDQ61W.png)

**二. 问题排查**

先上一张抓包截图，看看你能不能发现其中的异常

![img](http://cdn.passjava.cn/uPic/640-20240724225832189ssto54.png)

从这张图中一眼可以看出最后几个数据包 Client 一直在重传，但是 Server 没有 Ack

顺着重传包往上看，会发现被重传的是 Client 发起的序号为 16 的包。同时期间有 Server 发送的数据包被 Client Ack 了，这说明 Server 和 Client 还能交互，但是 Server 却没有收到 16 号包

那么问题来了，为什么 Server 没有收到 16 号包

来看看 16 号包有什么特征，Length 1514，是一个满载的数据帧

我们再往上倒一眼，看到 Server 连续发送的 6、7、8、9 四个包中，前三个 Length 都是 1506。这里疑点就出现了，为什么 Length 不是 1514。说明很可能中间设备修改了 Client 发给 Server 的 SYN 包中的 MSS，改为了 1452。这里我们有理由怀疑中间设备的 MTU 发送了变化

![img](http://cdn.passjava.cn/uPic/640-20240724225832223xUkQZ2.png)

再往上从 2 号包还可以看到 Server 发给 Client 的 SYN 包 MSS 是 1460，常规大小，没有变化。这里我们有理由怀疑中间设备对 MSS 的处理出现了异常，只处理了单向的 MSS。导致 Client 没有感知到路径上 MTU 的变化，导致满载 1514 大小的数据帧被丢弃

![img](http://cdn.passjava.cn/uPic/640-20240724225832275MG1zgW.png)

上面只有部分证据，怎么进一步证实呢：

用 ping 发送一个满载的禁止分片的包来探测

```
ping -M do -s 1472 -c 3 -i 0.2 ip
```

运气好的话，你会收到类似下面这种明显的提示。我们确实收到了:-)，这就证明了我们上面的猜测

```
ping: local error: Message too long, mtu=1492
```

如果没有明确的提示也可以通过调整 -s 参数逐步降低载荷，探测路径最小 MTU

如果想探测到具体是哪一跳的 MTU 异常，可以通过指定 TTL 来探测：

```
ping -M do -s 1472 -c 3 -i 0.2 ip -t 3
```

到这里分析还没有结束，让我们更深入业务来看一看。已知上面的请求是普通的 HTTP API Get 请求， 不涉及数据上传。暂停一会儿，你有看出其中反常的地方吗

如果没有，再来看一张 TLS 解密后的 HTTP API Get 请求，不知你是否看出其中端倪

![img](http://cdn.passjava.cn/uPic/640-20240724225832303HmNsYq.png)

下面揭晓答案

通常来说，Client 端发送的 API 类请求原始数据远小于 1460，再加上 HTTP/2 的头部压缩，数据量会更小，很少出现满载的数据包

所以我们和业务同学做了确认，原来是因为业务需求在新版本请求中加了一些非常大的参数。用户的报障也是从新版本上线后多起来的，回退到老版本可以避免触发相关问题。业务同学根据我们的反馈也在进行相应的优化

老版本请求大小：

![img](http://cdn.passjava.cn/uPic/640-20240724225832327avsvuP.png)

新版本请求大小：

![img](http://cdn.passjava.cn/uPic/640-20240724225832352tfKcuA.png)

Tips: 如果你想要观察 TLS 解密后的数据包，可以配置 SSLKEYLOGFILE 环境变量记录 TLS 会话密钥，再用 Wireshark 解密。Chrome、Curl、Firefox 等都支持这种方法

**三. 结语**

到此我们的分析就结束啦。抓包并分析是一种非常高效的 debug 方法，已经帮助笔者解决了不少问题。

不过笔者在处理此 case 时远没有文中那么顺畅，有很多细碎知识点运用并不熟练，初期没有相互关联起来。好在一个问题有多个观察面，念念不忘，逐渐搜集证据和知识，终于破案。以此记录，希望对你能有所助益。

**推荐阅读：**

1. 有关 MTU 和 MSS 的一切：*https://www.kawabangga.com/posts/4983* (以及这位博主的其他文章)
2. 《Wireshark 网络分析就这么简单》
3. 《Wireshark 网络分析的艺术》

-End-

作者丨 House
