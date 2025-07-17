import { arraySidebar } from "vuepress-theme-hope";
import { getChildren } from "./autoSidebar";

export const omnibus = arraySidebar([
  {
    text: "阿里文章",
    icon: "micro-service",
    prefix: "ali/",
    collapsible: false,
    children: "structure",
  },
]);
