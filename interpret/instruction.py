from sys import exit, stderr
from xml.etree.ElementTree import Element

import frames
from argument import Argument


class Instruction:
    def __init__(self, element:Element, syntax:list):
        self.order = int(element.attrib["order"])
        self.name = type(self).__name__.upper()
        self.arguments = []

        for argument in element:
            self.arguments.append(Argument(argument, syntax[len(self.arguments)]))
        if len(self.arguments) != len(syntax):
            stderr.write(f"{self.name}: (order: {self.order}): Not enought instruction arguments. (syntax: {syntax})\n")
            exit(53)

    def invoke(self):
        """Specific instruction implementation will be invoked here."""
        ...

    def get_var_or_literal_value(self, arg_index:int):
        value = frames.get_variable(self.name, self.order, self.arguments[arg_index].type, self.arguments[arg_index].value)
        if value is None:
            value = self.arguments[arg_index].value
        return value


class Move(Instruction):
    def __init__(self, element: Element):
        #TODO: arguments syntax check? number, types?
        super().__init__(element)

    def invoke(self):
        value = self.get_var_or_literal_value(1)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, value)


class CreateFrame(Instruction):
    def invoke(self):
        frames.temporary_frame = {}


class PushFrame(Instruction):
    def invoke(self):
        if frames.temporary_frame is not None:
            frames.local_frames.append(frames.temporary_frame)
            frames.temporary_frame = None
        else:
            stderr.write(f"{self.name} (order: {self.order}): Attempt to access undefined temporary frame.\n")
            exit(55)


class PopFrame(Instruction):
    def invoke(self):
        try:
            frames.temporary_frame = frames.local_frames.pop()
        except IndexError:
            stderr.write(f"{self.name} (order: {self.order}): No local frame available.\n")
            exit(55)


class Defvar(Instruction):
    def invoke(self):
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, defined_check=True, value=None)


class Pushs(Instruction):
    stack = []

    def invoke(self):
        self.stack.append(self.arguments[0].value)


class Pops(Instruction):
    def invoke(self):
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, value=Pushs.stack.pop())


class Add(Instruction):
    def invoke(self):
        result = self.get_var_or_literal_value(1) + self.get_var_or_literal_value(2)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class Sub(Instruction):
    def invoke(self):
        result = self.get_var_or_literal_value(1) - self.get_var_or_literal_value(2)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class Mul(Instruction):
    def invoke(self):
        result = self.get_var_or_literal_value(1) * self.get_var_or_literal_value(2)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class IDiv(Instruction):
    def invoke(self):
        try:
            result = self.get_var_or_literal_value(1) // self.get_var_or_literal_value(2)
        except ZeroDivisionError:
            stderr.write(f"{self.name} (order: {self.order}): Division by zero.\n")
            exit(57)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class Write(Instruction):
    def invoke(self):
        if self.arguments[0].type == "bool":
            print("true" if self.arguments[0].value else "false", end="")

        elif self.arguments[0].type == "nil":
            print("", end="")

        elif self.arguments[0].type == "var":
            print(frames.get_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value), end="")
            
        else:
            print(self.arguments[0].value, end="")
