from typing import TYPE_CHECKING, List, Callable, Sequence, Union

from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style


class CStatement:
    """Statement"""

    def __init__(self, render_function: Callable[..., str], **kwargs):
        self.render_function = render_function
        self.kwargs = kwargs

    def render(self, style: 'Style' = default_style) -> str:
        return self.render_function(style=style, **self.kwargs)


class CDeclaration(CStatement):
    """Declaration

    Definitions are considered as a type of declaration"""


class CStatementFreeStyle(CStatement):

    def __init__(self, content: str):
        super(CStatementFreeStyle, self).__init__(self.content_render)
        self.content = content

    def content_render(self, style: 'Style' = default_style) -> str:
        return self.content


class CDeclarationFreeStyle(CDeclaration, CStatementFreeStyle):
    pass


class CStatements(CStatement):
    """Statements Collection"""

    def __init__(self, statements: Sequence[CStatement]):
        super(CStatements, self).__init__(
            render_function=self.render
        )
        self.statements = list(statements)

    def render(self, style: 'Style' = default_style) -> str:
        content = ""
        for statement in self.statements:
            content += f"{statement.render(style)}{style.new_line_token}"
        return content.rstrip(style.new_line_token)

    def append(self, statement: CStatement):
        self.statements.append(statement)


class CDeclarations(CStatements):
    """Declarations Collection"""

    def __init__(self, declarations: List[CDeclaration]):
        super(CDeclarations, self).__init__(
            statements=declarations
        )


class CCompoundStatement(CStatement):
    _style_token: Union[str, None] = None

    def __init__(self, statements: Union['CStatements', List['CStatement']]):
        if isinstance(statements, CStatements):
            self.statements = statements
        else:
            self.statements = CStatements(statements)
        super(CCompoundStatement, self).__init__(self._render_function)

    def _render_function(self, style: 'Style') -> str:
        content = self.statements.render(style)
        if self._style_token is not None:
            content = style.indent(content, self._style_token + '_content')

        return (
            f"{self._pre_block(style)}"
            f"{style.bracket_open(self._style_token)}"
            f"{content}"
            f"{style.bracket_close(self._style_token)}"
            f"{self._post_block(style)}"
        )

    def _pre_block(self, style: 'Style') -> str:
        return ""

    def _post_block(self, style: 'Style') -> str:
        return ""


CBreak = CStatementFreeStyle('break;')
