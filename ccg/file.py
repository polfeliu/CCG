from typing import TYPE_CHECKING, Union, List, Callable

from .statements import CDeclarations, CDeclaration, CStatement
from .style import default_style

from os.path import isfile
import re

if TYPE_CHECKING:
    from .style import Style

UserCodeCallback = Callable[['Style', str], str]


class File:

    def __init__(self, declarations: Union['CDeclarations', List['CDeclaration']], style: 'Style' = default_style):
        if isinstance(declarations, CDeclaration):
            self.declarations = declarations
        else:
            self.declarations = CDeclarations(declarations)
        self.style = style

    def generate(self, path: str):
        current_code_sections = {}
        if isfile(path):
            # Scan current user code sections
            with open(path, "r") as current:
                current_content = current.read()
                current_code_sections = self._analyze_code_sections(current_content)

        generated = self.declarations.render()

        code_with_sections = self._insert_code_sections(generated, current_code_sections)

        with open(path, "w+") as output:
            output.write(code_with_sections)

    def _insert_code_sections(self, code: str, current: dict) -> str:
        generated_code_sections = self._analyze_code_sections(code)

        for identifier, _ in generated_code_sections.items():
            if identifier in current.keys():
                code = re.sub(
                    # Find Pattern
                    self.user_code_pattern(identifier),

                    # Replace with
                    render_user_code_section(
                        identifier=identifier,
                        content=current[identifier],
                        style=self.style
                    ),

                    # On this content
                    code
                )
        return code

    def _analyze_code_sections(self, content: str) -> dict:
        code_sections = {}

        identifier_finder = "--------------------------"

        for section_match in re.finditer(self.user_code_pattern(), content):
            section = section_match.group()
            begin_token = re.search(self.any_begin_pattern(), section).group()
            end_token = re.search(self.any_end_pattern(), section).group()

            begin_id = begin_token \
                .lstrip(self.style.user_code_begin_pattern_before) \
                .rstrip(self.style.user_code_begin_pattern_after)

            end_id = end_token \
                .lstrip(self.style.user_code_end_pattern_before) \
                .rstrip(self.style.user_code_end_pattern_after)

            if begin_id != end_id:
                raise ValueError("Code sections identifiers do not match")

            if begin_id in code_sections:
                raise KeyError(f"identifier {begin_id} is duplicated")

            code_sections[begin_id] = section \
                .lstrip(self.style.user_code_begin(begin_id)) \
                .rstrip(self.style.user_code_end(begin_id))

        return code_sections

    def any_begin_pattern(self) -> str:
        return self.style.user_code_begin_pattern(r'(.*)')  # TODO REMOVE

    def any_end_pattern(self) -> str:
        return self.style.user_code_end_pattern(r'(.*)')

    def user_code_pattern(self, identifier: str = r'(.*)') -> str:
        # Defaults to any
        return (
            rf"{self.style.user_code_begin_pattern(identifier)}"
            rf"(.|\n|\r|\t)*?"  # Any content between
            rf"{self.style.user_code_end_pattern(identifier)}"
        )


def render_user_code_section(identifier: str, content: str, style: 'Style'):
    return (
        f"{style.user_code_begin(identifier)}"
        f"{content}"
        f"{style.user_code_end(identifier)}"
    )


class UserCodeStatement(CStatement):

    def __init__(self, identifier: str, default_content: str = "\n"):
        # TODO VALIDATE IDENTIFIER INCLUDES STANDARD CHARACTERS
        super(UserCodeStatement, self).__init__(self._render)
        self.identifier = identifier
        self.default_content = default_content

    def _render(self, style: 'Style' = default_style) -> str:
        return render_user_code_section(
            identifier=self.identifier,
            content=self.default_content,
            style=style
        )
