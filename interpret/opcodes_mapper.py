from xml.etree.ElementTree import Element

from instructions.instruction_base import InstructionBase
from instructions.frames import Move, CreateFrame, PushFrame, PopFrame, Defvar
from instructions.stack import Pops, Pushs
from instructions.arithmetic import Add, Sub, Mul, IDiv
from instructions.relational import Lt, Gt, Eq
from instructions.boolean import And, Or, Not
from instructions.convertions import Int2Char, Stri2Int
from instructions.io import Write
from instructions.string import Concat, Strlen, Getchar, Setchar
from instructions.type import Type


def decode_opcode(instr_element:Element) -> InstructionBase:
    """Returns instance of an instruction subclass based on opcode."""

    opcodes_row = OPCODES.get(instr_element.attrib["opcode"], { "class" : InstructionBase, "syntax" : []})

    #construct Instruction based object
    return opcodes_row["class"](instr_element, opcodes_row["syntax"])


OPCODES = {
    #Práce s rámci, volání funkcí
    "MOVE"        : { "class" : Move       , "syntax" : ["var", "symb"] },
    "CREATEFRAME" : { "class" : CreateFrame, "syntax" : [] },
    "PUSHFRAME"   : { "class" : PushFrame  , "syntax" : [] },
    "POPFRAME"    : { "class" : PopFrame   , "syntax" : [] },
    "DEFVAR"      : { "class" : Defvar     , "syntax" : ["var"] },
    #"CALL"       : { "class" : Call       , "syntax" : ["label"] },
    #"RETURN"     : { "class" : Return     , "syntax" : [] },

    #Práce s datovým zásobníkem
    "PUSHS" : { "class" : Pushs, "syntax" : ["symb"] },
    "POPS"  : { "class" : Pops , "syntax" : ["var"] },

    #Aritmetické, relační, booleovské a konverzní instrukce
    "ADD"  : { "class" : Add , "syntax" : ["var", "symb", "symb"] },
    "SUB"  : { "class" : Sub , "syntax" : ["var", "symb", "symb"] },
    "MUL"  : { "class" : Mul , "syntax" : ["var", "symb", "symb"] },
    "IDIV" : { "class" : IDiv, "syntax" : ["var", "symb", "symb"] },
    "LT"   : { "class" : Lt  , "syntax" : ["var", "symb", "symb"] },
    "GT"   : { "class" : Gt  , "syntax" : ["var", "symb", "symb"] },
    "EQ"   : { "class" : Eq  , "syntax" : ["var", "symb", "symb"] },
    "AND"  : { "class" : And , "syntax" : ["var", "symb", "symb"] },
    "OR"   : { "class" : Or  , "syntax" : ["var", "symb", "symb"] },
    "NOT"  : { "class" : Not , "syntax" : ["var", "symb"] },
    "INT2CHAR" : { "class" : Int2Char , "syntax" : ["var", "symb"] },
    "STRI2INT" : { "class" : Stri2Int , "syntax" : ["var", "symb", "symb"] },

    #Vstupně-výstupní instrukce
    #"READ" : { "class" : Read , "syntax" : ["var", "type"] },
    "WRITE" : { "class" : Write, "syntax" : ["symb"] },

    #Práce s řetězci
    "CONCAT"  : { "class" : Concat , "syntax" : ["var", "symb", "symb"] },
    "STRLEN"  : { "class" : Strlen , "syntax" : ["var", "symb"] },
    "GETCHAR" : { "class" : Getchar, "syntax" : ["var", "symb", "symb"] },
    "SETCHAR" : { "class" : Setchar, "syntax" : ["var", "symb", "symb"] },

    #Práce s typy
    "TYPE" : { "class" : Type, "syntax" : ["var", "symb"] },

    #Instrukce pro řízení toku programu
    #"LABEL"     : { "class" : Label    , "syntax" : ["label"] },
    #"JUMP"      : { "class" : Jump     , "syntax" : ["label"] },
    #"JUMPIFEQ"  : { "class" : JumpIfEq , "syntax" : ["label", "symb", "symb"] },
    #"JUMPIFNEQ" : { "class" : JumpIfNeq, "syntax" : ["label", "symb", "symb"] },
    #"EXIT"      : { "class" : Exit     , "syntax" : ["symb"] },

    #Ladicí instrukce
    #"DPRINT" : { "class" : Dprint, "syntax" : ["symb"] },
    #"BREAK"  : { "class" : Break, "syntax" : [] } 
}
