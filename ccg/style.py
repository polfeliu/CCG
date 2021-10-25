from typing import List, Union, Optional
from enum import Enum

from textwrap import indent


class Style:
    check_hungarian = False

    # New lines
    new_line_function_bracket_open_before = True
    new_line_function_bracket_open_after = True
    new_line_function_bracket_close_before = True
    new_line_function_bracket_close_after = False
    new_line_function_declaration_after_type = False

    new_line_struct_bracket_open_before = True
    new_line_struct_bracket_open_after = True
    new_line_struct_bracket_close_before = True
    new_line_struct_bracket_close_after = False
    new_line_struct_members = True

    new_line_union_bracket_open_before = True
    new_line_union_bracket_open_after = True
    new_line_union_bracket_close_before = True
    new_line_union_bracket_close_after = False
    new_line_union_members = True

    new_line_class_bracket_open_before = True
    new_line_class_bracket_open_after = True
    new_line_class_bracket_close_before = True
    new_line_class_bracket_close_after = False

    # Spaces
    space_function_after_name_definition = False
    space_function_after_name_declaration = False

    space_function_bracket_open_before = False
    space_function_bracket_open_after = False
    space_function_bracket_close_before = False
    space_function_bracket_close_after = False

    space_struct_bracket_open_before = False
    space_struct_bracket_open_after = False
    space_struct_bracket_close_before = False
    space_struct_bracket_close_after = False
    space_struct_members = False

    space_union_bracket_open_before = False
    space_union_bracket_open_after = False
    space_union_bracket_close_before = False
    space_union_bracket_close_after = False
    space_union_members = False

    space_class_bracket_open_before = False
    space_class_bracket_open_after = False
    space_class_bracket_close_before = False
    space_class_bracket_close_after = False

    space_after_cast = True

    # Indentation
    indent_class_member = True
    indent_class_access = False
    indent_struct_member = True

    # Attributes
    attribute_packed = "__attribute__((__packed__))"

    # Class member styles
    class ClassMembers(Enum):
        inline_access_preserve_order = 0
        group_by_access_specified = 1

    class_members = ClassMembers.group_by_access_specified

    # Functions
    function_void_when_no_arguments = True

    def bracket_open(self, obj) -> str:
        return (
                str(self.__getattribute__(f"vnew_line_{obj}_bracket_open_before")) +
                str(self.__getattribute__(f"vspace_{obj}_bracket_open_before")) +
                '{' +
                str(self.__getattribute__(f"vnew_line_{obj}_bracket_open_after")) +
                str(self.__getattribute__(f"vspace_{obj}_bracket_open_after"))
        )

    def bracket_close(self, obj) -> str:
        return (
                str(self.__getattribute__(f"vnew_line_{obj}_bracket_close_before")) +
                str(self.__getattribute__(f"vspace_{obj}_bracket_close_before")) +
                '}' +
                str(self.__getattribute__(f"vnew_line_{obj}_bracket_close_after")) +
                str(self.__getattribute__(f"vspace_{obj}_bracket_close_after"))
        )

    def __getattribute__(self, item) -> object:
        if item.startswith('vnew_line'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return self.new_line_token if style_set else ''
        elif item.startswith('vspace'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return ' ' if style_set else ''
        else:
            return super(Style, self).__getattribute__(item)

    new_line_token = '\n'
    indent_token = '\t'

    def indent(self, value: str, obj: Optional[str] = None) -> str:
        style_set = True
        if obj is not None:
            style_set = bool(self.__getattribute__(f"indent_{obj}"))

        if style_set:
            return indent(value, self.indent_token)
        else:
            return value

    @staticmethod
    def check_hungarian_variable(variable_name: str, hungarian_prefixes: Union[List[str], str]) -> bool:
        if isinstance(hungarian_prefixes, str):
            hungarian_prefixes = [str(hungarian_prefixes)]

        for hungarian_prefix in hungarian_prefixes:
            if variable_name.startswith(hungarian_prefix):
                start_letter = variable_name[len(hungarian_prefix)]
                if start_letter.isupper():
                    return True

        return False

    # Doxygen
    doc_doxygen_start_block = "/**"
    doc_doxygen_line_block = " * "
    doc_doxygen_end_block = " */"

    doc_doxygen_command_token = "@"

    def doxygen_format(self, lines: List[str]) -> str:
        if len(lines) == 0:
            return ""
        elif len(lines) == 1:
            return f"{self.doc_doxygen_start_block} {lines[0]}{self.doc_doxygen_end_block}{self.new_line_token}"
        else:
            content = ''.join([f"{self.doc_doxygen_line_block}{line}{self.new_line_token}" for line in lines])
            return (
                f"{self.doc_doxygen_start_block}{self.new_line_token}"
                f"{content}"
                f"{self.doc_doxygen_end_block}{self.new_line_token}"
            )

    def doxygen_command(self, command_name: str) -> str:
        return f"{self.doc_doxygen_command_token}{command_name}"


default_style = Style()
