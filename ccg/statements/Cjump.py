from typing import TYPE_CHECKING

from .Cstatement import CTokenStatement

if TYPE_CHECKING:
    from ..style import Style
    from ..expressions import CExpression


class CBreak(CTokenStatement):
    _token = "break"


class CContinue(CTokenStatement):
    _token = "continue"


class CReturn(CTokenStatement):
    _token = "return"

    def __init__(self, expression: 'CExpression'):
        super(CReturn, self).__init__()
        self.expression = expression

    def _post_block(self, style: 'Style') -> str:
        return f" {self.expression.render(style)}"
