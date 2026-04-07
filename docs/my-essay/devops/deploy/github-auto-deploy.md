---
title: GitHub Actions + SSH  部署网站
date: 2026-04-07
---

## 在 Ubuntu 服务器上准备目录

```bash
# 确保目录存在并可写（ubuntu 用户有权限）
sudo mkdir -p /data/passjava/passjava-learning

# 将目录所有者改为 ubuntu 用户（这样就不需要 sudo 权限了）
sudo chown -R ubuntu:ubuntu /data/passjava/passjava-learning

# 验证权限
ls -la /data/passjava/
```

## 配置 SSH 免密登录

**在你的本地电脑上生成部署专用密钥**（如果还没有）：

```bash
# 生成密钥对（一路回车即可）
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/github-deploy
```

**将公钥添加到 Ubuntu 服务器**：

```bash
# 1. 查看公钥内容
cat ~/.ssh/github-deploy.pub

# 2. SSH 登录到你的服务器
ssh ubuntu@你的服务器IP

# 3. 在服务器上执行以下命令
mkdir -p ~/.ssh
echo "这里粘贴公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh

# 4. 退出服务器
exit
```

**测试免密登录**：

```sh
ssh -i ~/.ssh/github-deploy ubuntu@你的服务器IP
# 应该直接登录成功，不需要输入密码
```

![](http://cdn.passjava.cn/uPic/image-20260403091347275SndM23.png)

## 在 GitHub 仓库中配置 Secrets

进入你的 GitHub 仓库：**Settings → Secrets and variables → Actions**

![image-20260403091104245](http://cdn.passjava.cn/uPic/image-20260403091104245r9QSAbtIiI0f.png)

添加以下 secrets：

| Secret 名称       | 值             | 获取方式                                |
| :---------------- | :------------- | :-------------------------------------- |
| `SERVER_IP`       | `你的服务器IP` | 你的 Ubuntu 服务器公网 IP               |
| `SSH_USER`        | `ubuntu`       | 固定值                                  |
| `SSH_PRIVATE_KEY` | 私钥完整内容   | `cat ~/.ssh/github-deploy` 复制全部内容 |

**如何获取私钥内容**：

bash

```
cat ~/.ssh/github-deploy
# 复制从 -----BEGIN OPENSSH PRIVATE KEY----- 到结尾的所有内容
```

## 创建工作流文件

在你的项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Build and Deploy Docs

on:
  push:
    branches: [main] # 当推送到 main 分支时触发

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest # 使用 GitHub 官方 Ubuntu 环境

    steps:
      # 1. 拉取代码
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. 设置 Node.js 环境
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18" # 根据你的项目需要调整

      # 3. 安装依赖
      - name: Install dependencies
        run: npm ci # 使用 package-lock.json 精确安装

      # 4. 构建静态网站
      - name: Build docs
        run: npm run docs:build

      # 5. 同步到 Ubuntu 服务器
      - name: Deploy to Ubuntu Server
        uses: easingthemes/ssh-deploy@main
        env:
          SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
          ARGS: "-rlgoDzvc -i --delete" # 参数说明见下方
          SOURCE: "dist/" # 要上传的目录
          REMOTE_HOST: ${{ secrets.SERVER_IP }}
          REMOTE_USER: ${{ secrets.SSH_USER }}
          TARGET: "/var/www/my-docs/" # 服务器上的目标目录
          EXCLUDE: "/node_modules/, /.git/" # 排除不需要的文件
```

> **参数说明**：
>
> - `--delete`：删除服务器上本地没有的文件（保持完全同步）
> - 如果不希望删除服务器上的额外文件，去掉 `--delete` 参数
