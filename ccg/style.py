from textwrap import indent


class Style:
    check_hungarian = False

    # New lines
    new_line_function_bracket_open_before = True
    new_line_function_bracket_open_after = True
    new_line_function_bracket_close_before = True
    new_line_function_bracket_close_after = False
    new_line_function_prototype_after_type = False

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

    # Spaces
    space_function_after_name_prototype = True
    space_function_after_name_declaration = True

    space_function_bracket_open_before = False
    space_function_bracket_open_after = False
    space_function_bracket_close_before = False
    space_function_bracket_close_after = False

    space_struct_bracket_open_before = False
    space_struct_bracket_open_after = False
    space_struct_bracket_close_before = False
    space_struct_bracket_close_after = False
    space_struct_members = True

    space_union_bracket_open_before = False
    space_union_bracket_open_after = False
    space_union_bracket_close_before = False
    space_union_bracket_close_after = False
    space_union_members = False

    def bracket_open(self, object):
        return (
                self.__getattribute__(f"vnew_line_{object}_bracket_open_before") +
                self.__getattribute__(f"vspace_{object}_bracket_open_before") +
                '{' +
                self.__getattribute__(f"vnew_line_{object}_bracket_open_after") +
                self.__getattribute__(f"vspace_{object}_bracket_open_after")
        )

    def bracket_close(self, object):
        return (
                self.__getattribute__(f"vnew_line_{object}_bracket_close_before") +
                self.__getattribute__(f"vspace_{object}_bracket_close_before") +
                '}' +
                self.__getattribute__(f"vnew_line_{object}_bracket_close_after") +
                self.__getattribute__(f"vspace_{object}_bracket_close_after")
        )

    def __getattribute__(self, item):
        if item.startswith('vnew_line'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return '\n' if style_set else ''
        elif item.startswith('vspace'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return ' ' if style_set else ''
        else:
            return super(Style, self).__getattribute__(item)

    indent_token = '\t'

    def indent(self, value: str):
        return indent(value, self.indent_token)


default_style = Style()
