import { arraySidebar } from "vuepress-theme-hope";
import { getChildren } from "./autoSidebar";

export const myEssay = arraySidebar([
  {
    text: "博客优化",
    icon: "micro-service",
    prefix: "my-blog/",
    collapsible: true,
    children: "structure",
  },
  {
    text: "我的开源项目",
    icon: "micro-service",
    prefix: "my-opensource/",
    collapsible: true,
    children: "structure",
  },
  {
    text: "开源周",
    icon: "micro-service",
    prefix: "open-source-weekly/",
    collapsible: true,
    children: "structure",
  },
  {
    text: "AI",
    icon: "micro-service",
    prefix: "AI/",
    collapsible: true,
    children: [
      {
        text: "AI 基础知识",
        icon: "micro-service",
        prefix: "",
        collapsible: true,
        children: "structure",
      },
      {
        text: "CodeBuddy",
        icon: "micro-service",
        prefix: "codebuddy/",
        collapsible: true,
        children: "structure",
      },
    ],
  },
  {
    text: "工具",
    icon: "micro-service",
    prefix: "tools/",
    collapsible: true,
    children: "structure",
  },
]);
