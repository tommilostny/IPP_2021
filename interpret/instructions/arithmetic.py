from sys import exit, stderr
from typing import Callable

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _ArithmeticInstructionBase(InstructionBase):
    def invoke(self, operation:Callable[[int, int], int]):

        num1 = frames.get(self, 1)
        num2 = frames.get(self, 2)
        
        if type(num1) is not int or type(num2) is not int:
            stderr.write(f"{self.name} (order: {self.order}): Invalid operand type (all must be integers).\n")
            exit(53)

        result = operation(num1, num2)
        frames.set(self, 0, result)


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
