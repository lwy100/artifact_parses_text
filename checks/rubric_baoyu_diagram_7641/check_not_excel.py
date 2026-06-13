"""rubric「产物是否不是Excel格式」：后缀不能是 .xls/.xlsx。"""

from checks.checker import Checker


class NotExcelChecker(Checker):
    name = "not-excel"

    def check_filename(self, file_name, meta):
        lower = file_name.lower()
        if lower.endswith(".xlsx") or lower.endswith(".xls"):
            return {"ok": False, "name": self.name, "detail": f"产物是 Excel 格式：{file_name}"}
        return {"ok": True, "name": self.name, "detail": file_name}
