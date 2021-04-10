from sys import exit, stderr
from typing import Dict, List
from xml.etree.ElementTree import Element

import instructions.frames as frames
from instructions.instruction_base import InstructionBase

#Seznam instrukcí inicializovaný hlavním programem interpret.py
instructions:List[InstructionBase] = []

#Slovník návěští (jméno -> index v seznamu instrukcí)
labels:Dict[str, int] = {}


class Label(InstructionBase):
    def __init__(self, element: Element, syntax_symbols: List[str]):
        super().__init__(element, syntax_symbols)

        #Registrace návěští do slovníku
        if self.arguments[0].value not in labels.keys():
            labels[self.arguments[0].value] = len(instructions)
        else:
            stderr.write(f"{self.name} (order: {self.order}): Label {self.arguments[0].value} already exists.\n")
            exit(52)

class Jump(InstructionBase):
    def invoke(self) -> int:
        if self.arguments[0].value not in labels.keys():
            stderr.write(f"{self.name} (order: {self.order}): Label {self.arguments[0].value} does not exist.\n")
            exit(52)

        return labels[self.arguments[0].value]


class _ConditionalJumpBase(InstructionBase):
    def invoke(self, comparison) -> int:
        if self.arguments[0].value not in labels.keys():
            stderr.write(f"{self.name} (order: {self.order}): Label {self.arguments[0].value} does not exist.\n")
            exit(52)

        value1 = frames.get_var_or_literal_value(self, 1)
        value2 = frames.get_var_or_literal_value(self, 2)

        if type(value1) is not type(value2):
            stderr.write(f"{self.name} (order: {self.order}): Cannot compare {type(value1).__name__} and {type(value2).__name__}.\n")
            exit(53)

        if comparison(value1, value2):
            return labels[self.arguments[0].value]


class JumpIfEq(_ConditionalJumpBase):
    def invoke(self) -> int:
        return super().invoke(lambda x1, x2: x1 == x2)


class JumpIfNeq(_ConditionalJumpBase):
    def invoke(self) -> int:
        return super().invoke(lambda x1, x2: x1 != x2)


class Exit(InstructionBase):
    def invoke(self):
        exitcode = frames.get_var_or_literal_value(self, 0)

        if type(exitcode) is not int or exitcode < 0 or exitcode > 49:
            stderr.write(f"{self.name} (order: {self.order}): Invalid exit code {exitcode}.\n")
            exit(57)

        exit(exitcode)
