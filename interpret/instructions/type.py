import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Type(InstructionBase):
    def invoke(self):
        try:
            symbType = type(frames.get(self, 1, exit_on_uninitialized=False))
            if symbType is int:
                result_type = "int"
            elif symbType is bool:
                result_type = "bool"
            elif symbType is str:
                result_type = "string"
            else:
                result_type = "nil"

            frames.set(self, 0, result_type)

        except TypeError:
            frames.set(self, 0, "")
