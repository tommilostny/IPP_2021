from sys import exit, stderr

from instructions.instruction_base import InstructionBase


global_frame = {}
local_frames = []
temporary_frame = None


def set_variable(instr_name:str, instr_order:int, type:str, var:str, value, _define:bool=False):
    global global_frame, local_frames, temporary_frame
    if type == "var":
        frame, _, varname = var.partition("@")

        if frame == "GF" and (not _define or varname not in global_frame.keys()):
            global_frame[varname] = (value, not _define)

        elif frame == "LF" and len(local_frames) and (not _define or varname not in local_frames[-1].keys()):
            local_frames[-1][varname] = (value, not _define)

        elif frame == "TF" and temporary_frame is not None and (not _define or varname not in temporary_frame.keys()):
            temporary_frame[varname] = (value, not _define)

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
            value, initialized = global_frame[varname]

        elif frame == "LF" and len(local_frames) and varname in local_frames[-1].keys():
            value, initialized = local_frames[-1][varname]

        elif frame == "TF" and temporary_frame is not None and varname in temporary_frame.keys():
            value, initialized = temporary_frame[varname]

        else:
            stderr.write(f"{instr_name}: (order: {instr_order}): Invalid variable \"{var}\"\n")
            exit(52)

        if initialized:
            return value
        else:
            stderr.write(f"{instr_name}: (order: {instr_order}): Uninitialized variable {varname}.\n")
            exit(52)
    return None


def get_var_or_literal_value(instr:InstructionBase, arg_index:int):
    value = get_variable(instr.name, instr.order, instr.arguments[arg_index].type, instr.arguments[arg_index].value)
    if value is None and instr.arguments[arg_index].type != "var":
        value = instr.arguments[arg_index].value
    return value


class Move(InstructionBase):
    def invoke(self):
        value = get_var_or_literal_value(self, 1)
        set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, value)


class CreateFrame(InstructionBase):
    def invoke(self):
        global temporary_frame
        temporary_frame = {}


class PushFrame(InstructionBase):
    def invoke(self):
        global temporary_frame
        if temporary_frame is not None:
            local_frames.append(temporary_frame)
            temporary_frame = None
        else:
            stderr.write(f"{self.name} (order: {self.order}): Attempt to access undefined temporary frame.\n")
            exit(55)


class PopFrame(InstructionBase):
    def invoke(self):
        global temporary_frame
        try:
            temporary_frame = local_frames.pop()
        except IndexError:
            stderr.write(f"{self.name} (order: {self.order}): No local frame available.\n")
            exit(55)


class Defvar(InstructionBase):
    def invoke(self):
        set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, _define=True, value=None)
