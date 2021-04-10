from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Concat(InstructionBase):
    def invoke(self):
        string1 = frames.get_var_or_literal_value(self, 1)
        string2 = frames.get_var_or_literal_value(self, 2)

        if type(string1) is not str or type(string2) is not str:
            stderr.write(f"{self.name} (order: {self.order}): Arguments are expected to be string, got {type(string1).__name__, type(string2).__name__}.\n")
            exit(53)
        result = string1 + string2
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class Strlen(InstructionBase):
    def invoke(self):
        string = frames.get_var_or_literal_value(self, 1)

        if type(string) is not str:
            stderr.write(f"{self.name} (order: {self.order}): Argument is expected to be string, got {type(string).__name__}.\n")
            exit(53)
        result = len(string)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class Getchar(InstructionBase):
    def invoke(self):
        string = frames.get_var_or_literal_value(self, 1)
        index = frames.get_var_or_literal_value(self, 2)

        if type(string) is not str:
            stderr.write(f"{self.name} (order: {self.order}): symb1 argument is expected to be string, got {type(string).__name__}.\n")
            exit(53)
        if type(index) is not int:
            stderr.write(f"{self.name} (order: {self.order}): symb2 argument is expected to be integer, got {type(index).__name__}.\n")
            exit(53)
        try:
            result = string[index]
            frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)

        except IndexError as e:
            stderr.write(f"{self.name} (order: {self.order}): {e} {string, index}.\n")
            exit(58)


class Setchar(InstructionBase):
    def invoke(self):
        var = frames.get_var_or_literal_value(self, 0)
        index = frames.get_var_or_literal_value(self, 1)
        string = frames.get_var_or_literal_value(self, 2)

        if type(var) is not str:
            stderr.write(f"{self.name} (order: {self.order}): var argument is expected to be string, got {type(var).__name__}.\n")
            exit(53)
        if type(index) is not int:
            stderr.write(f"{self.name} (order: {self.order}): symb1 argument is expected to be integer, got {type(index).__name__}.\n")
            exit(53)
        if type(string) is not str:
            stderr.write(f"{self.name} (order: {self.order}): symb2 argument is expected to be string, got {type(string).__name__}.\n")
            exit(53)

        if index < 0 or index >= len(var):
            stderr.write(f"{self.name} (order: {self.order}): Index out of range {var, index, string}.\n")
            exit(58)
        if string == "":
            stderr.write(f"{self.name} (order: {self.order}): symb2 string is empty {var, index, string}.\n")
            exit(58)

        result = f"{var[0:index]}{string[0]}{var[index + 1:]}"
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)
