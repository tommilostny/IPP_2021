from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _ArithmeticInstructionBase(InstructionBase):
    def invoke(self, operation):
        try:
            num1 = int(frames.get_var_or_literal_value(self, 1))
            num2 = int(frames.get_var_or_literal_value(self, 2))
        except ValueError:
            stderr.write(f"{self.name} (order: {self.order}): Invalid operand type (all must be integers).\n")
            exit(53)
        result = operation(num1, num2)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


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
