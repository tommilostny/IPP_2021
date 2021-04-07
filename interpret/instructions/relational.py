from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _RelationalOperationBase(InstructionBase):
    def invoke(self, comparison):
        value1 = frames.get_var_or_literal_value(self, 1)
        value2 = frames.get_var_or_literal_value(self, 2)
        
        if type(value1) is not type(value2) or value1 is None or value2 is None:
            stderr.write(f"{self.name} (order: {self.order}): Cannot compare {type(value1).__name__} and {type(value2).__name__}.\n")
            exit(53)
        result = comparison(value1, value2)
        frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)


class Lt(_RelationalOperationBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 < x2)


class Gt(_RelationalOperationBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 > x2)


class Eq(_RelationalOperationBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 == x2)
