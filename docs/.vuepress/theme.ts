import { getDirname, path } from "vuepress/utils";
import { hopeTheme } from "vuepress-theme-hope";

import navbar from "./navbar.js";
import sidebar from "./sidebar/index.js";

const __dirname = getDirname(import.meta.url);

export default hopeTheme({
  hostname: "http://passjava.cn/",
  logo: "/logo.png",
  favicon: "/favicon.ico",

  //https://at.alicdn.com/t/c/font_2922463_o9q9dxmps9.css
  iconAssets: "//at.alicdn.com/t/c/font_4656749_qph2ex2rm9.css",

  author: {
    name: "悟空",
    url: "http://passjava.cn/article/",
  },

  repo: "https://github.com/Jackson0714/PassJava-Learning",
  docsDir: "docs",
  // 纯净模式：https://theme-hope.vuejs.press/zh/guide/interface/pure.html
  pure: true,
  breadcrumb: true,
  navbar,
  sidebar,
  footer:
    '<a href="https://beian.miit.gov.cn/" target="_blank">鄂ICP备2020015769号-1</a>',
  displayFooter: true,

  pageInfo: [
    "Author",
    "Date",
    "Category",
    "Tag",
    "Original",
    "Word",
    "ReadingTime",
    "PageView",
  ],

  blog: {
    intro: "/about-the-author/",
    sidebarDisplay: "mobile",
    medias: {
      Zhihu: "https://www.zhihu.com/people/passjava666",
      Github: "https://github.com/Jackson0714",
      Gitee: "https://gitee.com/jayh2018",
    },
  },

  plugins: {
    // 参考：https://theme-hope.vuejs.press/zh/guide/feature/comment.html
    // https://ecosystem.vuejs.press/zh/plugins/blog/comment/waline/
    comment: {
      provider: "Waline",
      serverURL: "https://comment.passjava.cn/", // your server url
      pageview: true,
    },
    components: {
      rootComponents: {
        // https://plugin-components.vuejs.press/zh/guide/utilities/notice.html#%E7%94%A8%E6%B3%95
        notice: [
          {
            path: "/",
            title: "知识星球",
            showOnce: true,
            content:
              "一对一交流/简历修改/专属求职指南，欢迎加入 悟空聊架构 知识星球。",
            actions: [
              {
                text: "前往了解",
                link: "http://passjava.cn/about-the-author/zhishixingqiu-two-years.html",
                type: "primary",
              },
            ],
          },
        ],
      },
    },

    blog: true,

    autoCatalog: {
      index: true,
    },

    copyright: {
      author: "悟空聊架构(passjava.cn)",
      license: "MIT",
      triggerLength: 100,
      maxLength: 700,
      canonical: "http://passjava.cn/",
      global: true,
    },

    feed: {
      atom: true,
      json: true,
      rss: true,
    },

    mdEnhance: {
      align: true,
      codetabs: true,
      figure: true,
      gfm: true,
      hint: true,
      include: {
        resolvePath: (file, cwd) => {
          if (file.startsWith("@"))
            return path.resolve(
              __dirname,
              "../snippets",
              file.replace("@", "./"),
            );

          return path.resolve(cwd, file);
        },
      },
      tasklist: true,
    },

    search: {
      isSearchable: (page) => page.path !== "/",
      maxSuggestions: 10,
    },
  },
});
