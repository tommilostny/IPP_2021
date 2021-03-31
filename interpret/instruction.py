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


def set_variable(instr_name:str, instr_order:int, type:str, var:str, value):
    global global_frame, local_frames, temporary_frame
    if type == "var":
        frame, _, varname = var.partition("@")

        if frame == "GF":
            global_frame[varname] = value

        elif frame == "LF" and len(local_frames):
            local_frames[-1][varname] = value

        elif frame == "TF" and temporary_frame is not None:
            temporary_frame[varname] = value

        else:
            stderr.write(f"{instr_name}: (order: {instr_order}): Invalid variable \"{var}\"\n")
            exit(52)
    else:
        stderr.write(f"{instr_name}: (order: {instr_order}): Bad argument type \"{type}\"\n")
        exit(52)


def get_variable(instr_name:str, instr_order:int, type:str, var:str):
    global global_frame, local_frames, temporary_frame
    if type == "var":
        frame, _, varname = var.partition("@")

        if frame == "GF" and varname in global_frame.keys():
            value = global_frame[varname]

        elif frame == "LF" and len(local_frames) and varname in local_frames[-1].keys():
            value = local_frames[-1][varname]

        elif frame == "TF" and temporary_frame is not None and varname in temporary_frame.keys():
            value = temporary_frame[varname]

        else:
            stderr.write(f"{instr_name}: (order: {instr_order}): Invalid variable \"{var}\"\n")
            exit(52)

        return value
    return None


class Move(Instruction):
    def invoke(self):
        value = get_variable("MOVE", self.order, self.arguments[1].type, self.arguments[1].value)
        if value is None:
            value = self.arguments[1].value
        set_variable("MOVE", self.order, self.arguments[0].type, self.arguments[0].value, value)


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
        set_variable("DEFVAR", self.order, self.arguments[0].type, self.arguments[0].value, None)


class Write(Instruction):
    def invoke(self):
        if self.arguments[0].type == "bool":
            print("true" if self.arguments[0].value else "false", end="")
        elif self.arguments[0].type == "nil":
            print("", end="")
        elif self.arguments[0].type == "var":
            print(get_variable("WRITE", self.order, self.arguments[0].type, self.arguments[0].value), end="")
        else:
            print(self.arguments[0].value, end="")
