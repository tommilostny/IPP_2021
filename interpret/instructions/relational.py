from sys import exit, stderr
from typing import Any, Callable

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _RelationalComparisonBase(InstructionBase):
    def invoke(self, comparison:Callable[[Any, Any], bool]):

        value1 = frames.get(self, 1)
        value2 = frames.get(self, 2)
        
        if type(value1) is not type(value2) or value1 is None or value2 is None:
            stderr.write(f"{self.name} (order: {self.order}): Cannot compare {type(value1).__name__} and {type(value2).__name__}.\n")
            exit(53)

        frames.set(self, 0, comparison(value1, value2))


class Lt(_RelationalComparisonBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 < x2)


class Gt(_RelationalComparisonBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 > x2)


class Eq(_RelationalComparisonBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 == x2)
