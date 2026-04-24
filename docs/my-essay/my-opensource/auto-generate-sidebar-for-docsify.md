---
title: 一键生成基于 docsify 框架网站的侧边栏
tag:
  - 开源项目
  - 博客美化
  - docsify
date: 2024-09-06
---

## 背景

docsify 网站的侧边栏每次都需要手动添加菜单链接，比较麻烦，想要一键自动生成目录。比如下图框起来的目录。

![](http://cdn.passjava.cn/uPic/image-20240906220729425uKA0ZB.png)

当我们需要修改侧边栏菜单时，需要编辑 \_sidebar.md 文件才行。

![image-20240906220823739](http://cdn.passjava.cn/uPic/image-20240906220823739AyE9ic.png)

该文件的内容如下：

![](http://cdn.passjava.cn/uPic/image-20240906220931026yaVvFF.png)

那有没有一种办法能自动添加侧边栏目录，或者一键生成侧边栏目录呢？

我写了一个小工具，一键生成docsify 的目录，github 上开源了。

## 包含功能

- 一键生成docsify 的目录文件 \_sidebar.md 和 README.md 文件。
- 上传修改的文件到 Git 仓库。
- Ssh登录网站服务器拉取最新仓库代码，更新网站菜单。

## 前提

### Git 仓库

本地网站代码需要配置远程的代码仓库地址和分支。提交命令在代码里面，如下所示：

```SH
git push origin main
```

### 网站服务器登录账号

该开源项目里面的登录方式用的是密钥文件。

## 代码

[docsify-generate-sidebar](https://github.com/Jackson0714/docsify-generate-sidebar)

## 调整内容

修改以下四项内容，可以全局搜索替换下。

```JAVA
// 网站代码的根目录
String rootFolder = "/Users/wukong/xxx/docs/";
// 服务器密钥路径
String keyPath = "~/xxx";
// 服务器上的网站部署路径
String remoteDirectory = "~/jay/geek/docs";
String filePathWithHttpLink = ("http://你的网站地址/#" + filePath).replace(".md", "");
```

## 适用场景

- 个人博客、技术笔记、项目文档等 docsify 站点。
- 多人协作时，自动生成统一格式的菜单，减少合并冲突。
- 配合 CI/CD（如 GitHub Actions）实现每次推送代码后自动更新侧边栏。

## 总结

这个小工具解决了 docsify 网站侧边栏需要手动维护的痛点，通过一键生成 `_sidebar.md` 和 `README.md` 文件，大幅提升了文档管理效率。对于维护大量文档或频繁更新菜单的用户来说，该工具能显著减少重复劳动，让内容创作更专注于文档本身而非繁琐的配置工作。开源在 GitHub 上，欢迎使用和贡献。
