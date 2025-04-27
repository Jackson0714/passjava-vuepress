---
doc_type: weread-highlights-reviews
bookId: CB_2qg3FS3EPG1r6hn6gY7X0FdL
reviewCount: 4
noteCount: 7
author: 【英】厄马（Raoul-Gabriel Urma）【意】 弗斯科（Mario Fusco）【英】 米克罗夫特（Alan Mycroft）
cover: https://res.weread.qq.com/wrepub/CB_2qg3FS3EPG1r6hn6gY7X0FdL_parsecover
readingStatus: 未标记
progress: 42%
totalReadDay: 10
readingTime: 1小时54分钟
readingDate: 2023-07-16
isbn: 
lastReadDate: 2023-08-23

---
# 元数据
> [!abstract] Java 8实战
> - ![ Java 8实战|200](https://res.weread.qq.com/wrepub/CB_2qg3FS3EPG1r6hn6gY7X0FdL_parsecover)
> - 书名： Java 8实战
> - 作者： 【英】厄马（Raoul-Gabriel Urma）【意】 弗斯科（Mario Fusco）【英】 米克罗夫特（Alan Mycroft）
> - 简介： 
> - 出版时间： 
> - ISBN： 
> - 分类： 
> - 出版社： 人民邮电出版社
> - PC地址：https://weread.qq.com/web/reader/ce442813643425f32716733465333455047317236686e36675937583046644cc83

# 高亮划线

## 4.1　流是什么

> 📌 流是Java API的新成员，它允许你以声明性方式处理数据集合（通过查询语句来表达，而不是临时编写一个实现）。就现在来说，你可以把它们看成遍历数据集的高级迭代器。此外，流还可以透明地并行处理，你无需写任何多线程代码了！ 
> ⏱ 2023-07-16 07:57:07 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-81-422-557

> 📌 代码是以声明性方式写的 
> ⏱ 2023-07-16 07:58:58 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-81-2409-2437

> 📌 你可以把几个基础操作链接起来，来表达复杂的数据处理流水线 
> ⏱ 2023-07-16 07:59:04 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-81-2672-2700

## 5.3.3　查找元素

> 📌 Optional<T>类（java.util.Optional）是一个容器类，代表一个值存在或不存在。在上面的代码中，findAny可能什么元素都没找到。Java 8的库设计人员引入了Optional<T>，这样就不用返回众所周知容易出问题的null了。 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-103-825-1023
- 💭 Optional 简介
    - ⏱ 2023-08-23 23:20:20 

## 5.4　归约

> 📌 此类查询需要将流中所有元素反复结合起来，得到一个值，比如一个Integer。这样的查询可以被归类为归约操作（将流归约成一个值）。用函数式编程语言的术语来说，这称为折叠（fold），因为你可以将这个操作看成把一张长长的纸（你的流）反复折叠成一个小方块，而这就是折叠操作的结果 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-105-724-907
- 💭 折叠这个解释好 - ⏱ 2023-08-17 09:17:57 

## 5.8　小结

> 📌 Streams API可以表达复杂的数据处理查询。常用的流操作总结在表5-1中。
   •  你可以使用filter、distinct、skip和limit对流做筛选和切片。
   •  你可以使用map和flatMap提取或转换流中的元素。
   •  你可以使用findFirst和findAny方法查找流中的元素。你可以用allMatch、noneMatch和anyMatch方法让流匹配给定的谓词。
   •  这些方法都利用了短路：找到结果就立即停止计算；没有必要处理整个流。
   •  你可以利用reduce方法将流中所有的元素迭代合并成一个结果，例如求和或查找最大元素。
   •  filter和map等操作是无状态的，它们并不存储任何状态。reduce等操作要存储状态才能计算出一个值。sorted和distinct等操作也要存储状态，因为它们需要把流中的所有元素缓存起来才能返回一个新的流。这种操作称为有状态操作。
   •  流有三种基本的原始类型特化：IntStream、DoubleStream和LongStream。它们的操作也有相应的特化。
   •  流不仅可以从集合创建，也可从值、数组、文件以及iterate与generate等特定方法创建。
   •  无限流是没有固定大小的流。 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-120-512-1474
- 💭 第五章总结
    - ⏱ 2023-08-23 23:17:56 

## 第 6 章　用流收集数据

> 📌 你可以把Java 8的流看作花哨又懒惰的数据集迭代器。它们支持两种类型的操作：中间操作（如filter或map）和终端操作（如count、findFirst、forEach和reduce）。中间操作可以链接起来，将一个流转换为另一个流。这些操作不会消耗流，其目的是建立一个流水线。与此相反，终端操作会消耗流，以产生一个最终结果，例如返回流中的最大元素。它们通常可以通过优化流水线来缩短计算时间。 ^CB-2qg3FS3EPG1r6hn6gY7X0FdL-121-678-953
- 💭 这个通俗易懂地解释了流是什么。 - ⏱ 2023-08-23 23:38:29 

# 读书笔记

## 5.3.3　查找元素

### 划线评论
> 📌 Optional<T>类（java.util.Optional）是一个容器类，代表一个值存在或不存在。在上面的代码中，findAny可能什么元素都没找到。Java 8的库设计人员引入了Optional<T>，这样就不用返回众所周知容易出问题的null了。  ^37992928-7KGLnBU7m
    - 💭 Optional 简介

    - ⏱ 2023-08-23 23:20:28
   
## 5.4　归约

### 划线评论
> 📌 此类查询需要将流中所有元素反复结合起来，得到一个值，比如一个Integer。这样的查询可以被归类为归约操作（将流归约成一个值）。用函数式编程语言的术语来说，这称为折叠（fold），因为你可以将这个操作看成把一张长长的纸（你的流）反复折叠成一个小方块，而这就是折叠操作的结果  ^37992928-7KwKmd33m
    - 💭 折叠这个解释好
    - ⏱ 2023-08-17 09:18:08
   
## 5.8　小结

### 划线评论
> 📌 Streams API可以表达复杂的数据处理查询。常用的流操作总结在表5-1中。
•  你可以使用filter、distinct、skip和limit对流做筛选和切片。
•  你可以使用map和flatMap提取或转换流中的元素。
•  你可以使用findFirst和findAny方法查找流中的元素。你可以用allMatch、noneMatch和anyMatch方法让流匹配给定的谓词。
•  这些方法都利用了短路：找到结果就立即停止计算；没有必要处理整个流。
•  你可以利用reduce方法将流中所有的元素迭代合并成一个结果，例如求和或查找最大元素。
•  filter和map等操作是无状态的，它们并不存储任何状态。reduce等操作要存储状态才能计算出一个值。sorted和distinct等操作也要存储状态，因为它们需要把流中的所有元素缓存起来才能返回一个新的流。这种操作称为有状态操作。
•  流有三种基本的原始类型特化：IntStream、DoubleStream和LongStream。它们的操作也有相应的特化。
•  流不仅可以从集合创建，也可从值、数组、文件以及iterate与generate等特定方法创建。
•  无限流是没有固定大小的流。  ^37992928-7KGLe76UN
    - 💭 第五章总结

    - ⏱ 2023-08-23 23:18:07
   
## 第 6 章　用流收集数据

### 划线评论
> 📌 你可以把Java 8的流看作花哨又懒惰的数据集迭代器。它们支持两种类型的操作：中间操作（如filter或map）和终端操作（如count、findFirst、forEach和reduce）。中间操作可以链接起来，将一个流转换为另一个流。这些操作不会消耗流，其目的是建立一个流水线。与此相反，终端操作会消耗流，以产生一个最终结果，例如返回流中的最大元素。它们通常可以通过优化流水线来缩短计算时间。  ^37992928-7KGMApEb8
    - 💭 这个通俗易懂地解释了流是什么。
    - ⏱ 2023-08-23 23:38:53
   
# 本书评论

