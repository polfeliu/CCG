from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Callable, Sequence, Union, Optional

from ..style import default_style

if TYPE_CHECKING:
    from ..style import Style
    from ..file import UserSectionCallback


class CStatement:
    """Statement"""

    def __init__(self, render_function: Callable[..., str], **kwargs):
        self.render_function = render_function
        self.kwargs = kwargs

    def render(self, style: 'Style' = default_style, user_code_callback: Optional['UserSectionCallback'] = None) -> str:
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


class CTokenStatement(CStatement, ABC):
    """Statement based on a token"""

    def __init__(self):
        super(CTokenStatement, self).__init__(self._render_function)

    @property
    @abstractmethod
    def _token(self) -> str:
        pass

    def _post_block(self, style: 'Style') -> str:
        return ""

    @abstractmethod
    def _semicolon_before_space(self, style: 'Style') -> bool:
        pass

    def _render_function(self, style: 'Style' = default_style) -> str:
        return (
            f"{self._token}"
            f"{self._post_block(style)}"
            f"{style.space(self._semicolon_before_space(style))}"
            f";"
        )


class CCompoundStatement(ABC, CStatement):
    """Statement based on statements enclosed in brackets"""

    _style_token: Union[str, None] = None

    def __init__(self, statements: Union['CStatements', List['CStatement']]):
        if isinstance(statements, CStatements):
            self.statements = statements
        else:
            self.statements = CStatements(statements)
        super(CCompoundStatement, self).__init__(self._render_function)

    @abstractmethod
    def _bracket_style(self, style: 'Style') -> 'Style.GroupDelimitatorStyle':
        pass

    @abstractmethod
    def _indent_content_style(self, style: 'Style') -> bool:
        pass

    def _render_function(self, style: 'Style') -> str:
        content = self.statements.render(style)
        if self._style_token is not None:
            content = style.indent(content, self._indent_content_style(style))

        return (
            f"{self._pre_block(style)}"
            f"{style.open_bracket(self._bracket_style(style))}"
            f"{content}"
            f"{style.close_bracket(self._bracket_style(style))}"
            f"{self._post_block(style)}"
        )

    def _pre_block(self, style: 'Style') -> str:
        return ""

    def _post_block(self, style: 'Style') -> str:
        return ""
