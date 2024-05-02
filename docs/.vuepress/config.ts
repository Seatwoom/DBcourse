import { defineUserConfig } from "vuepress";
import theme from "./theme.js";
import MarkdownItPlantuml from "markdown-it-plantuml";

export default defineUserConfig({
  base: "/DBcourse/",

  lang: "en-US",
  title: "Система управління відкритими даними",
  description: "Лабораторні роботи",

  theme,

  extendsMarkdown: (md) => {
    md.use(MarkdownItPlantuml);
  },

  // Enable it with pwa
  // shouldPrefetch: false,
});
