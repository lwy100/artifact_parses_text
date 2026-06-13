"""rubric「关键结论 Sheet 必须给出 ≥ 5 条编号结论」。

报告里结论是用 `【结论N·...】` 这种格式标注的；数一下出现次数即可。
"""

import re

from checks.checker import Checker


_CONCLUSION = re.compile(r"【结论\d")
MIN_COUNT = 5


class FiveConclusionsChecker(Checker):
    name = "five-conclusions"

    def check_content(self, text, meta):
        n = len(_CONCLUSION.findall(text))
        if n < MIN_COUNT:
            return {"ok": False, "name": self.name,
                    "detail": f"编号结论只有 {n} 条，少于 {MIN_COUNT}"}
        return {"ok": True, "name": self.name, "detail": f"共 {n} 条编号结论，达标"}
