---
title: 用 OpenClaw 做一个喝水提醒网站
date: 2026-04-20
---

# 用 OpenClaw 做一个喝水提醒网站

> 从一句"我需要喝水提醒"开始，到一个完整的前后端分离网站上线，只用了半天。

![](http://cdn.passjava.cn/uPic/image-202604202218357530E7WmG.png)

## 缘起：被提醒喝水的日常

那天我随口跟 OpenClaw 提了一句："我每天需要喝水提醒。"没想到这句话成了一切的起点。

我告诉它我的目标是每天喝 2000ml 水，它立刻给我写了一个 Python 脚本，用定时任务来实现每小时提醒。数据存储在本地 JSON 文件里，简单直接。

但很快问题就来了：JSON 文件跨天后数据就丢了，历史记录没法积累，更别说看周报了。

"换成pgsql存储吧。"我丢了一句话过去。

![](http://cdn.passjava.cn/uPic/image-20260420220350715YM8oYC.png)

## 选型：前后端分离的完整架构

当我提出"做一个更强大更完整的服务，前端用 Vue，后端用 Rust，单体应用就行，Vue 页面需要登录，接口有权限校验"的时候，OpenClaw 没有说"这很复杂"，而是直接开始规划。

它给出的架构是这样的：

```
water-service/
├── backend/          # Rust (Axum + SQLx + JWT)
├── frontend/         # Vue 3 + Vite + Element Plus
└── docker-compose.yml
```

接口设计也很清晰：

| 接口                | 方法 | 说明       | 权限   |
| ------------------- | ---- | ---------- | ------ |
| `/api/auth/login`   | POST | 登录       | 公开   |
| `/api/water/add`    | POST | 记录喝水量 | 需登录 |
| `/api/water/status` | GET  | 今日状态   | 需登录 |
| `/api/water/report` | GET  | 今日报告   | 需登录 |
| `/api/water/weekly` | GET  | 周报       | 需登录 |

数据库用的是 PostgreSQL，用户 `water` / 密码 `water123`，三张表：`water_log`（明细）、`water_daily`（每日汇总）、`water_settings`（设置）。

![](http://cdn.passjava.cn/uPic/image-20260420220553295k5zLkR.png)

## 第一个坑：时区显示差了8小时

跑起来之后，明细里显示的时间是 `02:57`，但实际应该是 `10:57`，差了整整 8 小时。

原因是存的虽然是 UTC 时间，但显示时直接用了 UTC，没有转成上海时区。

![image-20260420221716013](http://cdn.passjava.cn/uPic/image-20260420221716013JVNDWS.png)

## 第四个坑：502 错误

502 错误：

![](http://cdn.passjava.cn/uPic/image-20260420220635086wMnioKkAd19O.png)

## 细节优化1：午休免打扰设置

中午午休时免打扰设置：

![](http://cdn.passjava.cn/uPic/image-20260420221950282uLkBeg.png)

## 细节优化2：添加喝水记录后，刷新今日明细数据

![](http://cdn.passjava.cn/uPic/image-202604202221459983aOCis.png)

## 部署：从本地到域名

直接让 openclaw 修改 nginx 配置：

![](http://cdn.passjava.cn/uPic/image-202604202222350961aheJu.png)

### 原理

前端构建完之后，用一个简单的 Node.js 脚本做静态文件服务，监听 8029 端口，通过 nginx 反向代理到域名 `water.passjava.cn`。

nginx 配置也很简洁：

```nginx
server {
    listen 80;
    server_name water.passjava.cn;
    location / {
        proxy_pass http://127.0.0.1:8029;
    }
}
```

## 添加域名解析

登录阿里云，添加域名解析记录，步骤如下：

在域名解析里添加一条 A 记录：
类型：A
主机记录：water
记录值：你的服务器IP
配好后直接访问 http://water.passjava.cn 就能用了

## 总结

从最初的 Python 脚本，到完整的 Vue + Rust 网站，中间经历了很多：

1. **架构升级**：从单文件脚本到前后端分离
2. **数据库迁移**：从 JSON 到 PostgreSQL
3. **依赖地狱**：Rust 版本、crate 版本兼容性
4. **数据迁移**：字段类型重建、权限修复
5. **时区处理**：UTC 存储、本地时间显示
6. **运维部署**：进程管理、nginx 反向代理
7. **产品细节**：即时刷新、免打扰时段

整个过程最大的感触是：**好的 AI 协作不是一蹴而就，而是不断试错、不断调整**。OpenClaw 遇到问题不会卡住，它会尝试不同的方案，直到跑通为止。而作为用户，我只需要表达需求，剩下的它来搞定。

现在网站已经上线运行，喝水数据一目了然，周报自动生成，还有午休免打扰——从一个简单需求，生长出了一个完整的产品。

---

_如果你也有类似的需求，不妨试试和 AI 一起做。从一句话开始，也许会得到超出预期的东西。_
