from typing import TYPE_CHECKING, List, Callable

from .style import default_style

if TYPE_CHECKING:
    from .style import Style


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


class CStatements(CStatement):
    """Statements Collection"""

    def __init__(self, statements: List[CStatement]):
        super(CStatements, self).__init__(
            render_function=self.render
        )
        self.statements = statements

    def render(self, style: 'Style' = default_style):
        content = ""
        for statement in self.statements:
            content += f"{statement.render(style)}{style.new_line_token}"
        return content.rstrip(style.new_line_token)


class CDeclarations(CStatements):
    """Declarations Collection"""

    def __init__(self, declarations: List[CDeclaration]):
        super(CDeclarations, self).__init__(
            statements=declarations
        )
