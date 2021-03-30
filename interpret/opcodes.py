from instruction import *

def decode_opcode(instr_element:Element) -> Instruction:
        """Returns instance of an instruction subclass based on opcode."""
        return OPCODES.get(instr_element.attrib["opcode"], Instruction)(instr_element)

OPCODES = {
    #Práce s rámci, volání funkcí
    #"MOVE" : Move,
    "CREATEFRAME" : CreateFrame,
    "PUSHFRAME" : PushFrame,
    "POPFRAME" : PopFrame,
    "DEFVAR" : Defvar,
    #"CALL" : Call,
    #"RETURN" : Return,

    #Práce s datovým zásobníkem
    #"PUSHS" : Pushs,
    #"POPS" : Pops,

    #Aritmetické, relační, booleovské a konverzní instrukce
    #"ADD" : Add,
    #"SUB" : Sub,
    #"MUL" : Mul,
    #"IDIV" : Idiv,
    #"LT" : Lt,
    #"GT" : Gt,
    #"EQ" : Eq,
    #"AND" : And,
    #"OR" : Or,
    #"NOT" : Not,
    #"INT2CHAR" : Int2Char,
    #"STRI2INT" : Stri2Int,

    #Vstupně-výstupní instrukce
    #"READ" : Read,
    "WRITE" : Write,

    #Práce s řetězci
    #"CONCAT" : Concat,
    #"STRLEN" : Strlen,
    #"GETCHAR" : Getchar,
    #"SETCHAR" : Setchar,

    #Práce s typy
    #"TYPE" : Type,

    #Instrukce pro řízení toku programu
    #"LABEL" : Label,
    #"JUMP" : Jump,
    #"JUMPIFEQ" : JumpIfEq,
    #"JUMPIFNEQ" : JumpIfNeq,
    #"EXIT" : Exit,

    #Ladicí instrukce
    #"DPRINT" : Dprint,
    #"BREAK" :Break 
}
