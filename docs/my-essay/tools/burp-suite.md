---
title: 安装和破解 burp suite
date: 2025-03-26
---

## 下载地址

安装包

https://portswigger.net/burp/releases

破解文件

https://github.com/kx9bmy/burpsite

## 破解

- 在应用程序中找到burp，显示包内容，依次打开文件夹：./Contents/java/app（如果没有的话就是./Contents/Resources/app），然后就会看到我们熟悉的jar文件了
- 将启动器BurpLoaderKeygen.jar移动到当前app目录

![](http://cdn.jayh.club/uPic/image-20250326090542373V7K3d4.png)

- 返回到Contents目录，编辑vmoptions.txt，末尾追加内容

> --add-opens=java.base/java.lang=ALL-UNNAMED
> --add-opens=java.base/jdk.internal.org.objectweb.asm=ALL-UNNAMED
> --add-opens=java.base/jdk.internal.org.objectweb.asm.tree=ALL-UNNAMED
> --add-opens=java.base/jdk.internal.org.objectweb.asm.Opcodes=ALL-UNNAMED
> -javaagent:BurpLoaderKeygen.jar
> -noverify

- 保存，从启动台中运行app，然后启动注册机BurpLoaderKeygen.jar，用**老方法**生成激活码激活即可

只要注册算法不变，后续升级都可以直接用官网的安装包app覆盖安装，然后重新在vmoptions.txt中追加上面的代码文件就行，别的不用管

> 补充一下“老方法”：
> 1.从启动台中运行app，然后启动注册机BurpLoaderKeygen.jar，注册机上会显示license
> 2.把license填到app的页面以后，选中Manual register，进行手工注册，点击next
> 3.app页面上出现了request，把request的内容粘贴到注册机中，会在注册机中生成response
> 4.把注册机中的response，粘贴回app的页面，然后点击 next
> 5.提示注册成功

## 参考资料

https://www.lzskyline.com/index.php/archives/121/

https://www.freebuf.com/sectool/417321.html