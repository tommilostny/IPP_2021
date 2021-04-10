from typing import List, Union
from xml.etree.ElementTree import Element

from argument import Argument


class InstructionBase:
    def __init__(self, element:Element, syntax_symbols:List[str]):
        self.order = int(element.attrib["order"])
        self.name = type(self).__name__.upper()
        self.arguments = []

        for argument in element:
            self.arguments.append(Argument(argument, syntax_symbols[len(self.arguments)]))
        if len(self.arguments) != len(syntax_symbols):
            raise SyntaxError(f"Not enought instruction arguments. (syntax: {syntax_symbols})")

    def invoke(self) -> Union[None, int]:
        """Specific instruction implementation will be invoked here."""
        ...
