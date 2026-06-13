"""把 ``checks`` 暴露成一个包，让校验脚本里可以直接
``from checks.checker import Checker``。"""

from .checker import Checker

__all__ = ["Checker"]
