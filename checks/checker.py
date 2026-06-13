"""校验脚本的基类。

每个 ``--script`` 文件定义一个 :class:`Checker` 子类，按需改写以下方法之一：

* :meth:`check_filename` —— 只看附件文件名，不需要解析后的文本。
* :meth:`check_content` —— 看解析后的文本。

主脚本 ``parse_and_check.py`` 在加载脚本时挑出唯一一个 ``Checker`` 子类，
无参实例化后按"哪个方法被改写过"决定调谁。

每项 check 返回一个结果 dict::

    {
        "ok": bool,                # 必填
        "name": "<short id>",      # 可选，默认取 checker.name
        "detail": "<给人看的说明>", # 可选
    }

为了向后兼容，老的 ``def check(text, meta) -> dict`` 模块级函数仍然能用：
当文件里没有 ``Checker`` 子类时，主脚本会回退去找这个函数。
"""

from __future__ import annotations

from typing import Any


class Checker:
    """校验项基类。子类按需改写 :meth:`check_filename` 或 :meth:`check_content`，
    两者必须二选一，同时改写会被加载器拒绝。"""

    #: 在 stdout 标签和 report.json 里使用的短标识；当 check 结果里没给
    #: ``name`` 时会用它兜底。默认从子类名去掉 ``Checker`` 后缀再小写。
    name: str = ""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # 只在子类自己没显式定义 name 时才自动派生，避免误继承父类的值。
        if "name" not in cls.__dict__ or not cls.__dict__["name"]:
            stem = cls.__name__
            if stem.endswith("Checker"):
                stem = stem[: -len("Checker")]
            cls.name = stem.lower() or cls.__name__.lower()

    def check_filename(self, file_name: str, meta: dict) -> dict:
        """检查附件文件名。子类如果要做文件名检查就改写本方法。"""
        raise NotImplementedError

    def check_content(self, text: str, meta: dict) -> dict:
        """检查解析后的文本。子类如果要做内容检查就改写本方法。"""
        raise NotImplementedError

    def __call__(self, text: str, meta: dict) -> dict:
        cls = type(self)
        has_filename = cls.check_filename is not Checker.check_filename
        has_content = cls.check_content is not Checker.check_content

        if has_filename and has_content:
            raise RuntimeError(
                f"{cls.__name__} 同时改写了 check_filename 和 check_content，"
                "请只改写其中一个"
            )
        if has_filename:
            return self.check_filename(meta["file_name"], meta)
        if has_content:
            return self.check_content(text, meta)
        raise RuntimeError(
            f"{cls.__name__} 必须改写 check_filename 或 check_content 之一"
        )


__all__ = ["Checker"]
