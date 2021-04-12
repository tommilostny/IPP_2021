from sys import stderr

import instructions.frames as frames
import instructions.flow_control as flow_control
from instructions.instruction_base import InstructionBase


instructions_computed = 0
last_instruction_index = 0
break_instruction_present = False


class Dprint(InstructionBase):
    def invoke(self):
        stderr.write(str(frames.get_var_or_literal_value(self, 0)))


class Break(InstructionBase):
    def __init__(self, element, syntax_symbols):
        global break_instruction_present
        break_instruction_present = True

        super().__init__(element, syntax_symbols)

    def invoke(self):
        stderr.write(f"Stav rámců:\n\tGF:  {frames.global_frame}\n")
        stderr.write(f"\tLFs: {frames.local_frames}\n")
        stderr.write(f"\tTF:  {frames.temporary_frame}\n")
        stderr.write(f"Počet vykonaných instrukcí: {instructions_computed}\n")
        stderr.write(f"Pozice v kódu: {flow_control.instructions[last_instruction_index]}")
        stderr.write(f" (order: {flow_control.instructions[last_instruction_index].order})\n")


def log_program_progress():
    global instructions_computed, last_instruction_index
    if break_instruction_present:
        instructions_computed += 1
        last_instruction_index = flow_control.instruction_counter - 1
