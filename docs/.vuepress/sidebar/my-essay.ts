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
]);
