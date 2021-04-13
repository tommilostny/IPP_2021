from typing import List, Union
from xml.etree.ElementTree import Element

from argument import Argument


class InstructionBase:
    def __init__(self, element:Element, syntax_symbols:List[str]):
        self.name = type(self).__name__.upper()
        format_syntax_err = SyntaxError(f"{self.name}: Bad instruction element {element} {element.attrib} (syntax: {syntax_symbols})")
        
        try: self.order = int(element.attrib["order"])
        except: raise format_syntax_err

        _check_duplicate_order(self)

        if element.tag != "instruction" or len(element.attrib.keys()) != 2 or self.order < 1:
            raise format_syntax_err

        self.arguments = _load_arguments(self, element, syntax_symbols)


    def invoke(self) -> Union[None, int]:
        """Specifická implementace instrukce bude volána zde."""
        ...


def _check_duplicate_order(new_instr:InstructionBase):
    if not hasattr(_check_duplicate_order, "orders"):
        _check_duplicate_order.orders = []

    if new_instr.order not in _check_duplicate_order.orders:
        _check_duplicate_order.orders.append(new_instr.order)
    else:
        from instructions.flow_control import instructions
        for i in instructions:
            if i.order == new_instr.order:
                duplicate_instr = i.name
                break
        raise SyntaxWarning(f"{new_instr.name}: Duplicate order {new_instr.order} with instruction {duplicate_instr}")


def _load_arguments(new_instr:InstructionBase, element:Element, syntax_symbols:List[str]) -> List[Argument]:
    args:List[Argument] = []

    for arg in element:
        try:
            args.append(Argument(arg, syntax_symbols))
        except SyntaxError as e:
            raise SyntaxError(f"{new_instr.name} (order: {new_instr.order}): {e}")

    args.sort(key=lambda x: x.order)

    for i in range(0, len(syntax_symbols)):
        if args[i].order != i:
            raise SyntaxError(f"{new_instr.name} (order: {new_instr.order}): Instruction missing argument {i + 1} (syntax: {syntax_symbols})")

    return args
