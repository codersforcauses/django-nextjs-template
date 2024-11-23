import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "django-nextjs-template",
  description: "Project Documentation",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: "Home", link: "/" },
      { text: "Frontend", link: "/client" },
      { text: "Backend", link: "/server" },
    ],

    sidebar: [
      {
        text: "Frontend",
        items: [],
      },
      {
        text: "Backend",
        items: [],
      },
      {
        text: "Examples",
        items: [
          { text: "Markdown Examples", link: "/examples/markdown-examples" },
          { text: "Runtime API Examples", link: "/examples/api-examples" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/codersforcauses" },
    ],
  },
});
