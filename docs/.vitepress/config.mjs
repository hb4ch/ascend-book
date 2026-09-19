import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import footnote from 'markdown-it-footnote'
import { sidebar } from './sidebar.mjs'

export default withMermaid({
  mermaid: {
    securityLevel: 'loose',
    theme: 'base'
  },
  markdown: {
    lineNumbers: true,
    theme: { light: 'github-light', dark: 'github-dark' },
    config: (md) => {
      md.use(footnote)
    }
  },
  lang: 'zh-CN',
  title: '昇腾平台技术实战',
  description: '面向实操型工程师的昇腾全栈技术书——从芯片架构到算子开发、性能优化、分布式通信与现代编译后端',
  // GitHub Pages 项目站点需设置 VP_BASE=/ascend-book/；本地默认 '/'
  base: process.env.VP_BASE || '/',
  // GitHub Pages 不支持无后缀路由，部署时退回 .html
  cleanUrls: !process.env.VP_BASE,
  lastUpdated: true,
  themeConfig: {
    nav: [
      { text: '导读', link: '/' },
      { text: '第一编 · 平台全景', link: '/01-platform/' },
      { text: '第二编 · 运行时与底层', link: '/02-runtime/' },
      { text: '第三编 · 算子开发', link: '/03-ascendc/' },
      { text: '第四编 · 性能优化', link: '/04-perf/' },
      { text: '第五编 · 分布式通信', link: '/05-comm/' },
      { text: '第六编 · 现代编译后端', link: '/06-backend/' },
      { text: '第七编 · 展望', link: '/07-outlook/' },
      { text: '附录', link: '/附录/' }
    ],
    sidebar,
    outline: { level: [2, 3], label: '本页目录' },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索' },
          modal: { noResultsText: '未找到相关结果', resetButtonTitle: '清除', footer: { selectText: '选择', navigateText: '切换' } }
        }
      }
    },
    docFooter: { prev: '上一章', next: '下一章' },
    lastUpdated: { text: '最后更新于', formatOptions: { dateStyle: 'short', timeStyle: 'short' } },
    editLink: { pattern: 'https://github.com/hb4ch/ascend-book/blob/main/:path', text: '在本仓查看源码' },
    footer: {
      message: '《昇腾平台技术实战》· 基于 CANN Open 开源仓写作，内容以源码为准'
    }
  }
})
