import { navbar } from "vuepress-theme-hope";

export default navbar([
  { text: "我的专栏", icon: "framework", link: "/home.md" },
  // { text: "架构进阶之路", icon: "book", link: "/home.md" },
  { text: "我的项目", icon: "xueyuanapp", link: "/my-project/" },
  { text: "我的随笔", icon: "gongzuotai", link: "/my-essay/" },
  { text: "精选文集", icon: "kaoqin", link: "/omnibus/" },
  { text: "读书笔记", icon: "zuoye", link: "/weread/" },
  { text: "人工智能", icon: "ai", link: "/ai/" },
  { text: "运维", icon: "shezhi", link: "/devops/" },
  // { text: "技术摘抄", icon: "icon-temp", link: "/high-quality-articles/"},
  {
    text: "知识星球",
    icon: "zhishixingqiu",
    children: [
      {
        text: "星球介绍",
        icon: "about",
        link: "/about-the-author/zhishixingqiu-two-years.md",
      },
      // {
      //   text: "星球专属优质内容",
      //   icon: "about",
      //   link: "/zhuanlan/",
      // },
      {
        text: "星球优质主题汇总",
        icon: "star",
        link: "https://www.yuque.com/wukong-9bwbm/rfukgb/itlxl4wnggtgqone",
      },
    ],
  },
  {
    text: "网站相关",
    icon: "wentifankui",
    children: [
      { text: "关于作者", icon: "zuozhe", link: "/about-the-author/" },
      {
        text: "更新历史",
        icon: "caozuorizhi",
        link: "/timeline/",
      },
    ],
  },
  {
    text: "我的博客",
    icon: "xueyuanapp",
    link: "/article/",
  },
]);
