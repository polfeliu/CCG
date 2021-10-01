from typing import List, Union
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
            return '\n' if style_set else ''
        elif item.startswith('vspace'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return ' ' if style_set else ''
        else:
            return super(Style, self).__getattribute__(item)

    indent_token = '\t'

    def indent(self, value: str, obj: Union[str, None] = None) -> str:
        style_set = True
        if obj is not None:
            style_set = self.__getattribute__(f"indent_{obj}")

        if style_set:
            return indent(value, self.indent_token)
        else:
            return value

    @staticmethod
    def check_hungarian_variable(variable_name: str, hungarian_prefixes: List[str]) -> bool:
        for hungarian_prefix in hungarian_prefixes:
            if variable_name.startswith(hungarian_prefix):
                start_letter = variable_name[len(hungarian_prefix)]
                if start_letter.isupper():
                    return True

        return False


default_style = Style()
