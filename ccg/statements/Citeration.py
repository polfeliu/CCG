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

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"{self._style_token}"
            f"{style.parentheses_open(self._style_token)}"
            f"{self.condition.render(style)}"
            f"{style.parentheses_close(self._style_token)}"
        )


class CDoWhile(CCompoundStatement):
    _style_token = "do_while"

    def __init__(self, statements: Union['CStatements', List['CStatement']], condition: 'CExpression'):
        self.condition = condition
        super(CDoWhile, self).__init__(statements)

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"do"
        )

    def _post_block(self, style: 'Style') -> str:
        return (
            f"while"
            f"{style.parentheses_open(self._style_token)}"
            f"{self.condition.render(style)}"
            f"{style.parentheses_close(self._style_token)}"
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

    def _pre_block(self, style: 'Style') -> str:
        return (
            f"for"
            f"{style.parentheses_open(self._style_token)}"
            f"{self.initial.render(style) if self.initial is not None else ''}"
            ";"  # TODO Spacing between semicolons
            f"{self.condition.render(style) if self.condition is not None else ''}"
            ";"
            f"{self.iteration.render(style) if self.iteration is not None else ''}"
            f"{style.parentheses_close(self._style_token)}"
        )
