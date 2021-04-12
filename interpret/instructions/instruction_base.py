from typing import List, Union
from xml.etree.ElementTree import Element

from argument import Argument


class InstructionBase:
    def __init__(self, element:Element, syntax_symbols:List[str]):
        error = SyntaxError(f"Bad instruction element {element} {element.attrib} (syntax: {syntax_symbols})")
        
        try: self.order = int(element.attrib["order"])
        except: raise error

        if element.tag != "instruction" or len(element.attrib.keys()) != 2 or self.order < 1:
            raise error

        self.name = type(self).__name__.upper()

        self.arguments:List[Argument] = []

        for argument in element:
            self.arguments.append(Argument(argument, syntax_symbols[len(self.arguments)]))


    def invoke(self) -> Union[None, int]:
        """Specific instruction implementation will be invoked here."""
        ...

#TODO: opcodes se neopakují (unique)