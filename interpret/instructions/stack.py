from error import exit_instruction_error

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


data_stack = []


class Pushs(InstructionBase):
    def invoke(self):
        data_stack.append(frames.get(self, 0))


class Pops(InstructionBase):
    def invoke(self):
        if len(data_stack) == 0:
            exit_instruction_error(self, 56, "Stack is empty")

        frames.set(self, 0, data_stack.pop())
