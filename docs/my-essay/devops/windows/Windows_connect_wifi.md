---
title: Windows 自动连接 wifi
---

## 背景

电脑总是自动断开连接 WIFI，未找到原因，于是写个脚本自动连接 WIFI。

## 命令行连接 WIFI

### 查看已保存的网络连接

netsh wlan show profiles
查看 WIFI
![Pasted image 20240708105258.png](http://cdn.jayh.club/uPic/202407191059987YmTEy8.png)

## 自动连接网络

netsh wlan connect name=HUAWEI_1729
![Pasted image 20240708105309.png](http://cdn.jayh.club/uPic/202407191059864nOD3PF.png)

在Windows操作系统中，可以使用批处理脚本（Batch Script）或PowerShell脚本来实现定期自动连接Wi-Fi网络的功能。以下是两种方法的示例：

### 方法1：使用批处理脚本

1. **打开记事本**，输入以下批处理命令：

   batch

   ```batch
   @echo off
   set profile=YourWiFiProfileName
   netsh wlan connect name=%profile%
   ```

   将 `YourWiFiProfileName` 替换为你的Wi-Fi网络配置文件名。

2. **保存文件**，命名为 `connectWifi.bat`。

3. **设置任务计划程序**（Task Scheduler）来定期运行这个批处理脚本：

   - 打开“任务计划程序”。
   - 创建新任务，设置触发器为“周期性”。
   - 在“操作”部分，选择“启动程序”，并指向你的 `connectWifi.bat` 文件。
   - 完成设置并保存任务。

### 方法2：使用PowerShell脚本

1. **打开记事本**，输入以下PowerShell命令：

   powershell

   ```powershell
   $profile = "YourWiFiProfileName"
   netsh wlan connect name=$profile
   ```

   将 `YourWiFiProfileName` 替换为你的Wi-Fi网络配置文件名。

2. **保存文件**，命名为 `connectWifi.ps1`。

3. **设置任务计划程序**（Task Scheduler）来定期运行这个PowerShell脚本：

   - 打开“任务计划程序”。
   - 创建新任务，设置触发器为“周期性”。
   - 在“操作”部分，选择“启动程序”，并指向 `powershell.exe`。
   - 添加参数 `-ExecutionPolicy Bypass -File "C:\path\to\connectWifi.ps1"`（将路径替换为你的脚本实际路径）。
   - 完成设置并保存任务。

## 示例

### bat 脚本

```SH
@echo off
set profile=HUAWEI_1729
netsh wlan connect name=%profile%
```

### powershell 脚本

```shell
# 使用 Invoke-Expression 执行 netsh 命令并捕获输出
$output = Invoke-Expression "netsh wlan show interface"

# 显示输出结果
#Write-Host $output

# 解析输出结果以获取特定信息
# 例如，查找 "Media Connect State" 的值
$mediaConnectState = Select-String -InputObject $output -Pattern 'HUAWEI_1729'

# 显示 "Media Connect State"
#Write-Host "Media Connect State: $mediaConnectState"

$profile='HUAWEI_1729'

# 检查Wi-Fi是否已连接
if ($mediaConnectState -eq '' -or $mediaConnectState -eq $null) {
    Write-Host "Wi-Fi is not connected. Attempting to connect..."


    # 连接到Wi-Fi网络
    netsh wlan connect name=$profile

    # 检查连接是否成功
    if ($wifi.InterfaceStatus -ne "Connected") {
        Write-Host "Successfully connected to $profile."
    } else {
        Write-Host "Failed to connect to $profile."
    }
} else {
    Write-Host "Wi-Fi is already connected."
}

# 显示提示信息并等待用户输入
#$userInput = Read-Host "Please enter something and press Enter"

# 输出用户输入的内容
#Write-Host "You entered: $userInput"
```

![image-20241224112410492](http://cdn.jayh.club/top/202412241124209.png)

![image-20241224112202149](http://cdn.jayh.club/top/202412241122290.png)

![image-20241224112232268](http://cdn.jayh.club/top/202412241122403.png)

![image-20241224112247490](http://cdn.jayh.club/top/202412241122789.png)

![image-20241224112258113](http://cdn.jayh.club/top/202412241123106.png)

![image-20241224112304851](http://cdn.jayh.club/top/202412241123176.png)

![image-20250311195517319](http://cdn.jayh.club/uPic/image-20250311195517319AARzGj.png)

set-ExecutionPolicy RemoteSigned

set-executionpolicy -executionpolicy unrestricted
