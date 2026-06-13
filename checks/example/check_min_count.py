"""模板 5：数量阈值（行数 / 段数 / 关键词次数 ≥ N）。

适用场景：rubric 用『至少』『不少于 N』『至少四类』等量词。
比如：
- 至少 4 类风险（rubric: 跌倒/火灾/燃气/入室）
- 至少 3 个章节标题（# 开头的行 ≥ 3）
- 关键词出现 ≥ 5 次（衡量信息密度）

要点：MIN_COUNT 改阈值，COUNT_OF 改要数什么。这里给的是『以 # 开头的行数』示例 —— 数标题。
"""

from checks.checker import Checker


MIN_COUNT = 3


class MinHeadingCountChecker(Checker):
    name = "min-heading-count"

    def check_content(self, text, meta):
        n = sum(1 for line in text.splitlines() if line.lstrip().startswith("#"))
        if n < MIN_COUNT:
            return {"ok": False, "name": self.name,
                    "detail": f"标题行只有 {n} 个，少于阈值 {MIN_COUNT}"}
        return {"ok": True, "name": self.name, "detail": f"标题行 {n} 个，达标"}
