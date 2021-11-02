from typing import TYPE_CHECKING

from ccg import CExpression, default_style

if TYPE_CHECKING:
    from ccg import CGenericType, Style


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
