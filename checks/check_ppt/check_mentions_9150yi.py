"""检查解析后的文本里有没有『9150亿』。"""

from checks.checker import Checker


class Mentions9150yiChecker(Checker):
    name = "mentions-9150yi"

    def check_content(self, text, meta):
        if "9150 亿" in text:
            return {"ok": True, "name": self.name, "detail": "命中 '9150亿'"}
        return {"ok": False, "name": self.name, "detail": "没找到 '9150亿'"}
