from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _BooleanInstructionBase(InstructionBase):
    def invoke(self, operation):
        value1 = frames.get_var_or_literal_value(self, 1)
        value2 = frames.get_var_or_literal_value(self, 2)
        
        if type(value1) is bool and type(value2) is bool:
            result = operation(value1, value2)
            frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)
        else:
            stderr.write(f"{self.name} (order: {self.order}): Invalid types of operands {type(value1).__name__} and {type(value2).__name__}.\n")
            exit(53)


class And(_BooleanInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 and x2)


class Or(_BooleanInstructionBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 or x2)


class Not(InstructionBase):
    def invoke(self):
        value = frames.get_var_or_literal_value(self, 1)
        
        if type(value) is bool:
            result = not value
            frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)
        else:
            stderr.write(f"{self.name} (order: {self.order}): Invalid type of operand {type(value).__name__}.\n")
            exit(53)
