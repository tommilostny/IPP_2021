from sys import stdin

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


input_file = stdin


class Write(InstructionBase):
    def invoke(self):
        value = frames.get_var_or_literal_value(self, 0)

        if type(value) is bool:
            print(str(value).lower(), end="")
        elif value is None:
            print("", end="")     
        else:
            print(value, end="")


class Read(InstructionBase):
    def invoke(self):
        input_value = input_file.readline()
        required_type = self.arguments[1].value

        try:
            if required_type == "int":
                input_value = int(input_value)

            elif required_type == "bool":
                input_value = input_value.lower() == "true"

            elif required_type != "string":
                raise ValueError()
        except:
            input_value = None

        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, input_value)
