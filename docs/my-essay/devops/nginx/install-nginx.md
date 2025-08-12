---
title: Mac 安装 Nginx
date: 2025-08-09
tag:
  - Nginx
---

**macOS（Intel & Apple Silicon）** 上从零到上线的一条龙配置流程，全部基于 **Homebrew**，可直接复制执行。

---

1. 安装 / 更新 Homebrew（如果已装可跳过）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

2. 安装 Nginx

```bash
brew update
brew install nginx
```

安装完 Homebrew 会提示 3 个关键路径，先记下来：

- 配置文件：`/opt/homebrew/etc/nginx/nginx.conf`（Apple Silicon）  
  或 `/usr/local/etc/nginx/nginx.conf`（Intel）
- 站点根目录：`/opt/homebrew/var/www` 或 `/usr/local/var/www`
- 日志目录：`/opt/homebrew/var/log/nginx/` 或 `/usr/local/var/log/nginx/`

---

3. 启动 Nginx 并设为开机自启

```bash
# 前台调试（先看能否跑起来）
nginx

# 正式作为服务运行
sudo brew services start nginx
```

浏览器访问 http://localhost:8080 出现 “Welcome to nginx” 即成功。

---

4. 修改端口到 80（可选）  
   macOS 自带 Apache 可能已占 80，先停掉：

```bash
sudo apachectl stop
```

编辑配置：

```bash
# Apple Silicon
nano /opt/homebrew/etc/nginx/nginx.conf
# Intel
nano /usr/local/etc/nginx/nginx.conf
```

把 `listen 8080` 改成 `listen 80`，保存后

```bash
sudo nginx -s reload
```

此时访问 http://localhost 即可。

---

5. 配置虚拟主机示例  
   在 `nginx.conf` 末尾 `http {}` 里加：

```nginx
server {
    listen 80;
    server_name  test.local;

    root   /opt/homebrew/var/www/test;   # Intel 换成 /usr/local/var/www/test
    index  index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

创建目录并写个首页：

```bash
mkdir -p /opt/homebrew/var/www/test
echo "<h1>Hello macOS Nginx</h1>" > /opt/homebrew/var/www/test/index.html
```

重载生效：

```bash
sudo nginx -s reload
```

把 `test.local` 写到 `/etc/hosts`：

```
127.0.0.1 test.local
```

浏览器访问 http://test.local 应可见 “Hello macOS Nginx”。

---

6. 常用管理命令速查

```bash
sudo brew services start nginx     # 启动
sudo brew services stop nginx      # 停止
sudo brew services restart nginx   # 重启
sudo nginx -t                      # 检查语法
sudo nginx -s reload               # 平滑重载
sudo nginx -s stop                 # 立即退出
```

---

7. 目录结构一览（Apple Silicon 为例）

```
/opt/homebrew/
├── etc/nginx/nginx.conf            # 主配置
├── etc/nginx/servers/              # 虚拟主机片段，*.conf 自动 include
├── var/www/                        # 网站根目录
└── var/log/nginx/                  # access.log & error.log
```

Intel 把 `/opt/homebrew` 换成 `/usr/local` 即可。

至此，macOS 上的 Nginx 已全部配置完毕并具备生产级可用性。

## 附录

brew install nginx

![image-20250809041929494](http://cdn.jayh.club/uPic/image-20250809041929494TmwdpG.png)

```SH
✘ wukong@wukongs-MacBook-Pro  ~/_workspace/excalidraw/excalidraw  ↰ master  sudo brew services start nginx
Error: Formula `nginx` is not installed.
 ✘ wukong@wukongs-MacBook-Pro  ~/_workspace/excalidraw/excalidraw  ↰ master  brew install nginx
==> Downloading https://formulae.brew.sh/api/formula.jws.json
==> Downloading https://formulae.brew.sh/api/cask.jws.json
==> Fetching downloads for: nginx
==> Fetching dependencies for nginx: ca-certificates and openssl@3
==> Fetching ca-certificates
==> Downloading https://mirrors.ustc.edu.cn/homebrew-bottles/bottles/ca-certificates-2025-07-15.all.bottle.2.tar.gz
########################################################################################################################### 100.0%
==> Fetching openssl@3
==> Downloading https://mirrors.ustc.edu.cn/homebrew-bottles/bottles/openssl%403-3.5.2.arm64_ventura.bottle.tar.gz
########################################################################################################################### 100.0%
==> Fetching nginx
==> Downloading https://mirrors.ustc.edu.cn/homebrew-bottles/bottles/nginx-1.29.0.arm64_ventura.bottle.tar.gz
########################################################################################################################### 100.0%
==> Installing dependencies for nginx: ca-certificates and openssl@3
==> Installing nginx dependency: ca-certificates
==> Pouring ca-certificates-2025-07-15.all.bottle.2.tar.gz
==> Regenerating CA certificate bundle from keychain, this may take a while...
🍺  /opt/homebrew/Cellar/ca-certificates/2025-07-15: 4 files, 227.8KB
==> Installing nginx dependency: openssl@3
==> Pouring openssl@3-3.5.2.arm64_ventura.bottle.tar.gz
🍺  /opt/homebrew/Cellar/openssl@3/3.5.2: 7,563 files, 35.4MB
==> Installing nginx
==> Pouring nginx-1.29.0.arm64_ventura.bottle.tar.gz
==> Caveats
Docroot is: /opt/homebrew/var/www

The default port has been set in /opt/homebrew/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /opt/homebrew/etc/nginx/servers/.

To start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/nginx/bin/nginx -g daemon\ off\;
==> Summary
🍺  /opt/homebrew/Cellar/nginx/1.29.0: 27 files, 2.5MB
==> Running `brew cleanup nginx`...
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> No outdated dependents to upgrade!
==> Caveats
==> nginx
Docroot is: /opt/homebrew/var/www

The default port has been set in /opt/homebrew/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /opt/homebrew/etc/nginx/servers/.

To start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/nginx/bin/nginx -g daemon\ off\;
 wukong@wukongs-MacBook-Pro  ~/_workspace/excalidraw/excalidraw  ↰ master  nginx
```
