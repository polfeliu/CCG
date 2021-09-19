from typing import TYPE_CHECKING, List, Callable

from .style import default_style

if TYPE_CHECKING:
    from .style import Style


# TODO propagate styles

class Cstatement:
    def __init__(self, render_function: Callable):
        self.render_function = render_function

    def render(self, style: 'Style' = default_style) -> str:
        return self.render_function()


class Cdeclaration(Cstatement):
    pass


# TODO Statements vs definitions
class Cstatements(Cstatement):
    def __init__(self, statements: List[Cstatement]):
        super(Cstatements, self).__init__(
            render_function=self.render
        )
        self.statements = statements

    def render(self, style: 'Style' = default_style):
        content = ""
        for statement in self.statements:
            content += f"{statement.render()}\n"
        return content


class Cdeclarations(Cstatements):
    def __init__(self, declarations: List[Cdeclaration]):
        super(Cdeclarations, self).__init__(
            statements=declarations
        )
