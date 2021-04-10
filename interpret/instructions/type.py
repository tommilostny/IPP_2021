import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Type(InstructionBase):
    def invoke(self):
        symbType = type(frames.get_var_or_literal_value(self, 1))

        if symbType is int:
            result = "int"
        elif symbType is bool:
            result = "bool"
        elif symbType is str:
            result = "string"
        else:
            result = "nil"

        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)
