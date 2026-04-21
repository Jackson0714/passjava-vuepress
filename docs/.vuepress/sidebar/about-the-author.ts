import { arraySidebar } from "vuepress-theme-hope";

export const aboutTheAuthor = arraySidebar([
  {
    text: "个人经历",
    icon: "wentifankui",
    collapsible: false,
    prefix: "experience/",
    children: [
      "05.four-magic-personal-job",
      "13.use-six-years-to-10k-fans",
      "my-github",
    ],
  },
  {
    text: "获奖情况",
    icon: "ticheng",
    prefix: "award/article-contest/",
    collapsible: false,
    children: "structure",
  },
]);
