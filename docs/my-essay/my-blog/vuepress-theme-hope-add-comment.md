---
title: vuepress-theme-hope 主题添加评论功能（基于 waline + LeanCloud + Vercel 组件)
category: 博客优化
tag:
    - 博客优化
    - VuePress
    - 评论
---

## 评论效果图

![](http://cdn.jayh.club/uPic/image-20240826213042266uGkyHP.png)

## 依赖

| 组件                                                         | 说明                     |
| ------------------------------------------------------------ | ------------------------ |
| [Waline](https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/#waline) | 一个有后端的安全评论系统 |
| [LeanCloud ](https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/#leancloud-设置-数据库) | 数据库                   |
| [Vercel 部署 ](https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/#vercel-部署-服务端) | 服务端                   |

## Waline软件架构图

![Waline软件架构图](http://cdn.jayh.club/uPic/516671-20240131134443614-189961419YmVYHF.png)

##  Waline

waline[参考链接](https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/#%E7%BB%91%E5%AE%9A%E5%9F%9F%E5%90%8D-%E5%8F%AF%E9%80%89)

## LeanCloud

### 获取 APP ID 和 APP Key

请先 [登录](https://console.leancloud.app/login) 或 [注册](https://console.leancloud.app/register) `LeanCloud 国际版`, 进入 [控制台](https://console.leancloud.app/applist.html#/apps) 后点击左下角 [创建应用](https://console.leancloud.app/applist.html#/newapp)。创建应用后进入该应用，选择左下角的 `设置` > `应用Key`，然后记下 `APP ID`,`APP Key` 和 `Master Key`。

1. [登录](https://console.leancloud.app/login) 或 [注册](https://console.leancloud.app/register) `LeanCloud 国际版` 并进入 [控制台](https://console.leancloud.app/apps)

2. 点击左上角 [创建应用](https://console.leancloud.app/apps) 并起一个你喜欢的名字 (请选择免费的开发版):

   ![创建应用](https://ecosystem.vuejs.press/assets/leancloud-1-D6GvqV4-.png)创建应用

3. 进入应用，选择左下角的 `设置` > `应用 Key`。你可以看到你的 `APP ID`,`APP Key` 和 `Master Key`。请记录它们，以便后续使用。

   ![ID 和 Key](http://cdn.jayh.club/uPic/leancloud-2-B5wKvXiY4vmif2.png)

> 国内版需要完成备案接入
>
> 如果你正在使用 Leancloud 国内版 ([leancloud.cn](https://leancloud.cn/))，我们推荐你切换到国际版 ([leancloud.app](https://leancloud.app/))。否则，你需要为应用额外绑定**已备案**的域名，同时购买独立 IP 并完成备案接入:
>
> - 登录国内版并进入需要使用的应用
> - 选择 `设置` > `域名绑定` > `API 访问域名` > `绑定新域名` > 输入域名 > `确定`。
> - 按照页面上的提示按要求在 DNS 上完成 CNAME 解析。
> - 购买独立 IP 并提交工单完成备案接入。(独立 IP 目前价格为 ￥ 50/个/月)
>
> ![域名设置](http://cdn.jayh.club/uPic/leancloud-3-D7gbeXS0KmYO1o.png)



##  Vercel

[参考链接](https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/#vercel-%E9%83%A8%E7%BD%B2-%E6%9C%8D%E5%8A%A1%E7%AB%AF)

[deploy vercel](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fwalinejs%2Fwaline%2Ftree%2Fmain%2Fexample)

1. 点击上方按钮，跳转至 Vercel 进行 Server 端部署。

   提示

   如果你未登录的话，Vercel 会让你注册或登录，请使用 GitHub 账户进行快捷登录。

2. 输入一个你喜欢的 Vercel 项目名称并点击 `Create` 继续。

## 代码添加评论插件

参考链接：https://theme-hope.vuejs.press/zh/guide/feature/comment.html

博客根目录执行以下命令安装依赖：

``` SH
npm i -D @waline/client
```

theme.ts 添加评论插件：

``` JS
import { hopeTheme } from "vuepress-theme-hope";

export default {
  theme: hopeTheme({
    plugins: {
      comment: {
        // 选择一个评论服务
        provider: "Waline",

        // 服务选项
        serverURL: "...", // your serverURL
      },
    },
  }),
};
```



![添加评论插件](http://cdn.jayh.club/uPic/image-202408262117233266cS6Yr.png)

## 绑定域名

1. 点击顶部的 `Settings` - `Domains` 进入域名配置页

2. 输入需要绑定的域名并点击 `Add`

   ![Add domain](http://cdn.jayh.club/uPic/vercel-8VZx5yg.png)Add domain

3. 在域名服务器商处添加新的 `CNAME` 解析记录

   | Type  | Name    | Value                |
   | ----- | ------- | -------------------- |
   | CNAME | example | cname.vercel-dns.com |

4. 等待生效，你可以通过自己的域名来访问了🎉

   - 评论系统：example.your-domain.com
   - 评论管理：example.your-domain.com/ui

   ![success](http://cdn.jayh.club/uPic/vercel-9Vr8ZEz.png)success

![绑定域名](http://cdn.jayh.club/uPic/image-20240826212839501ZVnX18.png)

## [评论管理 (管理端)](https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/#评论管理-管理端)

1. 部署完成后，请访问 `<serverURL>/ui/register` 进行注册。首个注册的人会被设定成管理员。
2. 管理员登陆后，即可看到评论管理界面。在这里可以修改、标记或删除评论。
3. 用户也可通过评论框注册账号，登陆后会跳转到自己的档案页。

## 参考

https://theme-hope.vuejs.press/zh/guide/feature/comment.html

https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/

https://waline.js.org/guide/get-started/
