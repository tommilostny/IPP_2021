from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Int2Char(InstructionBase):
    def invoke(self):
        integer = frames.get(self, 1)

        if type(integer) is not int:
            stderr.write(f"{self.name} (order: {self.order}): Argument is expected to be integer, got {type(integer).__name__}.\n")
            exit(53)
        try:
            result = chr(integer)
            frames.set(self, 0, result)

        except ValueError as e:
            stderr.write(f"{self.name} (order: {self.order}): {e} ({integer}).\n")
            exit(58)


class Stri2Int(InstructionBase):
    def invoke(self):
        string = frames.get(self, 1)
        index = frames.get(self, 2)

        if type(string) is not str:
            stderr.write(f"{self.name} (order: {self.order}): First argument is expected to be string, got {type(string).__name__}.\n")
            exit(53)
        if type(index) is not int:
            stderr.write(f"{self.name} (order: {self.order}): Second argument is expected to be integer, got {type(index).__name__}.\n")
            exit(53)
        try:
            result = ord(string[index])
            frames.set(self, 0, result)

        except IndexError as e:
            stderr.write(f"{self.name} (order: {self.order}): {e} {string, index}.\n")
            exit(58)
