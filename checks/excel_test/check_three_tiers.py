"""rubric「敏感性预测必须包含 3 档：低档 10% / 中档 12% / 高档 20%」。

档位关键词 + 百分比都得出现，避免只有"低/中/高"三个字而没标具体百分比的情况。
"""

from checks.checker import Checker


REQUIRED = ["低档", "中档", "高档", "10%", "12%", "20%"]


class ThreeTiersChecker(Checker):
    name = "three-tiers"

    def check_content(self, text, meta):
        missing = [w for w in REQUIRED if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"敏感性档位缺关键词：{missing}"}
        return {"ok": True, "name": self.name, "detail": "低档10% / 中档12% / 高档20% 齐全"}
