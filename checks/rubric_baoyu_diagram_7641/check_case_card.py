"""rubric「真实案例卡」：北京朝阳区/78岁/60㎡/2800元/3秒/15分钟 六个特征关键词都要出现。"""

from checks.checker import Checker


class CaseCardChecker(Checker):
    name = "case-card"

    def check_content(self, text, meta):
        required = ["朝阳", "78", "60", "2800", "3秒", "15分钟"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"案例卡缺关键词：{missing}"}
        return {"ok": True, "name": self.name, "detail": "案例卡六要素齐全"}
