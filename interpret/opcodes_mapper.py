from xml.etree.ElementTree import Element

from instructions.instruction_base import InstructionBase
import instructions.frames       as frames
import instructions.function     as function
import instructions.stack        as stack
import instructions.arithmetic   as arithmetic
import instructions.relational   as relational
import instructions.boolean      as boolean
import instructions.convertions  as convertions
import instructions.io           as io
import instructions.string       as string
import instructions.type         as type
import instructions.flow_control as flow_control
import instructions.debug        as debug


def decode_opcode(instr_element:Element) -> InstructionBase:
    """Returns instance of an instruction subclass based on opcode."""
    try:
        opcodes_row = OPCODES[instr_element.attrib["opcode"]]
    except KeyError as e:
        raise KeyError(f"{e} is not a valid opcode")

    #construct Instruction based object
    return opcodes_row["class"](instr_element, opcodes_row["syntax"])


OPCODES = {
    #Práce s rámci, volání funkcí
    "MOVE"        : { "class" : frames.Move       , "syntax" : ["var", "symb"] },
    "CREATEFRAME" : { "class" : frames.CreateFrame, "syntax" : [] },
    "PUSHFRAME"   : { "class" : frames.PushFrame  , "syntax" : [] },
    "POPFRAME"    : { "class" : frames.PopFrame   , "syntax" : [] },
    "DEFVAR"      : { "class" : frames.Defvar     , "syntax" : ["var"] },

    "CALL"   : { "class" : function.Call  , "syntax" : ["label"] },
    "RETURN" : { "class" : function.Return, "syntax" : [] },

    #Práce s datovým zásobníkem
    "PUSHS" : { "class" : stack.Pushs, "syntax" : ["symb"] },
    "POPS"  : { "class" : stack.Pops , "syntax" : ["var"] },

    #Aritmetické, relační, booleovské a konverzní instrukce
    "ADD"  : { "class" : arithmetic.Add , "syntax" : ["var", "symb", "symb"] },
    "SUB"  : { "class" : arithmetic.Sub , "syntax" : ["var", "symb", "symb"] },
    "MUL"  : { "class" : arithmetic.Mul , "syntax" : ["var", "symb", "symb"] },
    "IDIV" : { "class" : arithmetic.IDiv, "syntax" : ["var", "symb", "symb"] },

    "LT" : { "class" : relational.Lt, "syntax" : ["var", "symb", "symb"] },
    "GT" : { "class" : relational.Gt, "syntax" : ["var", "symb", "symb"] },
    "EQ" : { "class" : relational.Eq, "syntax" : ["var", "symb", "symb"] },

    "AND" : { "class" : boolean.And, "syntax" : ["var", "symb", "symb"] },
    "OR"  : { "class" : boolean.Or , "syntax" : ["var", "symb", "symb"] },
    "NOT" : { "class" : boolean.Not, "syntax" : ["var", "symb"] },

    "INT2CHAR" : { "class" : convertions.Int2Char, "syntax" : ["var", "symb"] },
    "STRI2INT" : { "class" : convertions.Stri2Int, "syntax" : ["var", "symb", "symb"] },

    #Vstupně-výstupní instrukce
    #"READ" : { "class" : io.Read , "syntax" : ["var", "type"] },
    "WRITE" : { "class" : io.Write, "syntax" : ["symb"] },

    #Práce s řetězci
    "CONCAT"  : { "class" : string.Concat , "syntax" : ["var", "symb", "symb"] },
    "STRLEN"  : { "class" : string.Strlen , "syntax" : ["var", "symb"] },
    "GETCHAR" : { "class" : string.Getchar, "syntax" : ["var", "symb", "symb"] },
    "SETCHAR" : { "class" : string.Setchar, "syntax" : ["var", "symb", "symb"] },

    #Práce s typy
    "TYPE" : { "class" : type.Type, "syntax" : ["var", "symb"] },

    #Instrukce pro řízení toku programu
    "LABEL"     : { "class" : flow_control.Label    , "syntax" : ["label"] },
    "JUMP"      : { "class" : flow_control.Jump     , "syntax" : ["label"] },
    "JUMPIFEQ"  : { "class" : flow_control.JumpIfEq , "syntax" : ["label", "symb", "symb"] },
    "JUMPIFNEQ" : { "class" : flow_control.JumpIfNeq, "syntax" : ["label", "symb", "symb"] },
    "EXIT"      : { "class" : flow_control.Exit     , "syntax" : ["symb"] },

    #Ladicí instrukce
    "DPRINT" : { "class" : debug.Dprint, "syntax" : ["symb"] },
    "BREAK"  : { "class" : debug.Break, "syntax" : [] } 
}
