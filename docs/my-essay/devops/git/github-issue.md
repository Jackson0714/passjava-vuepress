---
title: github 常见问题
date: 2025-03-12
---

## git clone 报错：HTTP/2 stream 1 was not closed

```SH
git clone xxx
Cloning into 'xxx'...
fatal: unable to access 'https://github.com/zkep/my-geektime.git/': HTTP/2 stream 1 was not closed cleanly before end of the underlying stream
```

### 解决办法

```SH
git config --global http.version HTTP/1.1
```

## **Git 报错： Failed to connect to github.com port 443 解决方案**

### 解决办法

参考：https://blog.csdn.net/zpf1813763637/article/details/128340109

#### 两种情况：

**第一种情况自己有 vpn**，网页可以打开 github。说明命令行在拉取 / 推送代码时并没有使用 vpn 进行代理

**第二种情况没有 vpn**，这时可以去某些网站上找一些代理 ip+port

#### 解决办法：配置 http 代理 Windows、Linux、Mac OS 中 git 命令相同：

**配置 socks5 代理**

```sh
git config --global http.proxy socks5 127.0.0.1:7890
git config --global https.proxy socks5 127.0.0.1:7890
```

**配置 http 代理**

```sh
git config --global http.proxy 127.0.0.1:7890
git config --global https.proxy 127.0.0.1:7890
```

**注意：**

**命令中的主机号**（127.0.0.1）是使用的代理的主机号 (自己电脑有 vpn 那么本机可看做访问 github 的代理主机)，即填入 127.0.0.1 即可，否则填入代理主机 ip(就是网上找的那个 ip)
**命令中的端口号**（7890）为代理软件 (代理软件不显示端口的话，就去 Windows 中的代理服务器设置中查看) 或代理主机的监听 IP，可以从代理服务器配置中获得，否则填入网上找的那个端口 port

![img](http://cdn.passjava.cn/uPic/95317cc8ee4be11ca79e5744ad7a1ec25fDvwA.png)

socks5 和 http 两种协议由使用的代理软件决定，不同软件对这两种协议的支持有差异，如果不确定可以都尝试一下
**主机号和端口号可在代理的位置查看 (自己有 vpn 的需要查看)**

![img](http://cdn.passjava.cn/uPic/51468f9bb9698bf45f234a0f125cf292U8gL36.png)

**查看代理命令**

```sh
git config --global --get http.proxy
git config --global --get https.proxy
```

**取消代理命令**

```sh
git config --global --unset http.proxy
git config --global --unset https.proxy
```
