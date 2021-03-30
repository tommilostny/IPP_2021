from sys import exit, stderr
from xml.etree.ElementTree import Element

from argument import Argument

global_frame = {}
local_frames = []
temporary_frame = None

class Instruction:
    def __init__(self, element:Element):
        self.order = int(element.attrib["order"])
        self.arguments = []
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

class Defvar(Instruction):
    def invoke(self):
        global global_frame, local_frames, temporary_frame
        if self.arguments[0].type == "var":
            frame, _, varname = self.arguments[0].value.partition("@")

            if frame == "GF" and varname not in global_frame.keys():
                global_frame[varname] = None

            elif frame == "LF" and len(local_frames) and varname not in local_frames[-1].keys():
                local_frames[-1][varname] = None

            elif frame == "TF" and temporary_frame is not None and varname not in temporary_frame.keys():
                temporary_frame[varname] = None

            else:
                stderr.write(f"DEFVAR: (order: {self.order}): Invalid variable \"{self.arguments[0].value}\"\n")
                exit(52)
        else:
            stderr.write(f"DEFVAR: (order: {self.order}): Bad argument type \"{self.arguments[0].type}\"\n")
            exit(52)

class Write(Instruction):
    def invoke(self):
        if self.arguments[0].type == "bool":
            print("true" if self.arguments[0].value else "false", end="")
        elif self.arguments[0].type == "nil":
            print("", end="")
        else:
            print(self.arguments[0].value, end="")
