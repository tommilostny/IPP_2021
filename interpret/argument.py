import re
from typing import List
from xml.etree.ElementTree import Element


class Argument:
    def __init__(self, element:Element, syntax_symbols:List[str]):
        try: self.type = str(element.attrib["type"])
        except:
            raise SyntaxError(f"Bad argument: missing type attribute: {element} {element.attrib}")

        error_flag = len(element.attrib.keys()) > 1 or not re.compile("^arg\d$").match(element.tag)
        if not error_flag:
            self.order = int(element.tag[3]) - 1
            error_flag = self.order < 0 or self.order >= len(syntax_symbols)

        if error_flag:
            raise SyntaxError(f"Bad argument: Invalid XML element tag: {element} {element.attrib}")

        if syntax_symbols[self.order] == "symb":

            if self.type == "int":
                self.value = int(element.text)

            elif self.type == "string":
                self.value = _parse_string_arg(element.text)

            elif self.type == "bool":
                if element.text == "true": self.value = True
                elif element.text == "false": self.value = False
                else: raise SyntaxError(f"{element.text} is not a valid bool")
            
            elif self.type == "nil":
                self.value = None

            elif self.type == "var":
                self.value = element.text

            else: raise SyntaxError(f"{self.type} is not valid {syntax_symbols[self.order]}")
        
        elif syntax_symbols[self.order] == "var" and self.type == "var":
            self.value = element.text

        elif syntax_symbols[self.order] == "label" and self.type == "label":
            self.value = element.text

        elif syntax_symbols[self.order] == "type" and self.type == "type" and element.text in ["int", "string", "bool"]:
            self.value = element.text

        else: raise SyntaxError(f"{self.type} {element.text} is not valid {syntax_symbols[self.order]}")


def _parse_string_arg(string:str) -> str:
    if string is None:
        return ""

    result = ""
    loading_escape_sequence = False
    for char in string:
        if not loading_escape_sequence:
            if char == "\\":
                loading_escape_sequence = True
                ascii = ""
            else:
                result += char
        else:
            ascii += char
            if len(ascii) == 3:
                result += chr(int(ascii))
                loading_escape_sequence = False
    return result
