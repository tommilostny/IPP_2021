from typing import List

from error import exit_instruction_error

import instructions.flow_control as flow_control
from instructions.instruction_base import InstructionBase

#Zásobník volání, obsahuje "návratové adresy" (inkrementovanou pozici v seznamu instrukcí)
call_stack:List[int] = []


class Call(InstructionBase):
    def invoke(self) -> int:
        if self.arguments[0].value not in flow_control.labels.keys():
            exit_instruction_error(self, 52, f"Label {self.arguments[0].value} does not exist")
        
        call_stack.append(flow_control.program_counter + 1)
        return flow_control.labels[self.arguments[0].value]


class Return(InstructionBase):
    def invoke(self) -> int:
        if len(call_stack) == 0:
            exit_instruction_error(self, 56, "No return address in call stack")

        return call_stack.pop()
