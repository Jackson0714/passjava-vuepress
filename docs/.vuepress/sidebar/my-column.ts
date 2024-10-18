import { arraySidebar } from "vuepress-theme-hope";
import { getChildren } from "./autoSidebar";

export const myColumn = arraySidebar([
  {
    text: "SpringCloud 架构原理和实战",
    icon: "micro-service",
    prefix: "my-column/springcloud/",
    collapsible: true,
    children: 
      [
        {
          text: "Eureka 注册中心源码剖析",
          icon: "guide",
          prefix: "01.eureka",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/01.eureka/'),
        },
        {
          text: "Ribbon 负载均衡架构剖析",
          icon: "guide",
          prefix: "02.ribbon",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/02.ribbon/'),
        },
        {
          text: "OpenFeign 远程调用架构剖析",
          icon: "guide",
          prefix: "03.openfeign",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/03.openfeign/'),
        },
        {
          text: "Gateway 网关架构剖析",
          icon: "guide",
          prefix: "04.gateway",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/04.gateway/'),
        },
        {
          text: "Nacos 注册中心架构剖析",
          icon: "guide",
          prefix: "05.nacos",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/05.nacos/'),
        },
        {
          text: "Sentinel 流量控制原理剖析",
          icon: "guide",
          prefix: "06.sentinel",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/06.sentinel/'),
        },
        {
          text: "Seata 分布式事务原理剖析",
          icon: "guide",
          prefix: "07.seata",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/07.seata/'),
        },
        {
          text: "链路追踪原理剖析",
          icon: "guide",
          prefix: "08.trace",
          collapsible: true,
          children: getChildren('./docs/my-column/springcloud/08.trace/'),
        }]
  },
  {
    text: "ELK 统一日志平台原理和实战",
    icon: "elk",
    prefix: "my-column/elk/",
    collapsible: true,
    children: getChildren('./docs/my-column/elk')  
  },
  {
    text: "Jenkins 自动化部署实战",
    icon: "jenkins",
    prefix: "my-column/jenkins/",
    collapsible: true,
    children: getChildren('./docs/my-column/jenkins')  
  },
  {
    text: "用故事讲解分布式协议原理",
    icon: "distributed",
    prefix: "my-column/distributed-protocol/",
    collapsible: true,
    children: getChildren('./docs/my-column/distributed-protocol')  
  },
  {
    text: "Java核心知识",
    icon: "distributed",
    prefix: "my-column/java-core/",
    collapsible: true,
    children: [
      {
        text: "Java基础知识",
        icon: "distributed",
        prefix: "01.JavaCore",
        collapsible: true,
        children: getChildren('./docs/my-column/java-core/01.JavaCore')  
      },
      {
        text: "Spring核心知识",
        icon: "distributed",
        prefix: "02.Spring",
        collapsible: true,
        children: [
          {
            text: "Spring基础知识",
            icon: "distributed",
            prefix: "01.SpringCore",
            collapsible: true,
            children: getChildren('./docs/my-column/java-core/02.Spring/01.SpringCore')  
          },
        ]
      },
      {
        text: "Mybatis基础知识",
        icon: "distributed",
        prefix: "01.JavaCore",
        collapsible: true,
        children: getChildren('./docs/my-column/java-core/01.JavaCore')  
      },
    ]
  },
  {
    text: "Java并发编程",
    icon: "distributed",
    prefix: "my-column/java-concurrent/",
    collapsible: true,
    children: getChildren('./docs/my-column/java-concurrent') 
  }
]);
