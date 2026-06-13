"""模板 6：数值在合理区间内 / 不出现负值。

适用场景：rubric 直接给了数值边界，或者要求『剔除负值/异常值』之类。
比如：
- 价格区间应在 [200, 5000] 元
- 年龄字段应在 [0, 120]
- 报告里『不能出现负数』『统计表无 -999 之类哨兵值』

要点：用一个简单的正则把所有数字捞出来，再判区间。这里给的是『所有出现的数字必须 ≥ 0』的例子。

⚠️ 局限：纯正则会把『2026-020』『编号-001』里的『-020』『-001』也当成负数。如果产物里
有大量这种连字符编号，把这条 check 当成『提醒人去看一下』的信号就好，不要把它配成必过项；
或者根据自己产物的特点把正则收紧（比如要求负号前是空白/标点）。
"""

import re

from checks.checker import Checker


# 提取整数 / 小数 / 负数（含可能的负号）。
# 这里没收紧到「负号前必须是行首/空白/标点」——刻意保持简单，方便 reader 看懂；
# 真要避免编号噪声，把 r"-?" 换成 r"(?:(?<![\w-])-)?" 之类。
_NUM = re.compile(r"-?\d+(?:\.\d+)?")


class NoNegativeNumbersChecker(Checker):
    name = "no-negative-numbers"

    def check_content(self, text, meta):
        bad = []
        for m in _NUM.finditer(text):
            try:
                v = float(m.group())
            except ValueError:
                continue
            if v < 0:
                bad.append(m.group())
                if len(bad) >= 5:    # 不必把所有违规都列出来；列前几个够定位
                    break
        if bad:
            return {"ok": False, "name": self.name, "detail": f"出现负值（前几个）：{bad}"}
        return {"ok": True, "name": self.name, "detail": "未发现负值"}
