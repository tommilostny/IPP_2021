from error import exit_instruction_error

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Concat(InstructionBase):
    def invoke(self):
        string1 = frames.get(self, 1)
        string2 = frames.get(self, 2)

        if type(string1) is not str or type(string2) is not str:
            exit_instruction_error(self, 53, f"Arguments are expected to be string, got {type(string1).__name__, type(string2).__name__}")

        frames.set(self, 0, string1 + string2)


class Strlen(InstructionBase):
    def invoke(self):
        string = frames.get(self, 1)

        if type(string) is not str:
            exit_instruction_error(self, 53, f"Argument is expected to be string, got {type(string).__name__}")

        frames.set(self, 0, len(string))


class Getchar(InstructionBase):
    def invoke(self):
        string = frames.get(self, 1)
        index = frames.get(self, 2)

        if type(string) is not str:
            exit_instruction_error(self, 53, f"symb1 argument is expected to be string, got {type(string).__name__}")

        if type(index) is not int:
            exit_instruction_error(self, 53, f"symb2 argument is expected to be integer, got {type(index).__name__}")

        try:
            if index < 0: raise IndexError("Index cannot be negative.")

            frames.set(self, 0, string[index])
        except IndexError as e:
            exit_instruction_error(self, 58, f"{e} {string, index}")


class Setchar(InstructionBase):
    def invoke(self):
        var = frames.get(self, 0)
        index = frames.get(self, 1)
        string = frames.get(self, 2)

        if type(var) is not str:
            exit_instruction_error(self, 53, f"var argument is expected to be string, got {type(var).__name__}")

        if type(index) is not int:
            exit_instruction_error(self, 53, f"symb1 argument is expected to be integer, got {type(index).__name__}")

        if type(string) is not str:
            exit_instruction_error(self, 53, f"symb2 argument is expected to be string, got {type(string).__name__}")

        if index < 0 or index >= len(var):
            exit_instruction_error(self, 58, f"Index out of range {var, index, string}")

        if string == "":
            exit_instruction_error(self, 58, f"symb2 string is empty {var, index, string}")

        frames.set(self, 0, f"{var[0:index]}{string[0]}{var[index + 1:]}")
