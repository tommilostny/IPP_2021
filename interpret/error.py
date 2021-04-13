from sys import exit, stderr, stdin

from instructions.instruction_base import InstructionBase


def exit_error(message:str, exitcode:int):
    from instructions.io import input_file

    if input_file is not stdin:
        input_file.close()

    stderr.write(f"{message}.\n")
    exit(exitcode)


def exit_instruction_error(instr:InstructionBase, exitcode:int, message:str):
    exit_error(f"{instr.name} (order: {instr.order}): {message}", exitcode)
