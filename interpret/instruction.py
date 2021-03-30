from xml.etree.ElementTree import Element
from argument import Argument

class Instruction:
    def __init__(self, element:Element):
        self.order = int(element.attrib["order"])
        self.arguments = []
        for argument in element:
            self.arguments.append(Argument(argument))

    def invoke(self):
        """Specific instruction implementation will be invoked here."""
        ...

class Write(Instruction):
    def invoke(self):
        print(self.arguments[0].type, self.arguments[0].value)
