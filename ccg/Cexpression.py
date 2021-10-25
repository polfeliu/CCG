from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional
from .style import default_style

if TYPE_CHECKING:
    from .Ctypes import CGenericType
    from .style import Style


class CExpression(ABC):

    @abstractmethod
    def render(self, style: 'Style' = default_style) -> str:
        raise NotImplemented


class CExpressionFreeStyle(CExpression):

    def __init__(self, content: str):
        self.content = content

    def render(self, style: 'Style' = default_style) -> str:
        return self.content


class CCast(CExpression):

    def __init__(self, type: 'CGenericType', expression: CExpression):
        super(CCast, self).__init__()
        self.type = type
        self.expression = expression

    def render(self, style: 'Style' = default_style) -> str:
        return (
            f"({self.type.name})"
            f"{style.vspace_after_cast}"
            f"{self.expression.render()}"
        )
