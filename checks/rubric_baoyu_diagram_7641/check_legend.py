"""rubric「海报是否包含图例」：文本里必须出现『图例』字样。"""

from checks.checker import Checker


class LegendChecker(Checker):
    name = "legend"

    def check_content(self, text, meta):
        if "图例" in text:
            return {"ok": True, "name": self.name, "detail": "命中『图例』"}
        return {"ok": False, "name": self.name, "detail": "未提到『图例』"}
