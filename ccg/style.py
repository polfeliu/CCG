class Style:
    check_hungarian = False

    # New lines
    new_line_function_bracket_open_before = False
    new_line_function_bracket_open_after = False
    new_line_function_bracket_close_before = False
    new_line_function_bracket_close_after = False
    new_line_function_prototype_after_type = False

    new_line_struct_bracket_open_before = False
    new_line_struct_bracket_open_after = False
    new_line_struct_bracket_close_before = False
    new_line_struct_bracket_close_after = False
    new_line_struct_prototype_after_type = False

    # Spaces
    space_function_after_name_prototype = True
    space_function_after_name_declaration = True

    def __getattribute__(self, item):
        if item.startswith('vnew_line'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return '\n' if style_set else ''
        if item.startswith('vbracket'):
            if item.endswith('open'):
                before_set = super(Style, self).__getattribute__("new_line" + item[8:] + "_before")
                after_set = super(Style, self).__getattribute__("new_line" + item[8:] + "_after")
                return (
                    "\n" if before_set else ''
                    "{"
                    "\n" if after_set else '' # TODO
                )
            elif 'close' in item:
                pass
            else:
                raise KeyError("Brackets must be open or close")
        elif item.startswith('vspace'):
            style_set = super(Style, self).__getattribute__(item[1:])
            return ' ' if style_set else ''
        else:
            super(Style, self).__getattribute__(item)


default_style = Style()

asdf = 1
