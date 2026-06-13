"""模板 3：关键词集合『至少出现一个』。

适用场景：rubric 给了一组同义/同类的近义表达，只要任意一种说法出现就算过。
比如：
- 文末有"结论 / 结语 / 总结" 任一即算有结论段
- 海报有"图例 / Legend / 说明" 任一即算有图例
- 报告里出现 "5G / 6G / 移动通信" 任一即算覆盖了通信议题

要点：和"全部出现"是镜像。同义词宽容用 any-of，硬性多要素清单用 all-of。
"""

from checks.checker import Checker


CANDIDATES = ["结论", "结语", "总结"]


class AnyKeywordPresentChecker(Checker):
    name = "any-keyword-present"

    def check_content(self, text, meta):
        hit = next((w for w in CANDIDATES if w in text), None)
        if hit is None:
            return {"ok": False, "name": self.name, "detail": f"任一关键词都未命中：{CANDIDATES}"}
        return {"ok": True, "name": self.name, "detail": f"命中『{hit}』"}
