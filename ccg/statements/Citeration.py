from typing import TYPE_CHECKING, Union, List

from .Cstatement import CStatement, CStatements, CCompoundStatement

if TYPE_CHECKING:
    from ..expressions import CExpression
    from ..style import Style


class CWhile(CCompoundStatement):
    _style_token = "while"

    def __init__(self, condition: 'CExpression', statements: Union['CStatements', List['CStatement']]):
        self.condition = condition
        super(CWhile, self).__init__(statements)

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.while_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_while_content

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"{self._style_token}"
            f"{style.open_parentheses(style.while_bracket)}"
            f"{self.condition.render(style)}"
            f"{style.close_parentheses(style.while_bracket)}"
        )


class CDoWhile(CCompoundStatement):
    _style_token = "do_while"

    def __init__(self, statements: Union['CStatements', List['CStatement']], condition: 'CExpression'):
        self.condition = condition
        super(CDoWhile, self).__init__(statements)

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.do_while_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_do_while_content

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"do"
        )

    def _post_block(self, style: 'Style') -> str:
        return (
            f"while"
            f"{style.open_parentheses(style.do_while_bracket)}"
            f"{self.condition.render(style)}"
            f"{style.close_parentheses(style.do_while_bracket)}"
        )


class CFor(CCompoundStatement):
    _style_token = "for"

    def __init__(self,
                 initial: Union['CStatement', 'CExpression', None] = None,
                 condition: Union['CExpression', None] = None,
                 iteration: Union['CExpression', None] = None,
                 statements: Union['CStatements', List['CStatement'], None] = None
                 ):
        self.initial = initial
        self.condition = condition
        self.iteration = iteration

        if statements is None:
            statements = CStatements([])

        super(CFor, self).__init__(statements)

    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        return style.for_bracket

    def _indent_content_style(self, style: 'Style') -> bool:
        return style.indent_for_content

    def _pre_block(self, style: 'Style') -> str:
        delimiter = (
            f"{style.space(style.for_space_before_semicolon)}"
            f";"
            f"{style.space(style.for_space_after_semicolon)}"
        )
        return (
            f"for"
            f"{style.open_parentheses(style.for_bracket)}"
            f"{self.initial.render(style) if self.initial is not None else ''}"
            f"{delimiter}"
            f"{self.condition.render(style) if self.condition is not None else ''}"
            f"{delimiter}"
            f"{self.iteration.render(style) if self.iteration is not None else ''}"
            f"{style.close_parentheses(style.for_bracket)}"
        )
