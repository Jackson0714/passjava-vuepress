import { arraySidebar } from "vuepress-theme-hope";
import { getChildren } from "./autoSidebar";

export const myProject = arraySidebar([
  {
    text: "一、刷题系统 PassJava",
    icon: "list-check",
    prefix: "passjava",
    collapsible: false,
    children: 
      [
        {
          text: "一、刷题系统-项目介绍",
          icon: "list-check",
          prefix: "01.introduction",
          collapsible: false,
          children: getChildren('./docs/my-project/passjava/01.introduction/'),
        },
        {
          text: "二、刷题系统-技术进阶",
          icon: "list-check",
          prefix: "02.passjava_architecture",
          collapsible: true,
          children: getChildren('./docs/my-project/passjava/02.passjava_architecture/'),
        },
        {
          text: "三、刷题系统-业务功能",
          icon: "list-check",
          prefix: "03.passjava_business",
          collapsible: true,
          children: getChildren('./docs/my-project/passjava/03.passjava_business/'),
        }
      ]

  }
]);
