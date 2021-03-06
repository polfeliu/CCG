from typing import TYPE_CHECKING

from .Cexpression import CExpression
from ..style import default_style

if TYPE_CHECKING:
    from ..types.Ctypes import CGenericType
    from ..style import Style


class CCast(CExpression):
    """Explicit type cast"""

    def __init__(self, c_type: 'CGenericType', expression: CExpression):
        super(CCast, self).__init__()
        self.c_type = c_type
        self.expression = expression

    def render(self, style: 'Style' = default_style) -> str:
        return (
            f"({self.c_type.name})"
            f"{style.space(style.space_after_cast)}"
            f"{self.expression.render(style)}"
        )
