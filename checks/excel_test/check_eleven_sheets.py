"""rubric「报告必须包含 11 个 Sheet」：靠 parser 在每个 sheet 之前注入的 `## sheet:` 行计数。

parse_and_check.py 的 xlsx parser 对每个 sheet 都会写一行 `## sheet: <name>`，所以这里
直接计数 + 校验关键 sheet 名是否齐全。
"""

from checks.checker import Checker


REQUIRED_SHEETS = [
    "封面",
    "原始数据",
    "数据清洗",
    "历史趋势",
    "预测明细_中档",
    "预测明细_低档",
    "预测明细_高档",
    "敏感性对比",
    "Token",
    "可视化",
    "关键结论",
]


class ElevenSheetsChecker(Checker):
    name = "eleven-sheets"

    def check_content(self, text, meta):
        sheet_lines = [ln for ln in text.splitlines() if ln.startswith("## sheet:")]
        joined = "\n".join(sheet_lines)
        missing = [kw for kw in REQUIRED_SHEETS if kw not in joined]
        if len(sheet_lines) < 11:
            return {"ok": False, "name": self.name,
                    "detail": f"sheet 数 {len(sheet_lines)} < 11，且缺关键词 {missing}"}
        if missing:
            return {"ok": False, "name": self.name, "detail": f"sheet 名缺：{missing}"}
        return {"ok": True, "name": self.name, "detail": f"sheet 数 {len(sheet_lines)}，关键 sheet 齐全"}
