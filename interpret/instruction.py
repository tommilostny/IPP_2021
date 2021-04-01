from sys import exit, stderr
from xml.etree.ElementTree import Element

import frames
from argument import Argument


class Instruction:
    def __init__(self, element:Element):
        self.order = int(element.attrib["order"])
        self.arguments = []
        for argument in element:
            self.arguments.append(Argument(argument))

    def invoke(self):
        """Specific instruction implementation will be invoked here."""
        ...


class Move(Instruction):
    def __init__(self, element: Element):
        #TODO: arguments syntax check? number, types?
        super().__init__(element)

    def invoke(self):
        value = frames.get_variable("MOVE", self.order, self.arguments[1].type, self.arguments[1].value)
        if value is None:
            value = self.arguments[1].value
        frames.set_variable("MOVE", self.order, self.arguments[0].type, self.arguments[0].value, value)


class CreateFrame(Instruction):
    def invoke(self):
        frames.temporary_frame = {}


class PushFrame(Instruction):
    def invoke(self):
        if frames.temporary_frame is not None:
            frames.local_frames.append(frames.temporary_frame)
            frames.temporary_frame = None
        else:
            stderr.write(f"PUSHFRAME (order: {self.order}): Attempt to access undefined temporary frame.\n")
            exit(55)


class PopFrame(Instruction):
    def invoke(self):
        try:
            frames.temporary_frame = frames.local_frames.pop()
        except IndexError:
            stderr.write(f"POPFRAME (order: {self.order}): No local frame available.\n")
            exit(55)


class Defvar(Instruction):
    def invoke(self):
        frames.set_variable("DEFVAR", self.order, self.arguments[0].type, self.arguments[0].value, def_check=True, value=None)


class Write(Instruction):
    def invoke(self):
        if self.arguments[0].type == "bool":
            print("true" if self.arguments[0].value else "false", end="")
        elif self.arguments[0].type == "nil":
            print("", end="")
        elif self.arguments[0].type == "var":
            print(frames.get_variable("WRITE", self.order, self.arguments[0].type, self.arguments[0].value), end="")
        else:
            print(self.arguments[0].value, end="")
