"""rubric「指定推荐主路径：卧室+卫生间各1个雷达，床头+卫生间各1个按钮」必须出现。"""

from checks.checker import Checker


class RecommendedPathChecker(Checker):
    name = "recommended-path"

    def check_content(self, text, meta):
        # 主路径里 4 个布点要素都得提到
        required = ["卧室", "卫生间", "雷达", "床头", "按钮"]
        missing = [w for w in required if w not in text]
        if missing:
            return {"ok": False, "name": self.name, "detail": f"推荐主路径缺关键词：{missing}"}
        return {"ok": True, "name": self.name, "detail": "卧室/卫生间/雷达/床头/按钮 齐全"}
