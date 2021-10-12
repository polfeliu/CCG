from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from .style import Style


class Doc:

    def __init__(self, brief: Union[str, None] = "", body: Union[str, None] = None, ret: Union[str, None] = None):
        self.brief = brief
        self.body = body
        self.ret = ret

    def doxygen_doc(self, style: 'Style', content: Union[List[str], None] = None):
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
