from sys import exit, stderr
from typing import Any, Dict, List, Tuple

from instructions.instruction_base import InstructionBase

#Rámec jako slovníková struktura (jméno proměnné -> dvojice (hodnota, inicializováno?))
global_frame    : Dict[str, Tuple[Any, bool]]       = {}
local_frames    : List[Dict[str, Tuple[Any, bool]]] = []
temporary_frame : Dict[str, Tuple[Any, bool]]       = None


def set(instr:InstructionBase, arg_index:int, value:Any, _defining:bool=False):
    global global_frame, local_frames, temporary_frame

    if instr.arguments[arg_index].type == "var":
        frame, _, varname = instr.arguments[arg_index].value.partition("@")

        if frame == "GF" and (not _defining or varname not in global_frame.keys()):
            global_frame[varname] = (value, not _defining)

        elif frame == "LF" and len(local_frames) and (not _defining or varname not in local_frames[-1].keys()):
            local_frames[-1][varname] = (value, not _defining)

        elif frame == "TF" and temporary_frame is not None and (not _defining or varname not in temporary_frame.keys()):
            temporary_frame[varname] = (value, not _defining)

        else:
            stderr.write(f"{instr.name}: (order: {instr.order}): Invalid variable \"{instr.arguments[arg_index].value}\"\n")
            exit(54)
    else:
        stderr.write(f"{instr.name}: (order: {instr.order}): Bad argument type \"{type}\"\n")
        exit(52)
    

def get(instr:InstructionBase, arg_index:int):
    global global_frame, local_frames, temporary_frame

    if instr.arguments[arg_index].type == "var":
        frame, _, varname = instr.arguments[arg_index].value.partition("@")

        if frame == "GF" and varname in global_frame.keys():
            value, initialized = global_frame[varname]

        elif frame == "LF" and len(local_frames) and varname in local_frames[-1].keys():
            value, initialized = local_frames[-1][varname]

        elif frame == "TF" and temporary_frame is not None and varname in temporary_frame.keys():
            value, initialized = temporary_frame[varname]

        else:
            stderr.write(f"{instr.name}: (order: {instr.order}): Invalid variable \"{instr.arguments[arg_index].value}\"\n")
            exit(54)

        if not initialized:
            stderr.write(f"{instr.name}: (order: {instr.order}): Uninitialized variable {varname}.\n")
            exit(52)
    else:
        value = instr.arguments[arg_index].value

    return value


class Move(InstructionBase):
    def invoke(self):
        set(self, 0, get(self, 1))


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
        set(self, 0, _defining=True, value=None)
