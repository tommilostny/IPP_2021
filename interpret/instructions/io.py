import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class Write(InstructionBase):
    def invoke(self):
        if self.arguments[0].type == "bool":
            print("true" if self.arguments[0].value else "false", end="")

        elif self.arguments[0].type == "nil":
            print("", end="")

        elif self.arguments[0].type == "var":
            print(frames.get_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value), end="")
            
        else:
            print(self.arguments[0].value, end="")
