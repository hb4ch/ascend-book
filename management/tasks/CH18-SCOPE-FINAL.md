# 第18章最终主线条件核查（暂停正文写入）

经理接管正文/图收尾。你暂不改正文/图/appD，不提交推送，保持原模型。只交付management/CH18-SCOPE-FINAL.md。
重大新发现：经理亲读common_regbase_arch35.h IsDn(172–188)：fp16、无可选输入、s1!=64、d<=256、无rope会返回true。因此R3给出的fp16/s1=s2=128/D256/无可选输入实际上useDn=true，并不是正文宣称的Nd！不要再次只修D而不沿全部条件。
请给一个真正Nd且GM、非splitD的明确模板组合，并逐式代入IsDn、UbOutCondition、GetC2Position、useNz、splitD、optionalDn。例如hasAtten=true可能使IsDn=false并仍GM，但必须确认完整条件，然后确认mm1对应Fixpipe分支的dtype（不拿Dn真码当Nd）。若必须启用mask，给一个具体mask设定及其实际VF分支，保留主体假设限制，不能声称自动host选择已验证。
交付短而精确：所有实参表、条件代入、实际mm1出口函数与quantPre、mm2出口、vec1入口、vec2入口。源短摘录支持结论，禁止只“已证”两字。报告完成等待经理。此后再派第19章，先把这一个条件钉死。
