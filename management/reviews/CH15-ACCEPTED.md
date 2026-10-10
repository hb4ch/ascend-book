# 第15章源码、文稿与图检验收
经理独立读取固定版本Softmax实际四循环390–441及初始化常数，CPU math/struct复算全负有限行、极负行和全-inf边界，明确区别数学参考与NPU行为；正文已撤共享Load和错误下溢保证，官方cycles保留来源不作本机或单因果归因。
逐轮检查实际正文、表、摘要、脚注，亲自纠正剩余标题/alt/图注；最终两图独立重新截图并实际目检ch15-manager-case.png与ch15-manager-ladder.png，修正屏障位置②③、溢出与倍率。
独立verify83099真实exit0（ch15-manager-final.log）；最后图文本调整后docs:build29180真实exit0（ch15-manager-build.log）；截图脚本88829真实exit0；指定文件diff --check通过。
范围：第15章正文、ch15-case1v2.svg、ch15-ladder.svg。没有CANN编译、NPU或仿真实测。全书最终一致性审查另行进行。
