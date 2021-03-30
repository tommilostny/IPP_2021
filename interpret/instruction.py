from sys import exit, stderr
from typing import List
from xml.etree.ElementTree import Element

from argument import Argument

global_frame = {}
local_frames = []
temporary_frame = None

class Instruction:
    def __init__(self, element:Element):
        self.order = int(element.attrib["order"])
        self.arguments = List[Argument]()
        for argument in element:
            self.arguments.append(Argument(argument))

    def invoke(self):
        """Specific instruction implementation will be invoked here."""
        ...

class CreateFrame(Instruction):
    def invoke(self):
        global temporary_frame
        temporary_frame = {}

class PushFrame(Instruction):
    def invoke(self):
        global temporary_frame, local_frames
        if temporary_frame is not None:
            local_frames.append(temporary_frame)
            temporary_frame = None
        else:
            stderr.write(f"PUSHFRAME (order: {self.order}): Attempt to access undefined temporary frame.\n")
            exit(55)

class PopFrame(Instruction):
    def invoke(self):
        global temporary_frame, local_frames
        try:
            temporary_frame = local_frames.pop()
        except IndexError:
            stderr.write(f"POPFRAME (order: {self.order}): No local frame available.\n")
            exit(55)

class Write(Instruction):
    def invoke(self):
        if self.arguments[0].type == "bool":
            print("true" if self.arguments[0].value else "false", end="")
        elif self.arguments[0].type == "nil":
            print("", end="")
        else:
            print(self.arguments[0].value, end="")
