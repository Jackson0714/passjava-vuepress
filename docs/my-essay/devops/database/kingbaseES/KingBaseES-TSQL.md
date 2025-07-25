---
title: 【金仓数据库产品体验官】金仓数据库 SQL Server 兼容版 T-SQL 测试篇
date: 2025-07-25
---

你好，我是悟空。

很荣幸受邀作为金仓数据库产品体验官。前几天还获得了金仓社区的奖品。

![](http://cdn.jayh.club/uPic/image-20250725102911091fN3Eu6.png)

本篇将会介绍金仓数据库 SQL Server 兼容版 T-SQL 的基本测试情况。

## 一、测试说明

KES数据库已经兼容了 SQL Server，如在 SQL 特殊数据类型与对象，SQL 语句，T-SQL 语法、存储过程调用的兼容性上都很高。

本次我们就来测试常见的 T-SQL 语法的兼容性：

- 批处理语句 GO
- 打印语句 PRINT
- 错误处理语句 RAISEERROR
- THROW
- SQL 语法特性，分号和逗号

## 二、下载并安装SQL Server 兼容版KES数据库

### 下载地址

https://www.kingbase.com.cn/download.html

![img](http://cdn.jayh.club/uPic/1753345189081-fb6cf05e-69b2-46b3-b5fd-bebc1732530daTTGYJq4KEnv.png)

该版本新增了对SQLServer若干系统视图和内置函数的支持，支持ICU库并对其进行了优化；支持更多的高级查询功能，包括FOR XML子句、PIVOT行列转换操作、GROUP BY子句中基于不同数据类型进行分组、DINSTICT子句与ORDER BY联合中列别名的使用等；新增DML操作触发更新统计信息功能，提升查询性能与增强系统的稳定性；新增临时表优化功能，提升了函数执行效率。在客户端编程接口方面，.Net驱动中新增了对SQL Server 中一些日期函数的支持，加入了更多针对各行业应用场景的定制化功能，助力企业实现平滑迁移和业务高效运行。

### 下载授权文件

KingbaseES数据库(SQLServer兼容版)授权文件时长限制为90天，以数据库首次启动为首日开始计算。

![img](http://cdn.jayh.club/uPic/1753345227839-4adb128a-ae61-41d6-abd3-4a5fc5d5005axFAPEEGFIGWn.png)

## 三、兼容性测试 SQL Server T-SQL 语句

### 3.1、批处理语句

#### 1. 含义

批处理语句是指将多条 T-SQL 语句组合在一起，作为一个整体执行。SQL Server 支持通过分号（`;`）分隔多条语句，或者使用 `GO` 关键字分隔批处理。

#### 2. 语法

- **使用分号分隔**

```sql
SELECT * FROM Table1;
SELECT * FROM Table2;
```

- **使用** `GO` **分隔**

```sql
SELECT * FROM Table1;
GO
SELECT * FROM Table2;
GO
```

#### 3. 注意事项

- **分号**：在 SQL Server 中，分号是语句的结束符，但在某些情况下（如使用 `TRY...CATCH` 或 `BEGIN...END` 块）是必需的。
- `GO` **关键字**：`GO` 不是 T-SQL 的语法，而是 SQL Server Management Studio (SSMS) 和 SQLCMD 工具的批处理分隔符。它不能在存储过程或函数中使用。
- **性能**：将多条语句组合成一个批处理可以减少网络往返时间，提高性能。

#### 4. 实操

##### 示例 1：使用分号分隔

```sql
SELECT * FROM Table1;
SELECT * FROM Table2;
```

![img](http://cdn.jayh.club/uPic/1753343633798-069c2372-9320-4536-ba5a-e50de4bc6046j2YvodKST6Bl.png)

##### 示例 2：使用 `GO` 分隔

```sql
SELECT * FROM Table1;
GO
SELECT * FROM Table2;
GO
```

![img](http://cdn.jayh.club/uPic/1753343687067-c16ee946-29de-4f1e-aed0-dc00c9daca03vT9pSNAnVXqd.png)

![img](http://cdn.jayh.club/uPic/1753343668842-0a24e2ad-72a4-457b-b87b-539015822078TPN1F39mHnqW.png)

### 3.2、`PRINT` 语句

#### 1. 含义

`PRINT` 语句用于在 SQL Server 的消息窗口中输出文本信息。它常用于调试和日志记录。

#### 2. 语法

```sql
PRINT 'message';
```

- `message`：要输出的字符串，可以是常量、变量或表达式。

#### 3. 注意事项

- **输出限制**：`PRINT` 输出的最大长度为 8000 字符。
- **性能**：`PRINT` 语句不会影响查询的执行，但过多的 `PRINT` 语句可能会影响性能。
- **调试工具**：在实际生产环境中，建议使用更专业的日志记录工具（如 SQL Server 的 `ERRORLOG` 或自定义的日志表）。

#### 4. 实操

##### 示例 1：打印常量字符串

```sql
PRINT 'Hello, World!';
```

![img](http://cdn.jayh.club/uPic/1753343791993-736ea03c-d94b-453c-8d4a-8f6d5db28efazna5zITHalzq.png)

##### 示例 2：打印变量值

```sql
DECLARE @Message NVARCHAR(100) = 'This is a test message.';
PRINT @Message;
```

![img](http://cdn.jayh.club/uPic/1753343844661-8df36ff3-3c62-49f7-892c-82ba61498c758nwsIPsHkOnp.png)

### 3.3、`RAISERROR` 语句

#### 1. 含义

`RAISERROR` 语句用于生成错误消息，并将控制权传递给 `CATCH` 块（如果存在）。它常用于自定义错误处理。

#### 2. 语法

```sql
RAISERROR ( { msg_id | msg_str } , severity , state [ , argument [ ,...n ] ] );
```

- `msg_id`：用户定义的错误消息编号。
- `msg_str`：自定义错误消息。
- `severity`：错误的严重级别（0-25）。
- `state`：错误的状态码（0-255）。
- `argument`：可选的参数，用于替换消息中的占位符。

#### 3. 注意事项

- **严重级别**：严重级别为 11-19 的错误会触发 `CATCH` 块。
- **性能**：`RAISERROR` 会中断当前的执行流程，因此应谨慎使用。
- **替代**：在 SQL Server 2012 及更高版本中，建议使用 `THROW` 语句替代 `RAISERROR`。

### 4. 实操

#### 示例 1：使用 `RAISERROR` 抛出自定义错误

```sql
BEGIN TRY
    RAISERROR ('This is a custom error message.', 16, 1);
END TRY
BEGIN CATCH
    PRINT 'Error caught: ' + ERROR_MESSAGE();
END CATCH;
```

![img](http://cdn.jayh.club/uPic/1753343938312-939b9e8a-1eff-4d4d-b43e-311256efbea40mPSKyGRm95W.png)

### 3.4、`THROW` 语句

#### 1. 含义

`THROW` 语句用于抛出错误，并将控制权传递给 `CATCH` 块（如果存在）。它是 `RAISERROR` 的替代品，语法更简洁。

#### 2. 语法

```sql
THROW [error_number ,message ,state];
```

- `error_number`：错误编号（可选，默认为 50000）。
- `message`：自定义错误消息。
- `state`：错误的状态码（可选，默认为 1）。

#### 3. 注意事项

- **兼容性**：`THROW` 语句仅在 SQL Server 2012 及更高版本中可用。
- **性能**：与 `RAISERROR` 类似，`THROW` 会中断当前的执行流程。
- **使用场景**：建议在需要抛出自定义错误时使用 `THROW`，而不是 `RAISERROR`。

#### 4. 实操

##### 示例 1：使用 `THROW` 抛出自定义错误

```sql
BEGIN TRY
    THROW 50001, 'This is a custom error message.', 1;
END TRY
BEGIN CATCH
    PRINT 'Error caught: ' + ERROR_MESSAGE();
END CATCH;
```

![img](http://cdn.jayh.club/uPic/1753343953298-3785a308-7e4c-40b9-a44d-062516ca466bxZnUS3a6hPud.png)

### 3.5、SQL 语句无需分号分隔符

#### 1. 含义

在 SQL Server 中，分号（`;`）是语句的结束符

#### 2. 测试

```plain
BEGIN TRY
    SELECT * FROM Table1
    SELECT * FROM Table2
END TRY
BEGIN CATCH
    PRINT 'Error occurred';
END CATCH;
```

![img](http://cdn.jayh.club/uPic/1753344759724-01d1799b-6497-4fba-9a69-de5e40f8986f7xg6lc7SRIoM.png)

### 3.6 创建表时最后一个字段可加逗号

#### 1. 含义

在 SQL Server 中，创建表时，最后一个字段后面可以加逗号，这在某些情况下可以简化代码的维护和扩展。

#### 2. 语法

- **最后一个字段加逗号**：

```sql
CREATE TABLE ExampleTable (
    ID INT PRIMARY KEY,
    Data NVARCHAR(100),
    RowVer ROWVERSION,
);
```

- **最后一个字段不加逗号**：

```sql
CREATE TABLE ExampleTable (
    ID INT PRIMARY KEY,
    Data NVARCHAR(100),
    RowVer ROWVERSION
);
```

#### 3. 注意事项

- **语法兼容性**：在 SQL Server 中，最后一个字段加逗号是允许的，但在某些其他数据库管理系统（如 MySQL）中，这种语法可能不被支持。
- **代码维护**：在团队开发中，统一的代码风格很重要。如果团队决定在最后一个字段加逗号，那么所有表的定义都应保持一致。
- **性能影响**：这种语法对性能没有影响，但可以提高代码的可读性和可维护性。

#### 4. 实操

#### 示例 1：最后一个字段加逗号

```sql
CREATE TABLE ExampleTable (
    ID INT PRIMARY KEY,
    Data NVARCHAR(100),
    RowVer ROWVERSION,
);
```

![img](http://cdn.jayh.club/uPic/1753344961777-96589da0-c580-4d68-933e-15b1310c455cCsJsTUi5WhMH.png)

#### 示例 2：最后一个字段不加逗号

```sql
CREATE TABLE ExampleTable (
    ID INT PRIMARY KEY,
    Data NVARCHAR(100),
    RowVer ROWVERSION
);
```

![img](http://cdn.jayh.club/uPic/1753344978196-5c54f03f-b673-4b69-b6e0-29f8a756e29cWB9GtE69gT0I.png)

### 总结

工具语句：

- **批处理语句**：用于组合多条 T-SQL 语句，提高执行效率。
- `PRINT` **语句**：用于调试和输出信息，但不适合生产环境。
- `RAISERROR` **语句**：用于自定义错误处理，但在 SQL Server 2012 及更高版本中建议使用 `THROW`。
- `THROW` **语句**：语法更简洁，是 `RAISERROR` 的替代品，适用于 SQL Server 2012 及更高版本。

这些工具语句在 SQL Server 的开发和调试中非常有用，合理使用它们可以提高代码的可读性和可维护性。

语法特性：

- SQL 语句无需分号分隔符
- 创建表时最后一个字段可加逗号：

通过合理使用这些特性，可以提高 SQL Server 的开发效率和代码的可维护性。

## 五、Windows 安装 KingBaseES 报错汇总

### 1、安装软件时，提示初始化数据库失败

#### 解决方案

需要把360安全软件关闭后再执行下一步。

### 2、无法启动服务

打开服务 services.msc，找到可执行文件的路径。

![img](http://cdn.jayh.club/uPic/1753338549263-2057c0e6-6355-4454-a732-06e1e6768057xUc95bSrNkVo.png)

```sh
cd D:\Program Files\Kingbase\ES\V9\KESRealPro\V009R004C012\Server\bin
./sys_ctl.exe runservice -N "kingbase9_R1_instance" -D "D:\Program Files\Kingbase\ES\V9\data" -w

sys_ctl: could not start service "kingbase9_R1_instance": error code 1063

./sys_ctl.exe -D "kingbase9_R1_instance" -D "D:\Program Files\Kingbase\ES\V9\data" start

waiting for server to start.....
 HKT [18240] LOG:  正在启动 KingbaseES V009R004C012
 HKT [18240] LOG:  正在监听IPv6地址"::"，端口 54321
 HKT [18240] LOG:  无法绑定IPv4地址"0.0.0.0": Only one usage of each socket address (protocol/network address/port) is normally permitted.

 HKT [18240] HINT:  端口54321上是否已经运行了另一个kingbase?如果没有，请等待几秒钟后重试。
 HKT [18240] FATAL:  无法为"*"创建监听套接字
 HKT [18240] LOG:  database system is shut down
 stopped waiting
sys_ctl: could not start server
Examine the log output.
```

#### 解决方案

方案 1：查看端口是否被占用

```plain
netstat -ano | grep "54321"
kill <进程 id>
```

方案 2：更改启动端口

```plain
D:\Program Files\Kingbase\ES\V9\data
port=54325
```

重新启动，启动成功，如下图所示：

![image-20250724201706850](http://cdn.jayh.club/uPic/image-20250724201706850BjV1gO.png)

查看进程

![img](http://cdn.jayh.club/uPic/1753341920964-181a2ee3-0ab8-407b-b37f-11e344637c5fbqzTFfOx3DzY.png)

修改数据库连接的端口为 54325，连接成功，如下图所示：

![img](http://cdn.jayh.club/uPic/1753342078542-496bd056-3c1b-49b8-b191-a03a18885e6bVTNMQvqXQ3EN.png)

### 3、无法连接数据库，报错乱码

#### 解决方案

安装时选择 utf8 编码
