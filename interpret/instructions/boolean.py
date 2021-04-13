from typing import Callable

from error import exit_instruction_error

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _BooleanInstructionBase(InstructionBase):
    def invoke(self, operation:Callable[[bool, bool], bool]):
        value1 = frames.get(self, 1)
        value2 = frames.get(self, 2)
        
        if type(value1) is not bool or type(value2) is not bool:
            exit_instruction_error(self, 53, f"Invalid types of operands {type(value1).__name__} and {type(value2).__name__}")

        frames.set(self, 0, operation(value1, value2))


class And(_BooleanInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 and x2)


class Or(_BooleanInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 or x2)


class Not(InstructionBase):
    def invoke(self):
        value = frames.get(self, 1)
        
        if type(value) is not bool:
            exit_instruction_error(self, 53, f"Invalid type of operand {type(value).__name__}")

        frames.set(self, 0, not value)
