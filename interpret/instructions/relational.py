from sys import exit, stderr

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _RelationalOperationBase(InstructionBase):
    def invoke(self, comparison):
        value1 = frames.get_var_or_literal_value(self, 1)
        value2 = frames.get_var_or_literal_value(self, 2)
        
        if type(value1) is type(value2) and value1 is not None and value2 is not None:
            result = comparison(value1, value2)
            frames.set_variable(self.name, self.order, self.arguments[0].type, self.arguments[0].value, result)
        else:
            stderr.write(f"{self.name} (order: {self.order}): Cannot compare {type(value1).__name__} and {type(value2).__name__}.\n")
            exit(53)


class Lt(_RelationalOperationBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 < x2)


class Gt(_RelationalOperationBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 > x2)


class Eq(_RelationalOperationBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 == x2)
