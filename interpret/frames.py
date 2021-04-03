from sys import exit, stderr

global_frame = {}
local_frames = []
temporary_frame = None

def set_variable(instr_name:str, instr_order:int, type:str, var:str, value, defined_check:bool=False):
    global global_frame, local_frames, temporary_frame
    if type == "var":
        frame, _, varname = var.partition("@")

        if frame == "GF" and (not defined_check or varname not in global_frame.keys()):
            global_frame[varname] = value

        elif frame == "LF" and len(local_frames) and (not defined_check or varname not in local_frames[-1].keys()):
            local_frames[-1][varname] = value

        elif frame == "TF" and temporary_frame is not None and (not defined_check or varname not in temporary_frame.keys()):
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
