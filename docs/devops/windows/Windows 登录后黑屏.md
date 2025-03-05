
window 更新升级，导致 explorer.exe 文件丢失
解决方案：将explorer.exe下载下来拷贝到 C:Windows\explorer.exe

## 连接 WIFI 网络

### 查看已保存的网络连接
 netsh wlan show profiles
 查看 WIFI
![Pasted image 20240708105258.png](http://cdn.jayh.club/top/202407191059987.png)



### 连接网络
 netsh wlan connect name=HUAWEI_1729
 ![Pasted image 20240708105309.png](http://cdn.jayh.club/top/202407191059864.png)
 

## 将 explorer 下载保存到 C:Windows\explorer.exe


打开企业微信


保存文件到 D 盘，因为 C:\Windows\ 没有权限保存

拷贝 D:\explorer.exe 到  C:Windows\explorer.exe 
``` 
cp D:\explorer.exe C:\Windows\explorer.exe
```

![Pasted image 20240708105354.png](http://cdn.jayh.club/top/202407191059615.png)



## 启动 explorer.exe 
![](http://cdn.jayh.club/top/202407191100602.png)