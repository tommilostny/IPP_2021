from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


data_stack = []


class Pushs(InstructionBase):
    def invoke(self):
        data_stack.append(frames.get(self, 0))


class Pops(InstructionBase):
    def invoke(self):
        if len(data_stack) == 0:
            stderr.write(f"{self.name} (order: {self.order}): Stack is empty.\n")
            exit(56)

        frames.set(self, 0, data_stack.pop())
