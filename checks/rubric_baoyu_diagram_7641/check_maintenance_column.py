"""rubric「维护提醒侧栏：5年总拥有成本/年均维护费/电池更换周期」三个维度必须都出现。"""

from checks.checker import Checker


class MaintenanceColumnChecker(Checker):
    name = "maintenance-column"

    def check_content(self, text, meta):
        required = ["5年总拥有成本", "年均维护费", "电池更换周期"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"维护提醒侧栏缺：{missing}"}
        return {"ok": True, "name": self.name, "detail": "5年成本 / 年均维护费 / 电池周期 齐全"}
