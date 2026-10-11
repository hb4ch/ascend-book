# 第20章验算标签修正验收（2026-10-11）
仅将场景7/8的“场景实测”改成“按样例参数验算”。经理直接核查固定 asc-devkit 源仓 data_copy/README.md 365–372 行：A2 M6144/tile128/block48，950 M8192/tile128/block64；CPU除法复算48、64。没有运行NPU benchmark，不改变原性能数据和适用边界。
独立 npm run verify session78220 exit0，日志 ch01-ch20-manager-final.log；最终 git diff --check 通过。仅提交本章单行修订及本记录。
