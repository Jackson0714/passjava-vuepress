---
title: Docker快速安装KingbaseES
date: 2025-05-15
---

https://bbs.kingbase.com.cn/blogDetail?postsId=91fc0f4d8be5df33b2d4ebb636d239cd

通过推文得知KingBaseES在进行征文活动，我这边正好有国产化数据使用的需求，但是目前使用的是其他的国产数据库，正好通过此次征文活动，尝试一下KingbaseES部署使用，看看是否适合我们的业务场景。由于之前并未使用过KingbaseES，打算先简单部署上，以便进行开发测试，那么就先写一下我的部署过程，和遇到的问题以及解决办法

一、安装前准备工作

1.1、选择使用docker安装方式

简单看了官方文档，发现kingbaseES支持使用docker部署，感觉部署瞬间就简单多了，决定这次尝试kingbaseES就使用docker了。docker部署文档传送门。

1.2、准备安装环境

操作系统选择使用了ubuntu，毕竟centos的情况大家也应该都有所了解，本来是想用国产操作系统和国产CPU的，但是资源被使用着，没得办法，最后就是ubuntu2204和X64的CPU架构，资源4CPU，16G内存，200G硬盘，想来一个简单的测试环境应该是没啥问题了

下载官方镜像，下载地址，不太理解为什么没有上传到docker hub，或者自己实现一个docker镜像仓库，感觉官方可以考虑自己建设一个。

1.3、安装docker

感觉这部分没什么可说的，参考docker的官方文档进行安装吧，安装后执行docker info命令测试一下docker正常启动就可以了，还是比较容易的。

二、KingbaseES安装

2.1、首先加载镜像

```
# 加载镜像

docker load &lt; kdbx8664_V009R001C001B0025.tar
```

2.2、启动服务

官方文档中4.2部分，第一个启动命令如下

```
docker run -idt --privileged -p ${hostport}:${containerport} –v ${hostpath}:${containerpath} --name ${sub_container} ${image} /usr/sbin/init
```

能看出来，大意就是启动容器，挂载数据库目录，映射端口，指定启动命令是/usr/sbin/init，后面的4.2.2 4.2.3 4.2.4应该是对这个参数的解释。这部分按需修改，4.3部分讲解了设置环境变量，给出的参考命令

```
docker run -tid \

--name kingbase \

-e ENABLECI=${enableci} \

-e NEEDSTART=${needstart} \

-e DB_USER=${username} \

-e DB_PASSWORD=${passwd} \

-e DB_MODE=${dbmode} \

kingbase:v1 \

/bin/bash
```

从4.3.2到4.3.7这部分是对变量的解释。

可以说官方对运行应用所需的所有参数在这部分都给出了非常详细的解释说明，并给出了多个运行的示例，我们只需要按照自己生产需要结合官方的说明文档，整合出一个适合自己使用的命令即可。

通过分析官方的安装文档，结合自己使用的案例，最后写了一个下面的启动命令

```
docker run -d --name kingbase -p 4321:54321 \

--privileged \

--log-opt max-size=10m \

-v /etc/localtime:/etc/localtime:ro \

-v /etc/timezone:/etc/timezone \

-e DB_PASSWORD=aabbcc123@@ \

-e DB_MODE=mysql \

-v /work/kingbase/data:/home/kingbase/userdata/ \

kingbasev009r001c001b0025single_x86:v1 /usr/sbin/init
```

按照我的需求整合了一下，增加了docker的日志限制，避免本来就不大的空间被日志写满，挂载宿主机的时区文件，保证物理机和容器内部时区一致

启动后，查看日志

![image.png](http://cdn.passjava.cn/uPic/70d423d5d32e463eb7ab716a58b8b4c3-20250430164037080zSDXqQ.png)

进入容器，查看一下进程
![image.png](http://cdn.passjava.cn/uPic/32858dca7db748c5aa33672f8bdf48c8-20250430164047562hOtb37.png)

尝试连接
![image.png](http://cdn.passjava.cn/uPic/eac31d8d50754b7a8bf29452e75dc6e7bzj80Q.png)

安装到此结束，按照官方文档核对了一下，应该是没啥问题了

三、总结
安装算是比较顺利，就是在docker run命令的参数那纠结了一段时间，主要是最开始没看懂官方文档想表达的意思，分析清楚后就比较容易了，docker安装还是方便很多，而且让我比较奇怪的是为什么镜像这么小，因为我看了ISO的安装包，2个多G，镜像才将近700M。不过docker部署的环境，尽量还是不要在生产中使用吧，尤其是数据库类型的应用，如果真出了问题，可能会很麻烦
