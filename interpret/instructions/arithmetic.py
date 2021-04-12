from sys import exit, stderr
from typing import Callable

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _ArithmeticInstructionBase(InstructionBase):
    def invoke(self, operation:Callable[[int, int], int]):
        value1 = frames.get(self, 1)
        value2 = frames.get(self, 2)
        
        if type(value1) is not int or type(value2) is not int:
            stderr.write(f"{self.name} (order: {self.order}): Invalid types of operands {type(value1).__name__} and {type(value2).__name__}.\n")
            exit(53)

        frames.set(self, 0, operation(value1, value2))


class Add(_ArithmeticInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 + x2)


class Sub(_ArithmeticInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 - x2)


class Mul(_ArithmeticInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 * x2)


class IDiv(_ArithmeticInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 // x2)
