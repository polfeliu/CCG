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
            # Scan user code sections
            with open(path, "r") as current:
                current_content = current.read()
                current_code_sections = self._analyze_code_sections(current_content)

        generated = self.declarations.render()

        # self._analyze_code_sections(generated)

        """with open(path, "w+") as output:
            output.write(generated)"""

    def _analyze_code_sections(self, content: str) -> dict:
        any_identifier = r'(.*)'
        any_begin_pattern = self.style.user_code_begin_pattern(any_identifier)
        any_end_pattern = self.style.user_code_end_pattern(any_identifier)
        pattern = (
            rf"{any_begin_pattern}"
            rf"(.|\n|\r|\t)*?"  # Any content between
            rf"{any_end_pattern}"
        )

        code_sections = {}

        identifier_finder = "--------------------------"

        for section_match in re.finditer(pattern, content):
            section = section_match.group()
            begin_token = re.search(any_begin_pattern, section).group()
            end_token = re.search(any_end_pattern, section).group()

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

        print(code_sections)
        return code_sections


class UserCodeStatement(CStatement):

    def __init__(self, identifier: str):  # TODO VALIDATE IDENTIFIER INCLUDES STANDARD CHARACTERS
        super(UserCodeStatement, self).__init__(self._render)
        self.identifier = identifier
        self.content = ""  # TODO SCAN

    def _render(self, style: 'Style' = default_style) -> str:
        return (
            f"{style.user_code_begin(self.identifier)}\n"
            f"{self.content}"
            f"{style.user_code_end(self.identifier)}"
        )
