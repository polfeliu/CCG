from typing import TYPE_CHECKING, Union, List, Optional

from .Cstatement import CStatement, CStatements

if TYPE_CHECKING:
    from ..expressions import CExpression
    from ..style import Style


class CCompoundStatement(CStatement):  # TODO this is not exclusive for selection
    _style_token: Union[str, None] = None

    def __init__(self, statements: Union['CStatements', List['CStatement']]):
        if isinstance(statements, CStatements):
            self.statements = statements
        else:
            self.statements = CStatements(statements)
        super(CCompoundStatement, self).__init__(self._render_function)

    def _render_function(self, style: 'Style') -> str:
        content = self.statements.render()
        if self._style_token is not None:
            content = style.indent(content, self._style_token + '_content')

        return (
            f"{self._pre_block(style)}"
            f"{style.bracket_open(self._style_token) if self._style_token is not None else '{'}"
            f"{content}"
            f"{style.bracket_close(self._style_token) if self._style_token is not None else '}'}"
            f"{self._post_block(style)}"
        )

    def _pre_block(self, style: 'Style') -> str:
        return ""

    def _post_block(self, style: 'Style') -> str:
        return ""


class CIfLadder(CStatement):
    """Array of if, else if and else statements"""

    def __init__(self, c_if: 'CIf', c_else_ifs: Optional[List['CElseIf']], c_else: Optional['CElse'] = None):
        super(CIfLadder, self).__init__(self._render_function)
        self.c_if = c_if
        if c_else_ifs is None:
            self.c_else_ifs = []
        else:
            self.c_else_ifs = c_else_ifs
        self.c_else = c_else

    def _render_function(self, style: 'Style') -> str:
        content = self.c_if.render(style)
        for c_else_if in self.c_else_ifs:
            content += c_else_if.render(style)

        content += self.c_else.render()
        return content

    def ELSE_IF(self, condition: 'CExpression', statements: Union['CStatements', List['CStatement']]) -> 'CIfLadder':
        self.c_else_ifs.append(CElseIf(condition, statements))
        return self

    def ELSE(self, statements: Union['CStatements', List['CStatement']]) -> 'CIfLadder':
        self.c_else = CElse(statements)
        return self


class CIf(CCompoundStatement):
    _style_token = "if"

    def __init__(self, condition: 'CExpression', statements: Union['CStatements', List['CStatement']]):
        self.condition = condition
        super(CIf, self).__init__(statements)

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"if"
            f"{style.parentheses_open(self._style_token)}"
            f"{self.condition.render()}"
            f"{style.parentheses_close(self._style_token)}"
        )

    def ELSE_IF(self, condition: 'CExpression', statements: Union['CStatements', List['CStatement']]) -> 'CIfLadder':
        return CIfLadder(
            c_if=self,
            c_else_ifs=[CElseIf(condition, statements)]
        )

    def ELSE(self, statements: Union['CStatements', List['CStatement']]) -> 'CIfLadder':
        return CIfLadder(
            c_if=self,
            c_else_ifs=None,
            c_else=CElse(statements)
        )


class CElseIf(CIf):
    _style_token = "else_if"

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"else if"
            f"{style.parentheses_open(self._style_token)}"
            f"{self.condition.render()}"
            f"{style.parentheses_close(self._style_token)}"
        )


class CElse(CCompoundStatement):
    _style_token = "else"

    def __init__(self, statements: Union['CStatements', List['CStatement']]):
        super(CElse, self).__init__(statements)

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"else"
        )
