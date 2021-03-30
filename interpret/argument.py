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
                
        except Exception as e:
            raise Exception(f"{element.tag}: No attribute {e}, just {element.attrib}.")


def parse_string_arg(string:str) -> str: #TODO
    if string is None:
        return ""
    else:
        return string
