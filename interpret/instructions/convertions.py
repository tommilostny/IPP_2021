from error import exit_instruction_error

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Int2Char(InstructionBase):
    def invoke(self):
        integer = frames.get(self, 1)

        if type(integer) is not int:
            exit_instruction_error(self, 53, f"Argument is expected to be integer, got {type(integer).__name__}")
        try:
            frames.set(self, 0, chr(integer))

        except ValueError as e:
            exit_instruction_error(self, 58, f"{e} ({integer})")


class Stri2Int(InstructionBase):
    def invoke(self):
        string = frames.get(self, 1)
        index = frames.get(self, 2)

        if type(string) is not str:
            exit_instruction_error(self, 53, f"First argument is expected to be string, got {type(string).__name__}")
        if type(index) is not int:
            exit_instruction_error(self, 53, f"Second argument is expected to be integer, got {type(index).__name__}")
        try:
            frames.set(self, 0, ord(string[index]))

        except IndexError as e:
            exit_instruction_error(self, 58, f"{e} {string, index}")
