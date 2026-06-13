"""rubric「三层架构带：感知层/网络层/应用层」必须都出现。"""

from checks.checker import Checker


class ThreeLayersChecker(Checker):
    name = "three-layers"

    def check_content(self, text, meta):
        required = ["感知层", "网络层", "应用层"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"三层架构缺：{missing}"}
        return {"ok": True, "name": self.name, "detail": "感知层 / 网络层 / 应用层 齐全"}
