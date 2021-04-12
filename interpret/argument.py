from xml.etree.ElementTree import Element

class Argument:
    def __init__(self, element:Element, syntax_symbol:str):
        self.type = str(element.attrib["type"])

        if syntax_symbol == "symb":

            if self.type == "int":
                self.value = int(element.text)

            elif self.type == "string":
                self.value = parse_string_arg(element.text)

            elif self.type == "bool":
                if element.text == "true": self.value = True
                elif element.text == "false": self.value = False
                else: raise TypeError(f"{element.text} is not a valid bool")
            
            elif self.type == "nil":
                self.value = None

            elif self.type == "var":
                self.value = element.text

            else: raise SyntaxError(f"{self.type} is not valid {syntax_symbol}")
        
        elif syntax_symbol == "var" and self.type == "var":
            self.value = element.text

        elif syntax_symbol == "label" and self.type == "label":
            self.value = element.text

        elif syntax_symbol == "type" and self.type == "type" and element.text in ["int", "string", "bool"]:
            self.value = element.text

        else: raise SyntaxError(f"{self.type} {element.text} is not valid {syntax_symbol}")


def parse_string_arg(string:str) -> str:
    if string is None:
        return ""
    else:
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
