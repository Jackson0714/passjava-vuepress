---
title: 本地打包部署网站
date: 2025-11-11
---

```

npm run docs:build

tar -czf dist.tar.gz dist/

scp -i /Users/wukong/01.PassJava/passjava dist.tar.gz 服务器地址:~

ssh -i /Users/wukong/01.PassJava/passjava 服务器地址 "mkdir -p /部署目录 && mv  ~/dist.tar.gz /部署目录 && cd /部署目录 && tar -xzf dist.tar.gz && echo '文件已成功移动并解压'"
```
