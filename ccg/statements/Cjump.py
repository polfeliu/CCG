from typing import TYPE_CHECKING

from .Cstatement import CTokenStatement

if TYPE_CHECKING:
    from ..style import Style
    from ..expressions import CExpression


class CBreak(CTokenStatement):
    _token = "break"

    def _semicolon_before_space(self, style: 'Style') -> bool:
        return style.space_before_semicolon_break_statement


class CContinue(CTokenStatement):
    _token = "continue"

    def _semicolon_before_space(self, style: 'Style') -> bool:
        return style.space_before_semicolon_continue_statement


class CReturn(CTokenStatement):
    _token = "return"

    def _semicolon_before_space(self, style: 'Style') -> bool:
        return style.space_before_semicolon_return_statement

    def __init__(self, expression: 'CExpression'):
        super(CReturn, self).__init__()
        self.expression = expression

    def _post_block(self, style: 'Style') -> str:
        return f" {self.expression.render(style)}"
