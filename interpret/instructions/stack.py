from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


stack = []


class Pushs(InstructionBase):
    def invoke(self):
        stack.append(frames.get(self, 0))


class Pops(InstructionBase):
    def invoke(self):
        if len(stack) == 0:
            stderr.write(f"{self.name} (order: {self.order}): Stack is empty.\n")
            exit(56)

        value = stack.pop()
        frames.set(self, 0, value)
