# 升级 node

下载node
https://nodejs.org/zh-cn/about/previous-releases

拷贝到 /usr/local/node$
tar -Jxf node-v16.20.2-linux-x64.tar.xz

编辑环境变量
sudo vim /etc/profile
export NODE_HOME=/usr/local/node/node-v16.20.2-linux-x64
export PATH=$NODE_HOME/bin:$PATH
export NODE_PATH=$NODE_HOME/lib/node_modules

$ source /etc/profile
$ node -v

## 方式二

https://www.cnblogs.com/jackson0714/p/node.html

### 安装 nvm

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

报错：
fatal: unable to access 'https://github.com/nvm-sh/nvm.git/': gnutls_handshake() failed: The TLS connection was non-properly terminated.
Failed to clone nvm repo. Please report this!
解决方案

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash

报错：
fatal: unable to access 'https://github.com/nvm-sh/nvm.git/': Failed to connect to github.com port 443: Connection timed out
Failed to clone nvm repo. Please report this!

取消全局代理：
git config --global --unset http.https://github.com.proxy
git config --global --unset http.https://github.com.proxy
git config --global --unset http.proxy
git config --global --unset https.proxy

![安装 nvm](http://cdn.passjava.cn/uPic/image-20240819092210314iQ9bA1.png)

![nvm 立即生效](http://cdn.passjava.cn/uPic/image-202408190942403102Pdzo3.png)

### 升级

n stablecurl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
