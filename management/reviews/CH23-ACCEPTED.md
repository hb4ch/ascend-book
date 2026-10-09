# CH23 验收记录

2026-10-10，经理独立审读最终正文、实际查看ch23-r3-fig1/2/3.png，接受本章。

主要核查：产品支持以MatmulAllReduce README为准；setUseBufferType实际排除DAV_2002/ONLY_AICPU/reuse关闭/K零，严格容量比较，kernel另查determinism；混核notify为AIV0；Commit提交与server完成分开；Finalize正常单handle同步路径可闭合，多handle未证明。MoE限制仅四辅助张量，arch35入口实际实例化共享头。正文避免将目录存在或路径校验当论断正确。

验证：ch23-release-verify.log完整通过（exec exit 0）；ch23-manager-bashn.log通过；三图正文宽度已目检可读，图③仅计数示例不证明重叠时序。git diff --check通过。

边界：未进行NPU构建运行和性能测量；AICPU server内部消费、CCU算法、A2分层MoE协议未逐行证明。字数按用户可读性要求豁免，不堆变体。R1/R2/R3报告属历史，残留错误以最终正文及本记录为准。
