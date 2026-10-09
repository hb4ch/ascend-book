# CH24 验收记录

2026-10-10。经理完整读取初稿与R1正文，回源核CMake根路径、TileLeft分支、CPU TLOAD、a2a3 CheckStaticMad、MoE事件实际代码；接管修正cTile32×32float=4096B、事件状态与half转换、反引号及图形裁切后验收。

验证：ch24-r1-configure/build/run日志记录新目录完整CPU构建运行，max_abs_diff=1.19209e-07；经理完整verify退出0，日志ch24-manager-verify.log。bash语法检查通过；图①数据流实际查看，图②经理重渲染ch24-manager-layout.png，图③真实站点ch24-manager-mermaid2.png目检通过。标签存在检查不足以代替视觉检查，原图裁切已修。git diff --check通过。

边界：CPU示例与参考数值对拍，仅涵盖该输入；未NPU编译运行、不保证设备精度时序或性能。A5容量placeholder、CostModel和通信实现未展开；别名分支只证明类型布局差异。历史研究报告错误以最终正文为准。接受短章以单例解释，不靠字数填充。
