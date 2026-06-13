"""rubric「报告必须覆盖 4 个业务场景」：4 个场景名都得在文本里出现。"""

from checks.checker import Checker


REQUIRED = [
    "售后维修工单问答2",
    "设备运维手册检索",
    "质检报告摘要生成",
    "集团制度与EHS规程检索",
]


class FourScenariosChecker(Checker):
    name = "four-scenarios"

    def check_content(self, text, meta):
        missing = [w for w in REQUIRED if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"缺业务场景：{missing}"}
        return {"ok": True, "name": self.name, "detail": "4 个业务场景齐全"}
