<?php # Pomocné třídy lexikálního analyzátoru

//Typy Tokenů
const EOL = -2;
const EOF = -1;
const HEADER = 0;
const OPCODE = 1;
const ARGUMENT = 2;

const OPCODES = array
(
    //Práce s rámci, volání funkcí
    "MOVE", "CREATEFRAME", "PUSHFRAME", "POPFRAME", "DEFVAR", "CALL", "RETURN",
    //Práce s datovým zásobníkem
    "PUSHS", "POPS",
    //Aritmetické, relační, booleovské a konverzní instrukce
    "ADD", "SUB", "MUL", "IDIV", "LT", "GT", "EQ", "AND", "OR", "NOT", "INT2CHAR", "STRI2INT",
    //Vstupně-výstupní instrukce
    "READ", "WRITE",
    //Práce s řetězci
    "CONCAT", "STRLEN", "GETCHAR", "SETCHAR",
    //Práce s typy
    "TYPE",
    //Instrukce pro řízení toku programu
    "LABEL", "JUMP", "JUMPIFEQ", "JUMPIFNEQ", "EXIT",
    //Ladicí instrukce
    "DPRINT", "BREAK"
);

const ARGTYPES = array("int", "bool", "string", "nil", "label", "type", "var");

class Token
{
    public $Type = NULL;
    public $Attribute = NULL;
}

class Scanner
{
    private $File = STDIN;

    public function GetNextToken()
    {
        $token = new Token();
        $currText = "";
        $loadingHeader = false;
        $cnt = 0;

        while ($token->Type == NULL)
        {
            if (feof($this->File))
            {
                $token->Type = EOF;
            }
            else
            {
                $lastChar = fgetc($this->File);
                if ($currText == ". ")
                {
                    $currText = "";
                    $loadingHeader = true;
                }
                elseif ($loadingHeader && $lastChar == "\n")
                {
                    $token->Attribute = $currText;
                    $token->Type = HEADER;
                    break;
                }

                $currText .= $lastChar;
            }
        }
        return $token;
    }
}

?>