from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


stack = []


class Pushs(InstructionBase):
    def invoke(self):
        stack.append(frames.get_var_or_literal_value(self, 0))


class Pops(InstructionBase):
    def invoke(self):
        if len(stack) > 0:
            value = stack.pop()
            frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, value)
        else:
            stderr.write(f"{self.name} (order: {self.order}): Stack is empty.\n")
            exit(56)
