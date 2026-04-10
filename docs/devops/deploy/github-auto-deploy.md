---
title: GitHub Actions + SSH  部署网站
date: 2026-04-07
---

你好，我是悟空。

## 背景

之前通过以下方式更新网站的静态页面：

- Jenkins 打包部署到远程服务器。需要多点几步。
- 本地命令行上传到远程服务器。缺点：还需要多执行一步。
- 调用 MCP 服务上传到远程服务器。缺点：mcp 服务不稳定，有时候成功， 有时候不成功。
- 登录远程服务器，获取最新代码，执行打包命令。缺点：依赖 node 环境，下载 npm 依赖包总是失败，编译报错。

有没有更好的方式呢？Github Action 就能解决问题。

### GitHub Action 工作原理

首先上传代码到 GitHub，然后 GitHub 检测到代码提交后，github action 功能就会启动 JOB，执行代码仓库中的 workflow 脚本中配置的步骤。

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

**在服务器上生成部署专用密钥**（如果还没有）：

```bash
# 生成密钥对（一路回车即可）
$ ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/github-deploy
```

添加密钥到 authorized_keys

```SH
$ sudo sh -c 'cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys'
```

获取密钥，后续会添加到 github 的action 变量中。

```SH
sudo cat ~/.ssh/github_actions
```

![](http://cdn.passjava.cn/uPic/image-20260408222850468U1EgUl.png)

## 在 GitHub 仓库中配置 Secrets

进入你的 GitHub 仓库：**Settings → Secrets and variables → Actions**

![image-20260403091104245](http://cdn.passjava.cn/uPic/image-20260403091104245r9QSAbtIiI0f.png)

添加以下 repository secrets：

| Secret 名称       | 值             | 获取方式                                 |
| :---------------- | :------------- | :--------------------------------------- |
| `SERVER_IP`       | `你的服务器IP` | 你的 Ubuntu 服务器公网 IP                |
| `SSH_USER`        | `ubuntu`       | 固定值                                   |
| `SSH_PRIVATE_KEY` | 私钥完整内容   | `cat ~/.ssh/github_actions` 复制全部内容 |

**如何获取私钥内容**：

```
cat ~/.ssh/github-deploy
# 复制从 -----BEGIN OPENSSH PRIVATE KEY----- 到结尾的所有内容
```

添加三个密钥后如下图所示：

![](http://cdn.passjava.cn/uPic/image-20260408223845293JRIiJl.png)

## 创建工作流文件

在你的项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Build and Deploy Docs

on:
  push:
    branches: [main] # 当推送到 main 分支时触发

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      # 1. 拉取代码
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. 设置 Node.js 环境
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "22" # 根据你的项目调整

      # 3. 缓存 npm 依赖（加速构建）
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      # 4. 安装依赖
      - name: Install dependencies
        run: npm install

      # 5. 构建静态网站
      - name: Build docs
        run: npm run docs:build

      # 6. 部署到 Ubuntu 服务器（使用 tar + scp）
      - uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: "${{ secrets.SSH_PRIVATE_KEY }}"

      - name: Deploy to Ubuntu Server
        uses: easingthemes/ssh-deploy@main # 第三方SSH部署插件
        env:
          SSH_PRIVATE_KEY: "${{ secrets.SSH_PRIVATE_KEY }}" # 从仓库密钥读取私钥
          REMOTE_HOST: "${{ secrets.SERVER_IP }}" # 服务器公网IP或域名
          REMOTE_USER: "${{ secrets.SSH_USER }}"
          SOURCE: "dist/"
          TARGET: "/nfs-data/passjava/passjava-learning/dist" # 服务器目标目录
          ARGS: "-avz --delete" # rsync参数：归档模式，并压缩，并删除多余文件
```

> **参数说明**：
>
> - `--delete`：删除服务器上本地没有的文件（保持完全同步）
> - 如果不希望删除服务器上的额外文件，去掉 `--delete` 参数

ssh-deploy 插件使用的 rsync 工具进行同步，rsync 的同步策略对比如下。

### rsync不同同步策略对比

| 需求                         | 命令                             | 行为                                             |
| :--------------------------- | :------------------------------- | :----------------------------------------------- |
| **只新增和更新**（你的需求） | `rsync -avz`                     | 源 → 目标：新增+更新 目标端多余文件：**保留**    |
| **完全镜像**                 | `rsync -avz --delete`            | 源 → 目标：新增+更新 目标端多余文件：**删除**    |
| **只新增（不覆盖）**         | `rsync -avz --ignore-existing`   | 源 → 目标：只新增 已存在的文件：**不覆盖**       |
| **只更新（不新增）**         | `rsync -avz --existing --update` | 源 → 目标：只更新已存在的文件 新文件：**不同步** |

github action 执行如下：

![](http://cdn.passjava.cn/uPic/image-20260409133005231VbpCSI.png)

查看一个 action 的详情如下：

![image-20260409133332362](http://cdn.passjava.cn/uPic/image-20260409133332362J7xCav.png)
