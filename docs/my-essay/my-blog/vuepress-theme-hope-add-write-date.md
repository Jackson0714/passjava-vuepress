---
title: vuepress-theme-hope 主题添加文章写作日期
category: 博客优化
tag:
    - 博客优化
    - VuePress
date: 2024-08-30
---

## 背景

发布的文章没有显示发布的时间，此篇文章会介绍如何加上发布时间，效果如下图所示：

![](http://cdn.jayh.club/uPic/image-20240830171529963CMyH03.png)

## 操作步骤

[参考文章](https://theme-hope.vuejs.press/zh/guide/feature/page-info.html)

theme.ts 文件中配置 pageInfo

![](http://cdn.jayh.club/uPic/image-20240830171944369uFKuJE.png)

`pageInfo` 默认接受一个字符串数组，可以填入各条目名称，填入的顺序即是各条目显示的顺序。

条目可选的值和对应内容如下:

| 条目            | 对应内容     | 页面 frontmatter 值         | 主题设置的配置项           |
| --------------- | ------------ | --------------------------- | -------------------------- |
| `"Author"`      | 作者         | `author`                    | `author`                   |
| `"Date"`        | 写作日期     | `date`                      | N/A                        |
| `"Original"`    | 是否原创     | `isOriginal`                | N/A                        |
| `"Category"`    | 分类         | `category`                  | N/A                        |
| `"Tag"`         | 标签         | `tag`                       | N/A                        |
| `"ReadingTime"` | 预计阅读时间 | N/A(自动生成)               | N/A                        |
| `"Word"`        | 字数         | N/A(自动生成)               | N/A                        |
| `"PageView"`    | 访问量       | `pageview` (仅 Waline 可用) | `plugins.comment.pageview` |

默认会显示 “作者，访问量，写作日期，分类，标签，预计阅读时间”。

### 写作日期

建议 time 以标准格式输入日期，即 `xxxx-xx-xx` 的形式，如 “2020 年 4 月 1 日” 应当输入为 `2020-04-01`

例子:

在文章的开头添加以下内容

```
---
date: 2020-01-01
---
```