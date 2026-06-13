"""rubric「三个落点：基础看护/标准安防/全面守护」必须都出现。"""

from checks.checker import Checker


class ThreeTiersChecker(Checker):
    name = "three-tiers"

    def check_content(self, text, meta):
        required = ["基础看护", "标准安防", "全面守护"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"缺少落点：{missing}"}
        return {"ok": True, "name": self.name, "detail": "命中：基础看护 / 标准安防 / 全面守护"}
