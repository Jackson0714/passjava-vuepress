---
title: 生产环境 MySQL 8.0 LATERAL 实战：3s 慢查询优化到 0.8s 的完整过程
date: 2026-05-11
---

![mysql_lateral封面](http://cdn.passjava.cn/uPic/mysql_lateral1VRC9Qf.png)

你好，我是悟空。

今天又排查了一个 MySQL 慢查询的问题，接下来讲解下该 SQL 的问题和解决方案。

![SQL优化：从3秒到0.8秒](http://cdn.passjava.cn/uPic/mysql%20lateralcJH6XO.png)

## 一、问题

### 1.1 问题描述

通过监控慢查询，可以看到最近1小时内执行了 700多次查询，平均执行时间 2s。

![](http://cdn.passjava.cn/uPic/202605131437441YVIinz.png)

SQL语句如下：

```SQL
select
  overdue_amount
from
  cont_execute exe
  left join (
    SELECT
      cont_number,
      is_important_cont,
      is_important_cont_in,
      ROW_NUMBER() OVER (
        PARTITION BY
          cont_number
        ORDER BY
          create_time DESC
      ) AS rn
    FROM
      cont_review_main
    WHERE
      del_flag = 0
  ) main on exe.cont_number = main.cont_number
where
  exe.del_flag = 0
  and main.rn = 1
  and main.is_important_cont_in = 0
  and exe.cont_company_name = 'xx科技有限公司'

```

**该监控工具没有给出实质性的优化建议，如下图所示，删除冗余索引，改写建议都无法提升 SQL的查询性能。**

![](http://cdn.passjava.cn/uPic/202605131031864mimn5K.png)

### 1.2 分析执行计划

![](http://cdn.passjava.cn/uPic/202605131002408zwc6oQ.png)

| 步骤    | 表                 | 类型 | 行数       | 问题                        |
| :------ | :----------------- | :--- | :--------- | :-------------------------- |
| DERIVED | `cont_review_main` | ref  | **77,724** | 全量扫描 + filesort         |
| PRIMARY | `<derived2>`       | ALL  | 77,724     | 派生表无索引，全表扫描      |
| PRIMARY | `exe`              | ref  | 1          | 通过 `cont_number` 索引查找 |

### 1.3 核心瓶颈

#### 1.3.1 **派生表 `<derived2>` 无索引，导致全表扫描 77,724 行**

子查询生成派生表后，MySQL 无法为其创建索引（除非用 `LATERAL` 或物化），所以 `main.rn = 1` 的过滤是在**无索引的全表扫描**上进行的。

#### 1.3.2 **`cont_review_main` 的 `filesort` 开销大**

```sh
Using filesort  对 77,724 行做窗口函数排序
```

虽然用了 `idx_htps1_main`（`del_flag` 上的索引），但 `PARTITION BY cont_number ORDER BY create_time DESC` 需要额外排序。

## 二、优化方案

### 2.1 使用LATERAL关联子查询

使用LATERAL关联子查询避免派生表全扫描（MySQL 8.0.14+）

```sql
SELECT
  exe.overdue_amount
FROM
  cont_execute exe
  INNER JOIN LATERAL (
    SELECT
      is_important_cont,
      is_important_cont_in
    FROM cont_review_main main
    WHERE main.cont_number = exe.cont_number
      AND main.del_flag = 0
    ORDER BY main.create_time DESC
    LIMIT 1
  ) main ON main.is_important_cont_in = 0
WHERE
  exe.del_flag = 0
  AND exe.cont_company_name = '伟仕佳杰（重庆）科技有限公司';
```

**优势**：`LATERAL` 让子查询能利用 `exe.cont_number` 逐行过滤，避免生成大派生表。

**需要的索引**：

```sql
CREATE INDEX idx_main_cont_time
  ON cont_review_main(cont_number, create_time DESC, del_flag);
```

测试执行时间，0.75s，共计 3w条数据，性能有较大提升。

![](http://cdn.passjava.cn/uPic/202605131437723jRHetQ.png)

## 三、LATERAL 是什么？

**LATERAL** 是 MySQL 8.0.14+ 引入的关键字，意思是**横向关联**或**逐行引用**。

> 空哥发言：普通子查询是**独立执行**的，LATERAL 子查询可以**引用外层表的当前行**。

### 3.1 普通子查询和 LATERAL子查询对比

#### 3.1.1 普通子查询（错误，无法引用外层表）

```sql
-- 报错：exe.cont_number 在子查询里不认识
SELECT *
FROM cont_execute exe
INNER JOIN (
    SELECT *
    FROM cont_review_main m
    WHERE m.cont_number = exe.cont_number   -- ← 这里 exe 不存在！
    LIMIT 1
) main
```

#### 3.1.2 LATERAL 子查询（正确，可以引用外层表）

```sql
-- 正确：LATERAL 允许子查询引用 exe 的当前行
SELECT *
FROM cont_execute exe
INNER JOIN LATERAL (
    SELECT *
    FROM cont_review_main m
    WHERE m.cont_number = exe.cont_number   -- ← 现在可以用了！
    ORDER BY m.create_time DESC
    LIMIT 1
) main
```

直观比喻

| 类型       | 执行方式                           | 类比                         |
| :--------- | :--------------------------------- | :--------------------------- |
| 普通子查询 | 先**一次性**算完，再和外层关联     | 先印好一本通讯录，再发给大家 |
| LATERAL    | **逐行**执行，每行都用外层的值去查 | 每个人报姓名，现场查电话     |

## 四、优化前后 SQL 的逻辑对比

两个 SQL 在逻辑上**基本等价**，但存在一个微妙的潜在差异：当 `cont_review_main` 中同一合约存在多条 `create_time` 相同的记录时，两者选择“最新记录”的结果可能不一致。

### 4.1 详细对比

| 维度                          | SQL 1（LATERAL + LIMIT）                                            | SQL 2（窗口函数 + ROW_NUMBER）                                                                                                |
| :---------------------------- | :------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------- |
| 筛选最新记录的方式            | `ORDER BY create_time DESC LIMIT 1`                                 | `ROW_NUMBER() OVER (PARTITION BY cont_number ORDER BY create_time DESC)` 后取 `rn = 1`                                        |
| 对于相同 `create_time` 的处理 | 数据库返回**不确定的一条**（通常依赖存储顺序或索引扫描顺序）        | `ROW_NUMBER()` 的排序结果也不确定（若排序键不唯一，编号分配无稳定规则）                                                       |
| 核心过滤条件                  | 要求最新记录的 `is_important_cont_in = 0`，且必须存在匹配的审核记录 | 同上（通过 `WHERE main.rn = 1 AND main.is_important_cont_in = 0`）                                                            |
| JOIN 类型                     | `INNER JOIN LATERAL`（隐式要求子查询有返回值）                      | `LEFT JOIN` + WHERE 条件（实际等效为 `INNER JOIN`，因为 `main.rn` 和 `main.is_important_cont_in` 均为 `NOT NULL` 时才会保留） |
| 其他                          | 包含 `USE INDEX` 提示，仅影响执行计划，不改变结果                   | 派生表中多选了 `is_important_cont` 列，未使用                                                                                 |

### 4.2 结论

- **在假设 `create_time` 具有唯一性（或业务上不存在重复时间）的前提下**，两个 SQL 完全等价。
- **若存在重复时间**，两者结果可能不同，且均为“不确定”行为，不应依赖。建议为排序添加唯一列（如主键）作为 tie-breaker 以保证确定性。

### 4.3 优化建议

如果需要严格等价且结果确定，可将两个 SQL 都改为按 `(create_time DESC, id DESC)` 排序（假设 `id` 唯一）
