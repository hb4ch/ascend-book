// 全书侧边导航：每一编一个分组，章节按逻辑顺序排列。
// 章节文件命名规范：chNN-<english-slug>.md，中文标题写在 frontmatter 的 title 中。
export const sidebar = {
  '/00-导读/': [
    { text: '导读', items: [{ text: '导言：如何使用本书', link: '/' }] }
  ],

  '/01-platform/': [
    {
      text: '第一编 昇腾平台全景',
      items: [
        { text: '编导语', link: '/01-platform/' },
        { text: '第1章 昇腾平台与生态总览', link: '/01-platform/ch01-overview' },
        { text: '第2章 昇腾硬件体系结构', link: '/01-platform/ch02-hardware' },
        { text: '第3章 软件栈执行主链路', link: '/01-platform/ch03-exec-path' }
      ]
    }
  ],

  '/02-runtime/': [
    {
      text: '第二编 运行时、驱动与维测底层',
      items: [
        { text: '编导语', link: '/02-runtime/' },
        { text: '第4章 ACL 编程接口', link: '/02-runtime/ch04-acl' },
        { text: '第5章 运行时核心实现', link: '/02-runtime/ch05-runtime-impl' },
        { text: '第6章 驱动与系统软件协同', link: '/02-runtime/ch06-driver' },
        { text: '第7章 维测子系统 DFX', link: '/02-runtime/ch07-dfx' },
        { text: '第8章 内存与数据通路', link: '/02-runtime/ch08-memory' }
      ]
    }
  ],

  '/03-ascendc/': [
    {
      text: '第三编 算子开发：Ascend C',
      items: [
        { text: '编导语', link: '/03-ascendc/' },
        { text: '第9章 编程模型与 API 选择', link: '/03-ascendc/ch09-api-map' },
        { text: '第10章 核心编程能力详解', link: '/03-ascendc/ch10-core-programming' },
        { text: '第11章 SIMD/SIMT 与高级特性', link: '/03-ascendc/ch11-simd-simt' },
        { text: '第12章 编译、工具链与部署', link: '/03-ascendc/ch12-compile-tools' },
        { text: '第13章 算子库体系', link: '/03-ascendc/ch13-operator-libs' },
        { text: '第14章 经典算子实战（端到端）', link: '/03-ascendc/ch14-op-practice' }
      ]
    }
  ],

  '/04-perf/': [
    {
      text: '第四编 性能优化方法论',
      items: [
        { text: '编导语', link: '/04-perf/' },
        { text: '第15章 性能分析与瓶颈定位', link: '/04-perf/ch15-perf-analysis' },
        { text: '第16章 优化技术专题', link: '/04-perf/ch16-opt-topics' }
      ]
    }
  ],

  '/05-comm/': [
    {
      text: '第五编 分布式通信',
      items: [
        { text: '编导语', link: '/05-comm/' },
        { text: '第17章 HCCL 集合通信', link: '/05-comm/ch17-hccl' },
        { text: '第18章 HIXL 单边通信', link: '/05-comm/ch18-hixl' },
        { text: '第19章 通算融合与大规模系统', link: '/05-comm/ch19-supernode' }
      ]
    }
  ],

  '/06-backend/': [
    {
      text: '第六编 现代编译后端与编程范式',
      items: [
        { text: '编导语', link: '/06-backend/' },
        { text: '第20章 PTO 虚拟 ISA', link: '/06-backend/ch20-pto-isa' },
        { text: '第21章 PyPTO 框架深入', link: '/06-backend/ch21-pypto' },
        { text: '第22章 生态与前沿编译技术', link: '/06-backend/ch22-ecosystem' },
        { text: '第23章 全栈综合案例（可选）', link: '/06-backend/ch23-case' }
      ]
    }
  ],

  '/07-outlook/': [
    {
      text: '第七编 展望与总结',
      items: [
        { text: '编导语', link: '/07-outlook/' },
        { text: '第24章 路线图与展望', link: '/07-outlook/ch24-roadmap' }
      ]
    }
  ],

  '/附录/': [
    {
      text: '附录',
      items: [
        { text: '附录索引', link: '/附录/' },
        { text: '附录A 环境搭建', link: '/附录/appA-env' },
        { text: '附录B 术语表', link: '/附录/appB-glossary' },
        { text: '附录C 资源索引', link: '/附录/appC-resources' },
        { text: '附录D 来源映射表', link: '/附录/appD-source-map' }
      ]
    }
  ]
}
