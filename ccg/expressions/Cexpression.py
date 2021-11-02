from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from ccg import default_style

if TYPE_CHECKING:
    from ccg import Style


class CExpression(ABC):

    @abstractmethod
    def render(self, style: 'Style' = default_style) -> str:
        raise NotImplemented


class CExpressionFreeStyle(CExpression):

    def __init__(self, content: str):
        self.content = content

    def render(self, style: 'Style' = default_style) -> str:
        return self.content
