from typing import TYPE_CHECKING, Union, List, Optional

from .Cstatement import CStatement, CStatements, CCompoundStatement
from .Cjump import CBreak

if TYPE_CHECKING:
    from ..expressions import CExpression
    from ..style import Style


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

        if self.c_else is not None:
            content += self.c_else.render(style)

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

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.if_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_if_content

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"if"
            f"{style.space(style.if_space_after_token)}"
            f"{style.open_parentheses(style.if_parentheses)}"
            f"{self.condition.render(style)}"
            f"{style.close_parentheses(style.if_parentheses)}"
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

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.else_if_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_else_if_content

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"else if"
            f"{style.space(style.else_if_space_after_token)}"
            f"{style.open_parentheses(style.else_if_parentheses)}"
            f"{self.condition.render(style)}"
            f"{style.close_parentheses(style.else_if_parentheses)}"
        )


class CElse(CCompoundStatement):
    _style_token = "else"

    def __init__(self, statements: Union['CStatements', List['CStatement']]):
        super(CElse, self).__init__(statements)

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.else_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_else_content

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"else"
            f"{style.space(style.else_space_after_token)}"
        )


class CCaseSwitch(CStatement):

    def __init__(self,
                 match_expression: Optional['CExpression'],
                 statements: Union['CStatements', List['CStatement']],
                 auto_break: bool = True
                 ):
        self.match_expression = match_expression
        if isinstance(statements, CStatements):
            self.statements = statements
        else:
            self.statements = CStatements(statements)

        self.auto_break = auto_break
        super(CCaseSwitch, self).__init__(self._render_function)

    def _all_statements(self) -> 'CStatements':
        statements = CStatements([self.statements])
        if self.auto_break is not None:
            statements.append(CBreak())
        return statements

    def _header(self, style: 'Style') -> str:
        if self.match_expression is None:
            raise ValueError("Cannot render switch statement without a match_expression")
        return f"case {self.match_expression.render(style)}:"

    def _render_function(self, style: 'Style') -> str:
        return (
            f"{self._header(style)}"
            f"{style.new_line_token}"
            f"{style.indent(self._all_statements().render(style), style.indent_case_switch_content)}"
        )


class CDefaultCaseSwitch(CCaseSwitch):
    def __init__(self,
                 statements: Union['CStatements', List['CStatement']],
                 auto_break: bool = True
                 ):
        super(CDefaultCaseSwitch, self).__init__(
            match_expression=None,
            statements=statements,
            auto_break=auto_break
        )

    def _header(self, style: 'Style') -> str:
        return "default:"


class CSwitch(CCompoundStatement):
    Case = CCaseSwitch
    Default = CDefaultCaseSwitch

    _style_token = "switch"

    def __init__(self, value: 'CExpression', cases: List[CCaseSwitch]):
        self.value = value
        super(CSwitch, self).__init__(
            CStatements(cases)
        )

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.switch_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_switch_content

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"{self._style_token}"
            f"{style.space(style.switch_space_after_token)}"
            f"{style.open_parentheses(style.switch_parentheses)}"
            f"{self.value.render(style)}"
            f"{style.close_parentheses(style.switch_parentheses)}"
        )
