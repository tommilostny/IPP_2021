from xml.etree.ElementTree import Element

class Argument:
    def __init__(self, element:Element):
        try:
            self.type = str(element.attrib["type"])

            if self.type == "int":
                self.value = int(element.text)

            elif self.type == "string":
                self.value = parse_string_arg(element.text)

            elif self.type == "bool":
                if element.text == "true": self.value = True
                elif element.text == "false": self.value = False
                else: raise TypeError()
            
            elif self.type == "nil":
                self.value = None

            else: self.value = element.text
                
        except Exception as e:
            raise Exception(f"{element.tag}: No attribute {e}, just {element.attrib}.")


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
