from typing import Any, Callable, Dict, List

from error import exit_instruction_error

import instructions.frames as frames
from instructions.instruction_base import InstructionBase

#Seznam instrukcí inicializovaný hlavním programem interpret.py
instructions:List[InstructionBase] = []

#Slovník návěští (jméno -> index v seznamu instrukcí)
labels:Dict[str, int] = {}

#Čítač instrukcí
program_counter = 0


def register_all_labels():
    for index, instruction in enumerate(instructions):
	    if type(instruction) is Label:
		    instruction.register(index + 1)


class Label(InstructionBase):
    def register(self, index:int):
        #Registrace návěští do slovníku
        if self.arguments[0].value not in labels.keys():
            labels[self.arguments[0].value] = index
        else:
            exit_instruction_error(self, 52, f"Label {self.arguments[0].value} already exists")


class Jump(InstructionBase):
    def invoke(self) -> int:
        if self.arguments[0].value not in labels.keys():
            exit_instruction_error(self, 52, f"Label {self.arguments[0].value} does not exist")

        return labels[self.arguments[0].value]


class _ConditionalJumpBase(InstructionBase):
    def invoke(self, comparison:Callable[[Any, Any], bool]) -> int:

        if self.arguments[0].value not in labels.keys():
            exit_instruction_error(self, 52, f"Label {self.arguments[0].value} does not exist")

        value1 = frames.get(self, 1)
        value2 = frames.get(self, 2)

        if type(value1) is not type(value2) and value1 is not None and value2 is not None:
            exit_instruction_error(self, 53, f"Cannot compare {type(value1).__name__} and {type(value2).__name__}")

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
        exitcode = frames.get(self, 0)

        if type(exitcode) is not int:
            exit_instruction_error(self, 53, f"Invalid exit code type {exitcode}")

        if exitcode < 0 or exitcode > 49:
            exit_instruction_error(self, 57, f"Invalid exit code {exitcode}")

        exit(exitcode)
