---
title: 基于 AIOps 全球基础架构设施自动化运维的设计思路
date: 2025-09-10
---

原文链接：https://aws.amazon.com/cn/blogs/china/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops/

2016 年，Gartner 创新性地提出了 AIOps 的概念，开创了人工智能辅助运维决策的新篇章。

AIOps 的全称为 Artificial Intelligence for IT Operations，即为 IT 运维服务的人工智能。AIOps 是将人工智能和大数据分析技术应用于 IT 运维领域，旨在提高运维效率、自动化运维流程。AIOps 系统能够持续收集 IT 系统的各种运行数据，利用机器学习算法分析这些数据，及时发现异常情况、故障根源，并提供智能化的修复建议。它可以减轻运维人员的工作强度，提高故障处理效率。

而传统的运维方式往往依赖数个具备专业知识的运维人员对某个特定场景下的服务进行监控与决策。随着公司体量的成长，业务场景及数量指数型增长，传统运维将面临着决策时间长、决策难度大、人力成本高等问题，一旦出现重大决策失误，就可能造成巨大的商业损失。然而，海量的数据正好是机器学习的擅长领域。

**一套成熟的机器学习算法能够从运维操作中积累判断经验，不眠不休地持续对数据进行监控和分析，为运维决策提供有价值的信息。**

### SD-RTN™ 场景下的智能运维

本文我们以 SD-RTN™场景，介绍智能运维的设计思路和落地方案。

SD-RTN™，全称为 Software Defined Real-time Network，是声网专为双向实时音视频互动而设计的软件定义实时网。

它实现的核心是由遍布全球的机房搭建起的音视频传输网络，每个机房在信息传递的过程中都承担着发送和接受的工作。所有经过这些机房的音视频质量会通过一定的方式进行指标采集和上报，用于实时质量监控。而一旦这些指标反映出经过某个机房的通话出现了不可接受的问题，则需要对机房进行对应的运维操作，以保障用户的优质音视频体验。

传统的运维方法使用绝对水位或逻辑条件的方式进行机房质量监控，这种监控虽然能够识别一些质量异常，但存在着漏警误警严重、维度单一等问题，针对靠近阈值的报警缺少辨别能力，对于非常规质量异常的传输质量指标曲线也缺乏识别能力。而智能运维，正好可以弥补传统运维的不足。

本文我们会从智能运维的宗旨、架构、算法、技术细节等维度进行分享。

## 1. 智能运维的宗旨

我们首先要划定一条智能运维的思想主线，来实现其宗旨。目标，能力，边界三要素，需要我们进行清晰界定。

### 1.1 智能运维的目标

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops1Sks2Cg.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops1.png)

智能运维是一种运维形式的变更，其目标是将传统的值班制通过智能运维架构体系，改造为二十四小时不间断的异常监控和异常处理。同时，智能运维也是一种集体智慧的体现。由于每个运维人员的能力和经验有所不同，采取的运维手段也不尽相同，但一套优秀的智能运维体系能够从历史事件中总结经验智慧，得到一个相对优秀的解决方案。最后，至关重要的一点，传统的运维方式往往是处理故障，属于故障发生之后再去止血补救，而智能运维很大程度上赋能了主动运维这个概念，在故障出现前通过一些前兆特征加以规避，或者使故障范围最小化。

### 1.2 智能运维的能力

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops2Z5e35B.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops2.png)

智能运维是一种集体智慧的体现，智能运维的能力之一就是从有经验的运维人员的操作或判断中总结方法论，以指导未来的操作。当然，算法能力的提升除了依赖于运维人员的经验，也可以通过自编码的方式实现，这点在 AIGC 时代尤其能够体现，也会在接下来介绍算法的时候提到。总之，我们对智能运维的期望是它能够不间断地模拟有经验的运维人员，处理各种已经暴露的或者潜在的风险，但同时也要明确智能运维的能力边界。运维的场景往往不是非黑即白，而是存在很多灰色区域，可以自由选择是否处理，如何处理。对于智能运维体系，我们称之为边际能力。对边际能力的细化将有助于整体能力的提升。同时我们也应该明确，智能运维不等于无人运维，在一些特殊场景下，比起要求智能运维处理，我们会更希望它起到通知的作用；而在极端场景下，尤其是算法从未获得过经验知识的场景下，人的介入是必要的。

### 1.3 智能运维的边界

智能运维的目标对象是路径传输，软件状态和基础资源。智能运维的能力当然是保障这些目标对象正常运作。但同时我们应该认识到两个准则：

- 人类获取信息的渠道并非一成不变的；
- 互联网及其基础设施不是百分百可靠的。

这两个准则决定了算法存在一定的自然能力边界。在实际运维中如果遇到比较复杂的情况，运维人员会结合多个看板内容，多方信息反馈，多种日志文件决定实际的运维操作，而这些数据并不一定已经输入到智能运维体系中。更何况有些时候运维人员会从武装冲突、自然灾害等特殊情况中得到经验，获取信息多样化的途径并非智能运维体系能够完全覆盖的。其次，当智能运维体系的软件问题，消息传递，数据存储等基础设施故障，都会影响到智能运维体系本身的 SLA。

如何提升智能运维系统本身的韧性，自然成为我们首先需要考虑的问题。

## 2. 智能运维的架构

### 2.1 算法架构

智能运维架构设计的两个核心点，**分层化**和**模块化**。首先，根据智能运维全流程中的职能，我们将全过程的实现分为三大能力层，**监控告警层，智能运维层**和**统一执行层：**

- 智能运维层处于中间的位置，相当于全流程中的大脑部分，起到分析、决策的作用；
- 监控告警层是管理告警信息、通知运维人员的部分，相当于全流程中的嘴；
- 统一执行层会真正调用脚本和接口进行运维操作，相当于全流程中的手。

值得注意的是，监控告警层和统一执行层原则上不会直接连接，由监控告警层产生的运维请求，也必须在智能运维层已知的情况下传递到统一执行层。这样做可以使智能运维层视野的全局性得到保证，以便其给出更加合理的运维建议。同时，分层的结构将更利于系统的开发、改进和维护。在智能运维层给出对应交互格式样例的情况下，监控告警层和统一执行层将在整体结构上保证相对独立，其内部功能的丰富不依赖同时也不会受到智能运维层的影响。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops3O530q6.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops3.png)

智能运维层的流程设计中，最核心的一点就是模块化。之前提到了智能运维的阻力之一，互联网及其基础设施不是百分百可靠的，因此，负责运维的工具本身更应该拥有更高级别的可用性。图中是声网 SD-RTN 智能运维中一部分功能的信息流导向图，所有的算法结果均以信息流的方式向监控告警层和统一执行层传递。复数一级算法从数据中心处读取数据，经过算法逻辑后生成内部信息流，分享一级报警给统一执行层和监控告警层，并将数据和信息流存储在标准存储层中供后续算法迭代和二级算法分析使用。二级算法不再直接对接原始数据源，负责处理更高维度的数据，给出更综合的运维建议。在运行过程中，算法本身的读取、计算、存储也应当是模块化的。将所有的步骤和结构都模块化后，所有的传输流程都可以进行监控，所有的模块本身也可以进行健康上报，这大大提升了架构的可用性。同时也可以通过一些常规方法，如重要模块多点部署，信息流添加唯一可追溯字段，使用云端服务等常见高可用策略进一步提升智能运维服务的可用性。同时，模块化带来的另一个好处是高拓展性。这种高拓展性既体现在数据源上，也体现在算法设计上。我们之前提过智能运维的另一阻力，人类获取信息的渠道并非一成不变的。这意味着随着我们对于运维目标认知的增加，数据源可能会发生改变，数据规模可能会指数级增加，算法可能也会需要迭代甚至重做。这些情况在智能运维项目的开发过程中是非常常见且具有正面意义的，而一个高拓展性的架构就意味着所有的升级迭代流程和成本都可以大大降低。还是基于刚才声网的信息流导向图，当一级算法需要增加维度时，只需要由数据中心添加一条数据流，配置新的算法，再按照对应格式传输信息流就可以实现对接。当出现由于维度增加，算法需求视野增加等原因导致标准存储层压力过大时，我们只需要横向拓展数据库就可以实现容量的增加。当整个二级算法需要迭代时，我们可以使用长期存储层的数据进行训练和校验，然后再单独替换二级算法。智能运维模块化的设计在面对各种变更时，能有效避免牵一发而动全身，也更适合算法开发阶段需要面对的频繁调整的场景。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops4f4j1gL.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops4.png)

### 2.2 系统架构

构建一套成熟的智能运维架构体系，也要充分考虑系统架构的韧性和扩展性。基于亚马逊云科技，以 Severless、低代码的理念，构建了“信息流聚合分析平台”。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops5ZVWKlD.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops5.png)

#### 架构组件介绍

我们根据数据流走向，对整个架构，进行介绍：

1. Agent 运行异常检测算法，进行源数据的采集过滤，并发送异常信息
2. 使用 Kinesis Data Stream 作为数据流接入点，不同的采集信息流，发送到各自的“Data Stream”
3. Redshift 作为数据的统一查询出口，通过 Redshift Streaming Ingestion 可以实时查询 Data Stream 信息流
4. Redshift Spectrum 可以支持运维人员，针对历史信息的查询
5. Firehose 将 Kinesis Data Stream 数据流存储到 S3，以满足故障复盘，数据审计等
6. 运维分析算法通过 Redshift 中的异常信息数据，Amazon Neptune 中分布在全球的设备关系图谱数据，进行聚合分析，并将维护操作下发，和运维人员操作告警
7. 运维人员通过 OPS 平台，追溯告警信息，通过 Lambda 对 S3 上的历史信息进行查询
8. 查询展示部分，对应不同用户角色，提供了相应的查询方式/工具：
   1. Redshift Query Editor：针对数据分析人员，提供了 SQL base 的查询编辑器
   2. QuickSight：业务分析人员，通过 BI 工具可以获得更友好的数据图形展示
   3. Bedrock Claude：在 AIOps 系统中，大语言模型可以用于自然语言处理，如解析运维人员的自然语言指令、自动生成故障报告等

#### 架构特点

- 架构成熟：这是一个成熟的数据流查询处理架构，实施过程，都是低代码构建。
- 稳定性高：

Kinesis 99.9%
Redshift 99.9%
Lambda 99.95%
Neptune 99.9%
S3 数据可靠性，11 个 9

- 扩展性强：以托管的 Serverless 服务为主，资源扩展性强。
- 数据分层存储：Kinesis 存储实时数据，作为当前告警信息。历史信息存放到 S3。有效降低成本。
- SQL 流式数据查询：都可以通过 Redshift 作为统一查询入口，方便多表关联查询等复杂场景，同时查询 Mysql，kinesis，S3 的数据。
- 快速部署：通过 CloudFormation，新 Region 可以在 15 分钟内完成整个平台部署。

## 3. 智能运维的算法

接下来我将介绍一下智能运维的一些常见算法，受限于篇幅关系，不会对算法的细节和原理有太多的展开，而会更加侧重于算法的设计思路，希望能给各位带来一点启发。

### 3.1 传统算法

很多时候大家提到算法就想到深度学习，大模型，其实忽略了一个重点，算法是为了解决业务问题而存在的。虽然算法能力的多样性和全面性，在其他条件相同的情况下，是与复杂度正相关的。但一个能够解决需求的简单算法，从开发成本、时间投入、适配场景、迁移难度等多方便因素考虑都是比一个复杂算法更优秀的。因此，算法的开发更推崇由简至繁，当不能满足需求时，再节节升级。常见的传统算法根据我们的目标是标签类的还是数值类的，可以简单分为分类算法和预测算法，里面有很多经典思路更是经久不衰。值得注意的是，在创造算法时我们要关注许多问题，比如工作量最大的预处理阶段，我们要注意时序数据是否满足一些基本的要求，比如相对稳定、时间间隔相等、数值是否符合业务逻辑等等，需要对原始数据进行对应的预处理，在保证干净可用的同时尽量不丢失重要的原始信息。比如设计时要搞清楚业务上到底需求一个怎样的结果和响应时间，是否存在合适的数据和模型是否能够支持。训练时也要考虑算法该如何使用历史的数据或故障信息来得到一个具有相对普适性的模型，采用怎样的指标验证，模型能力是否相对静态，如果是有输入反馈如何进行迭代等种种问题。解决这些问题的方法和模型的选择都不一定只存在唯一解，开发算法时应该凭借经验给出最合适的算法范围或解决手段，然后勇于尝试。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops6aHFuGW.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops6.png)

### 3.2 特征工程

在这些算法和工具中，我想重点讲一下特征工程。在应用算法时，除了自身就具备特征工程能力的深度学习外，我们几乎不会将原始数据经过简单的预处理直接使用，而是会先进行特征工程。时间序列上的特征工程有三种常见手段，分割、升维、降维。由于时间序列存在一定的时效性，根据业务特点，超过一定长度的数据不适合用在短期的分类任务或预测任务，我们一般会将时间序列分割为一个个窗口，以窗口维度进行记录。相比于通常的升维概念，由于时间的特殊属性，时序数据往往能够拆分出更多的维度，诸如 statmodels、tslearn、tsfresh 等常用时序库都很好的提供了时序特征升维分解的能力。时间序列的降维则包含了时间序列曲线的平滑，特征的筛选等，由于会造成信息的缺失，通常是放在升维之后，考虑维度特征与目标之间的关联性来进行取舍。即使没有能够直接通过特征工程解决问题，操作的过程也能让我们对原始数据有着更加清晰的认知，这对我们设计其他的算法或者神经网络模型的结构也都有着很大的启发。

### 3.3 生成式神经网络

我们以声网智能运维团队自行构建的 GRTAE，GRTVAE 为例，简单介绍下生成式神经网络。时下非常火爆的 AIGC 话题的 G，指代的就是生成式。当训练模型时的负样本数量非常有限，标注数据规模较小时，生成式神经网络就成为了一个相对较优的选项。时间序列相关的生成式神经网络在结构上可以是多种多样的，一般需要根据神经网络各自层的用途来进行设计，比如增加全连接层来增加复杂度，增加池化层来增加鲁棒性等。值得注意的是，与图像和文字不同，时间的传递方向是单向的，这就意味着添加卷积层等具有方向性的神经网络层的时候需要注意维度和方向。另外，由于时刻是会周而复始的循环的，将时刻信息通过特殊方式嵌入到神经网络中往往能够对算法整体能力起到较大帮助。采用深度学习时，必须要注意，任何方案都有一定的 tradeoff。深度学习虽然能够更简单有效的获得输入输出，可以通过大量的数据堆积变得更加全面，但同时也较大程度上丧失了其可解释性，同时会使整体链路时间延长、依赖增加，因此并非所有的业务场景都能够较好适用。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops7AvuOe5.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops7.png)

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops8uEwehP.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops8.png)

## 4. 智能运维系统 端到端数据流展示

在详细地介绍了智能运维的架构、算法之后，我们通过一个告警数据流的演示，更清晰地展现整个智能运维的工作原理。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops9SCPU5U.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops9.png)

### 端到端技术详解

#### 信息流部分技术详解

1. 指标元数据样式

以”最后一英里”的用户接入质量监控为例，每分钟会从数据源持续输入约 9000 条数据，数据样式包含：时间戳，数据所属维度，接入国家，接入机房，接入运营商，区间内统计打点上报数量，符合不同丢包标准的上报数量，符合不同迟延标准的上报数量。

同时，还会存在许多例如厂商维度质量统计表，运维操作状态表，区域容量状态表等其他辅助数据。

1. 信息采集 agent 的 AI 算法处理后，发给 kinesis 的数据格式

一级 AI 算法处理，将单维度的报警信息作为数据流传递给 kinesis，报警信息包含：事件 ID、时间戳、运维机房、维度、子维度、根因分析、严重等级、偏离值、操作状态、看板链接等。

1. 通过 redshift 建标 SQL 语句

   ```sql
   DROP SCHEMA if exists <schema_name>;
   ---创建EXTERNAL SCHEMA
   CREATE EXTERNAL SCHEMA <schema_name>
   FROM KINESIS
   IAM_ROLE <iam_role>;
   ---创建物化视图
   CREATE MATERIALIZED VIEW <table_name> AUTO REFRESH YES AS
   SELECT approximate_arrival_timestamp,JSON_PARSE(from_varbyte(kinesis_data, 'utf8')) as Data
   FROM <schema_name>.<kinesis_source>
   WHERE is_utf8(kinesis_data) AND is_valid_json(from_varbyte(kinesis_data, 'utf8'))
   ```

2. 通过 redshift streaming ingest 查询的 SQL

   ```sql
   select Data.event_id::varchar,\
       Data.idc::varchar,\
       Data.ts::int,\
       Data.type::varchar,\
       Data.sub_type::varchar,\
       Data.drill_cause::varchar,\
       Data.alert_level::int,\
       Data.decrease_value::float,\
       Data.status::varchar,\
       Data.link::varchar\
       from alert_stream_table\
       where Data.ts >= <CURRENT_TS>-2*60*60 and Data.ts <= <CURRENT_TS>\
       order by Data.ts
   ```

3. 通过 redshift streaming ingest 查询的 SQL 的输出格式

   ```sql
   查询结果转换为DataFrame格式的表格，列名包含：event_id，idc，ts，type，sub_type，drill_cause，alert_level，decrease_value，status，link
   ```

4. 通过运维分析算法处理后，发送的运维指令给谁，输出的格式
   二级 AI 算法处理，将多维度分析后的运维操作手段以 JSON 格式推送到各个消费端，运维信息包含：事件 ID、时间戳、运维机房、运维来源、供应商。维度数量、可靠程度、操作状态。

5. 发给运维人员

   同时，二级 AI 算法会以企业微信的形式，将自动处理后的运维结果通知到运维人员所在企业微信群组；针对未成功执行的运维操作会电话报警相关运维人员。

   点击近期报警链接会对添加对应的 WHERE 条件，对 redshift 进行一次查询并返回查询结果，帮助运维人员了解目前对应机房的所有维度的故障细节，方便问题定位和后续处理。

   [![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops10VdXe2O.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops10.png)

## 5. 智能运维成果

针对机房出现的各种特定场景下的传输质量问题，智能运维能够增加运维的覆盖面积，有效缩短运维时间，降低人力消耗。在部分场景下，智能运维会采取保护性的方式提前运维，防患于未然。对客户流量的实时预测，除了起到帮助客户感知问题外，也可以在销售策略上起到指导性作用。除此之外，智能运维还在声网很多场景下发挥着作用，这里就不再一一赘述。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops11zV2DvJ.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops11.png)

## 6. 智能运维的未来

智能运维作为人工智能技术在运维领域的应用，是随着技术的发展不断演变的，而这些新技术又能持续为智能运维提供新鲜的血液，使智能运维更高效便捷，覆盖度更广。

### 6.1 GNN 与智能运维

RTS 这个实时通讯场景天生就和图算法有着较高的契合度。实时互联网的信息传递状态可以非常直观地体现在拓扑图中。而比起一般的图，时间维度提供了更高的维度和更丰富的数据。举个例子，如果训练得当，我们可以通过各个城市间实时的网络流量和质量预测未来的大流量和高质量风险，在全局视野上实现预知网络动向。但相对的，将大规模的图数据实时输入模型也将成为一个难点。

### 6.2 RL 与智能运维

实时通讯这种状态随时间变化的场景同样也非常适合强化学习发挥能力。如果要使用强化学习来支持智能运维，可执行的运维手段自然的就成为了行动部分。但相对的，如何定义反馈机制进而得到一个正确且稳定的智能运维系统将成为一个难点。

[![img](http://cdn.passjava.cn/uPic/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops12gq8adZ.png)](https://s3.cn-north-1.amazonaws.com.cn/awschinablog/design-ideas-for-automated-operation-and-maintenance-of-global-infrastructure-facilities-based-on-aiops12.png)

### 6.3 AIGC 与智能运维

AIGC 是当下最热门的话题和技术。但是智能运维不是 AIGC 的一个优秀应用场景，因为 AIGC 的主要能力侧重点在创造，会以图像或语言为载体进行模仿式的生成，而智能运维更倾向于决策，要求的是准确和稳定。但之前我们也提到，智能运维并不等价于无人运维，在很多场景下仍旧离不开人的判断和决策。在这一角度上，AIGC 能够为智能运维提供一些帮助。通过 fine-tuning 的概念，训练一个具备丰富运维知识的大语言模型，就相当于有一个实时在线的具有丰富经验的运维人员，通过和人的对话来给出有帮助的运维建议。

## 参考文档

https://docs.aws.amazon.com/zh_cn/kinesisanalytics/latest/dev/what-is.html

https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c-getting-started-using-spectrum-add-role.html
