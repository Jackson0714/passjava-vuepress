---
title: 劫持 Typora 的图片请求、不影响浏览器正常访问
date: 2025-08-09
---

---

下面用一句话总结，再展开成 4 个关键步骤，让你一眼看懂「为什么 Typora 不改路径就能绕过七牛云的空 Referer 限制」。

## 一句话原理

**把 Typora 的 HTTP 请求先拉到本地 Nginx，由 Nginx 代填 Referer 后再转给七牛云，浏览器则继续直连，互不影响。**

## 4 步拆解

| 步骤         | 动作                                                              | 作用                   |
| ------------ | ----------------------------------------------------------------- | ---------------------- |
| ① 本地监听   | Nginx 启动在 `127.0.0.1:8888`                                     | 成为 Typora 的“中转站” |
| ② 进程劫持   | Proxifier 把 **Typora.exe** 的所有 `我的cdn域名:80` 流量指向 8888 | 只改进程，不改系统     |
| ③ 补 Referer | Nginx `proxy_set_header Referer http://<我的网站>;`               | 七牛云验证通过         |
| ④ 原路返回   | Nginx 把图片回给 Typora                                           | 图片正常显示           |

---

## 示意流程图

```
Typora ──(http://cdn域名/xxx.png)──► 127.0.0.1:8888
               ↑(Proxifier 劫持)
               │
           Nginx 代填 Referer
               │
               ▼
       七牛云收到带 Referer 的请求 → 返回图片
```

---

## 关键点

- **只劫持 Typora 进程**：浏览器仍直连七牛云，无冲突。
- **不改图片 URL**：Typora 里还是写 `http://cdn.passjava.cn/…`，路径零改动。
- **零成本**：Nginx 绿色版 + Proxifier 免费规则即可。

## ✅ 终极方案：Typora 专用代理（不改系统 hosts，不改图片路径）

### 🎯 核心思路

- **不改系统 hosts**（避免影响浏览器）。
- **不改图片路径**（Typora 里还是 `https://your-domain.com/xxx.jpg`）。
- **Typora 走代理，浏览器走直连**。

---

## 🛠️ 具体操作（Windows/macOS/Linux 通用）

### ① 安装本地代理工具

用 [Proxifier](https://www.proxifier.com)（Windows/macOS）或 [Clash](https://github.com/Dreamacro/clash)（跨平台）即可实现**按进程代理**。

这里用 **Proxifier** 举例（最简单）：

### ② 启动 Nginx 本地代理（监听 127.0.0.1:8888）

新建 `nginx.conf`：

```nginx
server {
    listen 127.0.0.1:8888;

    location / {
        proxy_pass https://your-domain.com;
        proxy_set_header Referer "https://your-allowed-referer.com";
    }
}
```

![](http://cdn.passjava.cn/uPic/image-20250809232539681PsdUQC.png)

重新加载配置

```bash
sudo nginx -s reload
```

### ③ 用 Proxifier 强制 Typora 走代理

1. 打开 Proxifier → `Profile` → `Proxy Servers` → 添加：
   - **Address**: `127.0.0.1`
   - **Port**: `8888`
   - **Type**: HTTP

![image-20250809233044417](http://cdn.passjava.cn/uPic/image-20250809233044417gGXhA4BtkEFj.png)

1. 新建 `Proxy Rules`：
   - **Applications**: 填 Typora 的路径（如 `C:\Program Files\Typora\Typora.exe`）
   - **Target hosts**: `your-domain.com`
   - **Action**: 选择刚才的代理服务器

![image-20250809233108439](http://cdn.passjava.cn/uPic/image-20250809233108439BH8AET.png)

### ✅ 效果

- **Typora** 访问 `https://your-domain.com/image.jpg` → 自动走 127.0.0.1:8888 → 加 Referer → 正常显示。
- **浏览器** 访问 `https://your-domain.com/image.jpg` → 直连七牛云 → 不受影响。

---

## 🚀 一键脚本（可选）

如果你不想手动配置，我可以帮你打包一个：

- Windows：一键启动的 Nginx + Proxifier 配置
- macOS：一键启动的 Nginx + Clash 配置

告诉我你的系统，我帮你写好。

参考：

https://www.cnblogs.com/liyiran/p/5166155.html

https://macked.app/proxifier.html
