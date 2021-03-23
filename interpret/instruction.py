from argument import *


class Instruction:
    def __init__(self, order:int):
        self.arguments = [ Argument("int", 100) ]
        self.order = order

    def invoke(self):
        ...

class Write(Instruction):
    def invoke(self):
        print(self.arguments[0].type, self.arguments[0].value)