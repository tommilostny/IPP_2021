from xml.etree.ElementTree import Element

class Argument:
    def __init__(self, element:Element):
        try:
            self.type = str(element.attrib["type"])
        except Exception as e:
            raise Exception(f"{element.tag}: No attribute {e}, just {element.attrib}.")

        self.value = element.text ##TODO: decode value based on type
