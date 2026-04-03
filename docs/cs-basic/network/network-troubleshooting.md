---
title: 网络故障排查
date: 2025-07-25
---

转载：Alex 的网络故障排查

网卡问题排障： 网卡buff溢出，端口速率协商失败，网卡流控丢包，mac地址错误，和其他异常丢包情况分析。

![图片](http://cdn.passjava.cn/uPic/640QJyYyd.jpg)

网卡驱动问题排障： 驱动收包队列溢出丢包，驱动处理异常丢包，单核负载丢包等。

![图片](http://cdn.passjava.cn/uPic/640-202507252242574735p8bZH.jpg)

协议栈问题排障：主要是协议栈分层丢包问题排障，比如邻居系统ARP层，IP网络层，TCP/UDP传输层，socket层等。

![图片](http://cdn.passjava.cn/uPic/640-20250725224257499CAn4rv.jpg)

分析工具：主要是常用网络排障工具介绍，包括经典定位排障工具，抓包工具，抓包分析工具，报文修改工具，内核协议栈丢包排查工具集等。

![图片](http://cdn.passjava.cn/uPic/640-20250725224257667TemD1q.jpg)

...
