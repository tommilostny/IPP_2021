from sys import exit, stderr
from typing import List

import instructions.flow_control as flow_control
from instructions.instruction_base import InstructionBase

#Zásobník volání, obsahuje "návratové adresy" (inkrementovanou pozici v seznamu instrukcí)
call_stack:List[int] = []


class Call(InstructionBase):
    def invoke(self) -> int:
        if self.arguments[0].value not in flow_control.labels.keys():
            stderr.write(f"{self.name} (order: {self.order}): Label {self.arguments[0].value} does not exist.\n")
            exit(52)
        
        call_stack.append(flow_control.instruction_counter + 1)
        return flow_control.labels[self.arguments[0].value]


class Return(InstructionBase):
    def invoke(self) -> int:
        if len(call_stack) == 0:
            stderr.write(f"{self.name} (order: {self.order}): No return address in call stack.\n")
            exit(56)

        return call_stack.pop()
