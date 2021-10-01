from typing import TYPE_CHECKING, List, Callable

from .style import default_style

if TYPE_CHECKING:
    from .style import Style


# TODO propagate styles

class CStatement:
    def __init__(self, render_function: Callable):
        self.render_function = render_function

    def render(self, style: 'Style' = default_style) -> str:
        return self.render_function()


class Cdeclaration(CStatement):
    pass


# TODO Statements vs definitions
class CStatements(CStatement):
    def __init__(self, statements: List[CStatement]):
        super(CStatements, self).__init__(
            render_function=self.render
        )
        self.statements = statements

    def render(self, style: 'Style' = default_style):
        content = ""
        for statement in self.statements:
            content += f"{statement.render()}\n"
        return content


class CDeclarations(CStatements):
    def __init__(self, declarations: List[Cdeclaration]):
        super(CDeclarations, self).__init__(
            statements=declarations
        )
