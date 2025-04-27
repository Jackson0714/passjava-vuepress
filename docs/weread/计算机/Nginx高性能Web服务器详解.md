---
doc_type: weread-highlights-reviews
bookId: "654105"
reviewCount: 0
noteCount: 1
author: 苗泽编著
cover: https://cdn.weread.qq.com/weread/cover/17/YueWen_654105/t7_YueWen_654105.jpg
readingStatus: 在读
progress: 38%
totalReadDay: 13
readingTime: 1小时56分钟
readingDate: 2023-08-31
isbn: 9787121215186
lastReadDate: 2023-09-16

---
# 元数据
> [!abstract] Nginx高性能Web服务器详解
> - ![ Nginx高性能Web服务器详解|200](https://cdn.weread.qq.com/weread/cover/17/YueWen_654105/t7_YueWen_654105.jpg)
> - 书名： Nginx高性能Web服务器详解
> - 作者： 苗泽编著
> - 简介： 本书全面介绍了当前Internet上流行的一款开放源代码的Web服务器——Nginx.全书一共分为四大部分，分别从入门、功能、实现和应用等四个方面对Nginx服务器的知识进行了完整阐述，满足了广大读者在应用Nginx服务器时的普遍性需求，同时也深入剖析了Nginx服务器的工作原理和实现技术，对其中使用到的数据结构和方法进行了详细阐述，并且结合实际的应用情况给出了多个基于Nginx服务器并结合其他典型服务器的分布式网站架构部署配置。
> - 出版时间： 2013-10-01 00:00:00
> - ISBN： 9787121215186
> - 分类： 计算机-计算机综合
> - 出版社： 电子工业出版社
> - PC地址：https://weread.qq.com/web/reader/e8d3200059fb19e8d3b2af6

# 高亮划线

## 第6章 Nginx服务器的Rewrite功能

> 📌 指令用于实现会话保持功能，将某个客户端的多次请求定向到组内同一台服务器上，保证客户端与服务器之间建立稳定的会话。只有当该服务器处于无效（down）状态时，客户端请求才会被下一个服务器接收和处理。其语法结构为：
   ​​​​​​ip_hash;​​
   ip_hash技术在一些情况下非常有用，能够避免我们关心的服务器组内各服务器之间会话共享的问题。但是ip_hash技术在实际使用过程中也有限制。
   首先，ip_hash指令不能与server指令中的weight变量一起使用。其次，由于ip_hash技术主要根据客户端IP地址分配服务器，因此在整个系统中，Nginx服务器应该是处于最前端的服务器，这样才能获取到客户端的IP地址，否则它得到的IP地址将是位于它前面的服务器地址，从而就会产生问题。同时要注意，客户端IP地址必须是C类地址。Nginx 1.3.2开发版本和Nginx 1.2.2稳定版本开始支持IPv6地址。
   我们来看下面这个示例：
   ​​​​​​upstream backend￼ ​​​​{￼ ​​​​  ip_hash;￼ ​​​​  server myback1.proxy.com;￼ ​​​​  server myback2.proxy.com;￼ ​​​​}​​
   该示例中配置了一个名为backend的服务器组，包含两台后端服务器myback1.proxy.com和myback2.proxy.com。在添加ip_hash指令后，我们使用同一个客户端向Nginx服务器发送请求，将会看到一直是由服务器myback1.proxy.com响应；如果注释掉ip_hash指令后进行相同的操作，发现组内的两台服务器轮流响应请求。 
> ⏱ 2023-09-16 17:43:56 ^654105-9-3657-4597

# 读书笔记

# 本书评论

