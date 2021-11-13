from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .style import Style


class Doc:
    """Documentation"""

    def __init__(self,
                 brief: Optional[str] = None,
                 body: Optional[str] = None,
                 ret: Optional[str] = None
                 ):
        """Constructor

        Args:
            brief: brief title of the object
            body: body with description of the object
            ret: documentation for return of function and methods
        """
        self.brief = brief
        self.body = body
        self.ret = ret

    def render(self, style: 'Style', content: Optional[List[str]] = None) -> str:
        lines = []

        if self.body is not None:
            lines.append(f"{self.body}")

        if content is not None:
            lines.extend(content)

        if self.brief is not None:
            lines.insert(0, f"{style.doxygen_command('brief')} {self.brief}")
            if len(lines) > 1:
                # If there is more content, insert a space between brief and others
                lines.insert(1, "")

        return style.doxygen_format(lines)
