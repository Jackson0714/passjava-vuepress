---
title: "TCPIP详解_卷1_协议_英文_第2版"
date: 1970-01-01
doc_type: weread-highlights-reviews
bookId: CB_8cD1Dt1F55bD6zv71H4tu4Lb
reviewCount: 1
noteCount: 5
author: Kevin R. Fall; W. Richard Stevens
cover: https://res.weread.qq.com/wrepub/CB_9aS0fA0bq8ak6vW6xG5BW45k_parsecover
progress: 21%
readingTime: 2小时8分钟
readingDate: 1970-01-01
isbn:
lastReadDate: 2025-11-21
---

# 元数据

> [!abstract] TCP:IP详解*卷1*协议*英文*第2版
>
> - ![ TCP:IP详解_卷1_协议_英文_第2版|200](https://res.weread.qq.com/wrepub/CB_9aS0fA0bq8ak6vW6xG5BW45k_parsecover)
> - 书名： TCP:IP详解*卷1*协议*英文*第2版
> - 作者： Kevin R. Fall; W. Richard Stevens
> - 简介：
> - 出版时间：
> - ISBN：
> - 分类：
> - 出版社：
> - PC地址：https://weread.qq.com/web/reader/25d42473643425f386344314474314635356244367a76373148347475344c62a71

# 高亮划线

### 5.2 IPv4 and IPv6 Headers

> 📌 widespread
> ⏱ 2025-11-21 11:20:53 ^CB-8cD1Dt1F55bD6zv71H4tu4Lb-93-3212-3222

> 📌 Explicit
> ⏱ 2025-11-21 11:21:20 ^CB-8cD1Dt1F55bD6zv71H4tu4Lb-93-3469-3477

> 📌 Congestion
> ⏱ 2025-11-21 11:21:25 ^CB-8cD1Dt1F55bD6zv71H4tu4Lb-93-3478-3489

> 📌 indicator
> ⏱ 2025-11-21 11:21:34 ^CB-8cD1Dt1F55bD6zv71H4tu4Lb-93-3517-3526

> 📌 forwarded
> ⏱ 2025-11-21 11:21:47 ^CB-8cD1Dt1F55bD6zv71H4tu4Lb-93-3650-3659

# 读书笔记

## 5.2 IPv4 and IPv6 Headers

### 划线评论

> 📌 5.2 IPv4 and IPv6 Headers
> Figure 5-1 shows the format of an IPv4 datagram. The normal size of the IPv4 header is 20 bytes, unless options are present (which is rare). The IPv6 header is twice as large but never has any options. It may have extension headers, which pro-vide similar capabilities, as we shall see later. In our pictures of headers and data-grams, the most significant bit is numbered 0 at the left, and the least significant bit of a 32-bit value is numbered 31 on the right. The 4 bytes in a 32-bit value are transmitted in the following order: bits 0–7 first, then bits 8–15, then 16–23, and bits 24–31 last. This is called big endian byte ordering, which is the byte ordering required for all binary integers in the TCP/IP headers as they traverse a network. It is also called network byte order. Computer CPUs that store binary integers in other formats, such as the little endian format used by most PCs, must convert the header values into network byte order for transmission and back again for reception.
> 5.2.1 IP Header Fields
> The first field (only 4 bits or one nibble wide) is the Version field. It contains the version number of the IP datagram: 4 for IPv4 and 6 for IPv6. ^37992928-84JlS7a03

    - 💭
    - ⏱ 2025-11-17 20:42:32

# 本书评论
