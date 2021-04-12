import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Type(InstructionBase):
    def invoke(self):
        symbType = type(frames.get(self, 1))

        if symbType is int:
            result = "int"
        elif symbType is bool:
            result = "bool"
        elif symbType is str:
            result = "string"
        else:
            result = "nil"

        frames.set(self, 0, result)
