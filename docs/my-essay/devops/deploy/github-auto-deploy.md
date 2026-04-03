### 在 Ubuntu 服务器上准备目录

bash

```
# 确保目录存在并可写（ubuntu 用户有权限）
sudo mkdir -p /data/passjava/passjava-learning

# 将目录所有者改为 ubuntu 用户（这样就不需要 sudo 权限了）
sudo chown -R ubuntu:ubuntu /data/passjava/passjava-learning

# 验证权限
ls -la /data/passjava/
```

### 2️⃣ 配置 SSH 免密登录

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

### 3️⃣ 在 GitHub 仓库中配置 Secrets

进入你的 GitHub 仓库：**Settings → Secrets and variables → Actions**

![image-20260403091104245](http://cdn.passjava.cn/uPic/image-20260403091104245r9QSAbtIiI0f.png)

添加以下 secrets：

| Secret 名称       | 值             | 获取方式                                |
| :---------------- | :------------- | :-------------------------------------- |
| `SERVER_IP`       | `你的服务器IP` | 你的 Ubuntu 服务器公网 IP               |
| `SSH_USER`        | `ubuntu`       | 固定值                                  |
| `SSH_PRIVATE_KEY` | 私钥完整内容   | `cat ~/.ssh/github-deploy` 复制全部内容 |
