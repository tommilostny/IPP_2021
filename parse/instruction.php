<?php # Pomocné struktury pro práci s instrukcemi jazyka IPPcode21

class Instruction
{
    public const OPCODES = array
    (
        //Práce s rámci, volání funkcí
        "MOVE" => array(),
        "CREATEFRAME" => array(),
        "PUSHFRAME" => array(),
        "POPFRAME" => array(),
        "DEFVAR" => array(),
        "CALL" => array(),
        "RETURN" => array(),

        //Práce s datovým zásobníkem
        "PUSHS" => array(),
        "POPS" => array(),

        //Aritmetické, relační, booleovské a konverzní instrukce
        "ADD" => array(),
        "SUB" => array(),
        "MUL" => array(),
        "IDIV" => array(),
        "LT" => array(),
        "GT" => array(),
        "EQ" => array(),
        "AND" => array(),
        "OR" => array(),
        "NOT" => array(),
        "INT2CHAR" => array(),
        "STRI2INT" => array(),

        //Vstupně-výstupní instrukce
        "READ" => array(),
        "WRITE" => array(),

        //Práce s řetězci
        "CONCAT" => array(),
        "STRLEN" => array(),
        "GETCHAR" => array(),
        "SETCHAR" => array(),

        //Práce s typy
        "TYPE" => array(),

        //Instrukce pro řízení toku programu
        "LABEL" => array(),
        "JUMP" => array(),
        "JUMPIFEQ" => array(),
        "JUMPIFNEQ" => array(),
        "EXIT" => array(),

        //Ladicí instrukce
        "DPRINT" => array(),
        "BREAK" => array()
    );

    private const ARGTYPES = array
    (
        "/^int@(-)?\d+/" => "int",
        "/^(bool@)((true)|(false))$/" => "bool",
        "/^string@/" => "string",
        "/^((GF)|(LF)|(TF))@([a-z]|[A-Z]|\d|_|-|\\$|&|%|\*|!)+$/" => "var",
        "/^(int|bool|string)$/" => "type", 
        "/^(nil@nil)$/" => "nil",
        "/./" => "label"
    );

    public function ResolveArgumentType(string $string)
    {
        foreach (self::ARGTYPES as $pattern => $type)
        {
            if (preg_match($pattern, $string))
            {
                echo "Found match: \"".$string."\" is ".$type.".\n";
                return $type;
            }
        }
        return NULL;
    }
}
?>