---
title: 安装 KingbaseES 遇到的问题
date: 2025-7-28
---

## 一、下载并安装SQL Server 兼容版KES数据库

### 下载地址

https://www.kingbase.com.cn/download.html

![img](http://cdn.passjava.cn/uPic/1753345189081-fb6cf05e-69b2-46b3-b5fd-bebc1732530daTTGYJq4KEnvHY1d9d.png)

该版本新增了对SQLServer若干系统视图和内置函数的支持，支持ICU库并对其进行了优化；支持更多的高级查询功能，包括FOR XML子句、PIVOT行列转换操作、GROUP BY子句中基于不同数据类型进行分组、DINSTICT子句与ORDER BY联合中列别名的使用等；新增DML操作触发更新统计信息功能，提升查询性能与增强系统的稳定性；新增临时表优化功能，提升了函数执行效率。在客户端编程接口方面，.Net驱动中新增了对SQL Server 中一些日期函数的支持，加入了更多针对各行业应用场景的定制化功能，助力企业实现平滑迁移和业务高效运行。

### 下载授权文件

KingbaseES数据库(SQLServer兼容版)授权文件时长限制为90天，以数据库首次启动为首日开始计算。

## 二、Windows 安装 KingBaseES 报错汇总

### 1、安装软件时，提示初始化数据库失败

#### 解决方案

需要把360安全软件关闭后再执行下一步。

### 2、无法启动服务

打开服务 services.msc，找到可执行文件的路径。

![img](http://cdn.passjava.cn/uPic/1753338549263-2057c0e6-6355-4454-a732-06e1e6768057xUc95bSrNkVo.png)

```sh
cd D:\Program Files\Kingbase\ES\V9\KESRealPro\V009R004C012\Server\bin
./sys_ctl.exe runservice -N "kingbase9_R1_instance" -D "D:\Program Files\Kingbase\ES\V9\data" -w

sys_ctl: could not start service "kingbase9_R1_instance": error code 1063

./sys_ctl.exe -D "kingbase9_R1_instance" -D "D:\Program Files\Kingbase\ES\V9\data" start

waiting for server to start.....
 HKT [18240] LOG:  正在启动 KingbaseES V009R004C012
 HKT [18240] LOG:  正在监听IPv6地址"::"，端口 54321
 HKT [18240] LOG:  无法绑定IPv4地址"0.0.0.0": Only one usage of each socket address (protocol/network address/port) is normally permitted.

 HKT [18240] HINT:  端口54321上是否已经运行了另一个kingbase?如果没有，请等待几秒钟后重试。
 HKT [18240] FATAL:  无法为"*"创建监听套接字
 HKT [18240] LOG:  database system is shut down
 stopped waiting
sys_ctl: could not start server
Examine the log output.
```

#### 解决方案

方案 1：查看端口是否被占用

```plain
netstat -ano | grep "54321"
kill <进程 id>
```

方案 2：更改启动端口

```plain
D:\Program Files\Kingbase\ES\V9\data
port=54325
```

重新启动，启动成功，如下图所示：

![image-20250724201706850](http://cdn.passjava.cn/uPic/image-20250724201706850BjV1gO.png)

查看进程

![img](http://cdn.passjava.cn/uPic/1753341920964-181a2ee3-0ab8-407b-b37f-11e344637c5fbqzTFfOx3DzY.png)

修改数据库连接的端口为 54325，连接成功，如下图所示：

![img](http://cdn.passjava.cn/uPic/1753342078542-496bd056-3c1b-49b8-b191-a03a18885e6bVTNMQvqXQ3EN.png)

### 3、无法连接数据库，报错乱码

#### 解决方案

安装时选择 utf8 编码

### 4、Register KingbaseES failed

这个问题困扰我许久，尝试方式如下

1. 更换license，包括windows版本，开发版本 -> 未能解决问题

2. 卸载重装，更改安装目录 -> 未能解决问题

最终换了一台电脑就好了，现在分析原因大概率是这台电脑做了设置，无法初始化实例！

### 5、Windows 默认安装路径安装失败

问题描述
在windows环境中安装KingbaseES V8安装包，安装时安装路径选择系统盘（C盘）默认安装路径（C:\Program Files）时，初始化数据库错误，导致数据库安装失败。

安装目录选择在C:\Program Files

![img](http://cdn.passjava.cn/uPic/341182b6abdda69c7092752cd7f8acccGaawHs.png)

安装时出现以下错误：

![img](http://cdn.passjava.cn/uPic/1425b026cfcaa75e1f157ecfc365e83d4Xnyeh.png)

解决方案
在安装KingbaseES V8安装包时，安装路径选择非默认路径外（桌面或D盘）的空文件夹：

![img](http://cdn.passjava.cn/uPic/548120a73b1d96ebc7a39b4a31c02f6byto38j.png)

这样初始化不会报错并能成功安装：

![img](http://cdn.passjava.cn/uPic/41abba615bc50771069a592aabddc4a0ghA8pE.png)

### 6、数据库初始化失败

异常：

![KingbaseES人大金仓数据库windows系统安装过程及异常处理](http://cdn.passjava.cn/uPic/00cd9808857ce92c0df7e8a1973452cchWLoHo.png)

安装过程设置账号密码下一步时出现 初始化失败

导致：data数据目录无法正常创建，服务正常无法启动

解决：手动生成指定data目录

创建数据存储文件夹data，右键文件夹属性-安全将访问权限打开（没有权限将无法创建data目录）

打开命令窗口cd 到 C:\Program Files\Kingbase\ES\V8\Server\bin目录

命令窗口输入 initdb -D “data文件夹的绝对路径” 即可生成data目录

输入 sys_ctl -D “data数据目录的绝对路径” start 即可启动服务（默认服务启动失败可自行注册）
