<?php # Pomocné struktury pro práci s instrukcemi jazyka IPPcode21

class Instruction
{
    //Operační kódy IPPcode21 a syntaxe jejich argumentů
    private const OPCODES = array
    (
        //Práce s rámci, volání funkcí
        "MOVE" => array( "var", "symb" , "\n" ),
        "CREATEFRAME" => array( "\n" ),
        "PUSHFRAME" => array( "\n" ),
        "POPFRAME" => array( "\n" ),
        "DEFVAR" => array( "var", "\n" ),
        "CALL" => array( "label", "\n" ),
        "RETURN" => array( "\n" ),

        //Práce s datovým zásobníkem
        "PUSHS" => array( "symb", "\n" ),
        "POPS" => array( "var", "\n" ),

        //Aritmetické, relační, booleovské a konverzní instrukce
        "ADD" => array( "var", "symb", "symb", "\n" ),
        "SUB" => array( "var", "symb", "symb", "\n" ),
        "MUL" => array( "var", "symb", "symb", "\n" ),
        "IDIV" => array( "var", "symb", "symb", "\n" ),
        "LT" => array( "var", "symb", "symb", "\n" ),
        "GT" => array( "var", "symb", "symb", "\n" ),
        "EQ" => array( "var", "symb", "symb", "\n" ),
        "AND" => array( "var", "symb", "symb", "\n" ),
        "OR" => array( "var", "symb", "symb", "\n" ),
        "NOT" => array( "var", "symb", "symb", "\n" ),
        "INT2CHAR" => array( "var", "symb", "\n" ),
        "STRI2INT" => array( "var", "symb", "symb", "\n" ),

        //Vstupně-výstupní instrukce
        "READ" => array( "var", "type", "\n" ),
        "WRITE" => array( "symb", "\n" ),

        //Práce s řetězci
        "CONCAT" => array( "var", "symb", "symb", "\n" ),
        "STRLEN" => array( "var", "symb", "\n" ),
        "GETCHAR" => array( "var", "symb", "symb", "\n" ),
        "SETCHAR" => array( "var", "symb", "symb", "\n" ),

        //Práce s typy
        "TYPE" => array( "var", "symb", "\n" ),

        //Instrukce pro řízení toku programu
        "LABEL" => array( "label", "\n" ),
        "JUMP" => array( "label", "\n" ),
        "JUMPIFEQ" => array( "label", "symb", "symb", "\n" ),
        "JUMPIFNEQ" => array( "label", "symb", "symb", "\n" ),
        "EXIT" => array( "symb", "\n" ),

        //Ladicí instrukce
        "DPRINT" => array( "symb", "\n" ),
        "BREAK" => array( "\n" )
    );

    public function IsOpcode($word)
    {
        return array_key_exists(strtoupper($word), self::OPCODES);
    }
}
?>