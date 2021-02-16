<?php # Pomocné struktury pro práci s instrukcemi jazyka IPPcode21

class Instruction
{
    private const OPCODES = array
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

    public function IsOpcode($word)
    {
        return array_key_exists(strtoupper($word), self::OPCODES);
    }
}
?>