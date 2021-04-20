from typing import Any, Dict, List, Tuple

from error import exit_instruction_error

from instructions.instruction_base import InstructionBase
from instructions.type import Type

#Rámec jako slovníková struktura (jméno proměnné -> dvojice (hodnota, inicializováno?))
global_frame    : Dict[str, Tuple[Any, bool]]       = {}
local_frames    : List[Dict[str, Tuple[Any, bool]]] = []
temporary_frame : Dict[str, Tuple[Any, bool]]       = None


def set(instr:InstructionBase, arg_index:int, value:Any, defining:bool=False):
    global global_frame, local_frames, temporary_frame

    if instr.arguments[arg_index].type == "var":
        frame, _, varname = instr.arguments[arg_index].value.partition("@")

        if frame == "GF":
            var_in_frame = varname in global_frame.keys()
            if defining and var_in_frame:
                exit_instruction_error(instr, 52, f"Variable redefinition \"{instr.arguments[arg_index].value}\"")
            elif (not defining and var_in_frame) or (defining and not var_in_frame):
                global_frame[varname] = (value, not defining)
            else:
                exit_instruction_error(instr, 54, f"Undefined variable \"{instr.arguments[arg_index].value}\"")

        elif frame == "LF":
            if len(local_frames) == 0:
                exit_instruction_error(instr, 55, f"Undefined frame \"{instr.arguments[arg_index].value}\"")

            var_in_frame = varname in local_frames[-1].keys()
            
            if defining and var_in_frame:
                exit_instruction_error(instr, 52, f"Variable redefinition \"{instr.arguments[arg_index].value}\"")
            elif (not defining and var_in_frame) or (defining and not var_in_frame):
                local_frames[-1][varname] = (value, not defining)
            else:
                exit_instruction_error(instr, 54, f"Undefined variable \"{instr.arguments[arg_index].value}\"")

        elif frame == "TF":
            if temporary_frame is None:
                exit_instruction_error(instr, 55, f"Undefined frame \"{instr.arguments[arg_index].value}\"")

            var_in_frame = varname in temporary_frame.keys()
            if defining and var_in_frame:
                exit_instruction_error(instr, 52, f"Variable redefinition \"{instr.arguments[arg_index].value}\"")
            elif (not defining and var_in_frame) or (defining and not var_in_frame):
                temporary_frame[varname] = (value, not defining)
            else:
                exit_instruction_error(instr, 54, f"Undefined variable \"{instr.arguments[arg_index].value}\"")

        else:
            exit_instruction_error(instr, 55, f"Invalid frame \"{instr.arguments[arg_index].value}\"")
    else:
        exit_instruction_error(instr, 52, f"Bad argument type \"{instr.arguments[arg_index].type}\"")
    

def get(instr:InstructionBase, arg_index:int, exit_on_uninitialized:bool=True):
    global global_frame, local_frames, temporary_frame

    if instr.arguments[arg_index].type == "var":
        frame, _, varname = instr.arguments[arg_index].value.partition("@")

        if frame == "GF":
            if varname not in global_frame.keys():
                exit_instruction_error(instr, 54, f"Undefined variable \"{instr.arguments[arg_index].value}\"")

            value, initialized = global_frame[varname]

        elif frame == "LF":
            if len(local_frames) == 0:
                exit_instruction_error(instr, 55, f"Undefined frame \"{instr.arguments[arg_index].value}\"")

            if varname not in local_frames[-1].keys():
                exit_instruction_error(instr, 54, f"Undefined variable \"{instr.arguments[arg_index].value}\"")

            value, initialized = local_frames[-1][varname]

        elif frame == "TF":
            if temporary_frame is None:
                exit_instruction_error(instr, 55, f"Undefined frame \"{instr.arguments[arg_index].value}\"")

            if varname not in temporary_frame.keys():
                exit_instruction_error(instr, 54, f"Undefined variable \"{instr.arguments[arg_index].value}\"")
            
            value, initialized = temporary_frame[varname]

        else:
            exit_instruction_error(instr, 55, f"Invalid frame \"{instr.arguments[arg_index].value}\"")

        if not initialized:
            if exit_on_uninitialized:
                exit_instruction_error(instr, 56, f"Uninitialized variable {varname}")
            else:
                raise TypeError()
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
        set(self, 0, defining=True, value=None)
