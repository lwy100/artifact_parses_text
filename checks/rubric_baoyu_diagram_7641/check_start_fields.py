"""rubric「路径起点是否包含老人年龄/是否独居/户型/预算」：4 个起始信息维度都要在文本中出现。"""

from checks.checker import Checker


class StartFieldsChecker(Checker):
    name = "start-fields"

    def check_content(self, text, meta):
        required = ["年龄", "独居", "户型", "预算"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"缺少起点字段：{missing}"}
        return {"ok": True, "name": self.name, "detail": "命中：年龄 / 独居 / 户型 / 预算"}
