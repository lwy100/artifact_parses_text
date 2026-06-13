"""模板 2：关键词集合『必须全部出现』。

适用场景：rubric 列了一组术语 / 要素 / 节点名，要求产物里每一项都得有。
比如：
- 三档落点「基础看护 / 标准安防 / 全面守护」三个都要出现
- 三层架构「感知层 / 网络层 / 应用层」三个都要出现
- 报告结构「摘要 / 结论 / 附录」三个章节都要有

要点：把 REQUIRED 改成你那一组词；fail 时 detail 直接列出缺哪几个，方便定位。
"""

from checks.checker import Checker


REQUIRED = ["基础看护", "标准安防", "全面守护"]


class AllKeywordsPresentChecker(Checker):
    name = "all-keywords-present"

    def check_content(self, text, meta):
        missing = [w for w in REQUIRED if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"缺少：{missing}"}
        return {"ok": True, "name": self.name, "detail": f"全部命中：{REQUIRED}"}
