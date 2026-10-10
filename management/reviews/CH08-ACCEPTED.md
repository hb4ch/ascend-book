# 第8章验收（2026-10-11）
经理已全文复核正文及固定源仓：单条MemcpyAsync非锁页返回语义见runtime内存复制文档140/213；L2粒度见basic_architecture113/206；UB到L1接口支持范围与物理通路分开，Host复用等待与设备StreamWait区分，双缓冲不等于自动重叠。无NPU实测声明。
实际查看ch08-final-render-640-hierarchy.png及ch08-final-render-640-mte-units.png，两图文字可读，Cube/Vector两路、FixPipe回路与架构限定一致。旧ch08-final-640截图为过期图，不作为验收依据。
经理独立npm run verify会话25452真实exit0；日志management/validation/ch08-appd-manager-final.log。验收范围正文及两幅SVG。
