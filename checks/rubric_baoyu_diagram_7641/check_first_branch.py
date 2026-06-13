"""rubric「主决策树第一层分叉为跌倒报警选型」：四类技术都要出现。"""

from checks.checker import Checker


class FirstBranchChecker(Checker):
    name = "first-branch"

    def check_content(self, text, meta):
        required = ["毫米波雷达", "AI摄像头", "穿戴设备", "红外感应"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"第一层分叉缺：{missing}"}
        return {"ok": True, "name": self.name, "detail": "四类跌倒报警技术齐全"}
