from typing import Any, Callable

from error import exit_instruction_error

import instructions.frames as frames
from instructions.instruction_base import InstructionBase


class _RelationalComparisonBase(InstructionBase):
    def invoke(self, comparison:Callable[[Any, Any], bool], compare_nils:bool):
        value1 = frames.get(self, 1)
        value2 = frames.get(self, 2)
        contains_nil = value1 is None or value2 is None

        if (type(value1) is type(value2) and not contains_nil) or (compare_nils and contains_nil):
            frames.set(self, 0, comparison(value1, value2))
        else:
            exit_instruction_error(self, 53, f"Cannot compare {type(value1).__name__} and {type(value2).__name__}")


class Lt(_RelationalComparisonBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 < x2, False)


class Gt(_RelationalComparisonBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 > x2, False)


class Eq(_RelationalComparisonBase):
    def invoke(self):
        super().invoke(lambda x1, x2: x1 == x2, True)
