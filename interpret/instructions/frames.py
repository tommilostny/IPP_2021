from typing import Any, Dict, List, Tuple

from error import exit_instruction_error

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
            exit_instruction_error(instr, 54, f"Invalid variable \"{instr.arguments[arg_index].value}\"")
    else:
        exit_instruction_error(instr, 52, f"Bad argument type \"{instr.arguments[arg_index].type}\"")
    

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
            exit_instruction_error(instr, 54, f"Invalid variable \"{instr.arguments[arg_index].value}\"")

        if not initialized:
            exit_instruction_error(instr, 52, f"Uninitialized variable {varname}")
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
            exit_instruction_error(self, 55, "Attempted to access undefined temporary frame")


class PopFrame(InstructionBase):
    def invoke(self):
        global temporary_frame
        try:
            temporary_frame = local_frames.pop()
        except IndexError:
            exit_instruction_error(self, 55, "No local frame available")


class Defvar(InstructionBase):
    def invoke(self):
        set(self, 0, _defining=True, value=None)
