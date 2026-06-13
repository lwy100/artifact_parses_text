"""模板 4：『禁止出现』黑名单。

适用场景：rubric 是反向约束 ——『不允许出现 X』。
比如：
- 选型气泡里『不能写具体设备型号』
- 报告『不要给我 Mermaid/Markdown 代码』
- 决策树『不要出现 TBD / 待定 / TODO』占位

要点：FORBIDDEN 里写所有不允许的子串；任一命中即 fail，detail 列出所有命中的。
"""

from checks.checker import Checker


FORBIDDEN = ["TBD", "TODO", "待定", "占位"]


class ForbiddenKeywordsChecker(Checker):
    name = "forbidden-keywords"

    def check_content(self, text, meta):
        hits = [w for w in FORBIDDEN if w in text]
        if hits:
            return {"ok": False, "name": self.name, "detail": f"命中禁词：{hits}"}
        return {"ok": True, "name": self.name, "detail": f"无禁词出现：{FORBIDDEN}"}
