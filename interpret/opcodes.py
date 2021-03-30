from instruction import *

def decode_opcode(instr_element:Element) -> Instruction:
        """Returns instance of an instruction subclass based on opcode."""
        return OPCODES.get(instr_element.attrib["opcode"], Instruction)(instr_element)

OPCODES = {
    "WRITE" : Write,
}
