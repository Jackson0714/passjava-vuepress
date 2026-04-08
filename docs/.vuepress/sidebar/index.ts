import { sidebar } from "vuepress-theme-hope";
import { highQualityArticles } from "./high-quality-articles.js";
import { myProject } from "./my-project.js";
import { myEssay } from "./my-essay.js";
import { omnibus } from "./omnibus.js";
import { aboutTheAuthor } from "./about-the-author.js";
import { myColumn } from "./my-column.js";
import { weread } from "./weread.ts";
import { ai } from "./ai.ts";

export default sidebar({
  // 应该把更精确的路径放置在前边
  "/about-the-author/": aboutTheAuthor,
  // "/high-quality-articles/": highQualityArticles,
  "/my-project/": myProject,
  "/my-essay/": myEssay,
  "/omnibus/": omnibus,
  "/weread/": weread,
  "/ai/": ai,
  "/zhuanlan/": [
    "java-mian-shi-zhi-bei",
    "back-end-interview-high-frequency-system-design-and-scenario-questions",
    "handwritten-rpc-framework",
    "source-code-reading",
  ],
  "/": myColumn,
  // 必须放在最后面
  // "/": [
  //   {
  //     text: "必看",
  //     icon: "star",
  //     collapsible: true,
  //     prefix: "passjava/",
  //     children: ["intro", "use-suggestion", "contribution-guideline", "faq"],
  //   }
  // ],
});
