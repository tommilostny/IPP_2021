<?php # Lexikální analyzátor

include_once("instruction.php");

class TokenType
{
    public const UNKNOWN = -3;
    public const EOL = -2;
    public const EOF = -1;
    public const HEADER = 0;
    public const OPCODE = 1;
    public const ARGUMENT = 2;
    public const LEX_ERROR = 3;
}

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

        if (feof($this->File))
        {
            $token->Type = TokenType::EOF;
        }
        else switch ($word = $this->LoadWord())
        {
            case ".":
                $token->Type = TokenType::HEADER;
                $token->Attribute = $this->LoadWord();
                break;
            case "\n":
                $token->Type = TokenType::EOL;
                break;
            default:
                if (array_key_exists($word, Instruction::OPCODES))
                {
                    $token->Type = TokenType::OPCODE;
                    $token->Attribute = $word;
                }
                else
                {
                    $token->Type = TokenType::UNKNOWN;
                    $token->Attribute = $word;
                }
                break;
        }
        return $token;
    }

    private function LoadWord()
    {
        //přeskočit bílé znaky a komentáře
        $inComment = false;
        $read = fgetc($this->File);
        while ($inComment || (ctype_space($read) && $read != "\n") || (!$inComment && $read == "#"))
        {
            if ($read == "\n" && $inComment)
            {
                fseek($this->File, -1, SEEK_CUR);
                $inComment = false;
            }
            elseif($read == "#")
            {
                $inComment = true;
            }
            $read = fgetc($this->File);
        }

        //načtení slova do dalšího bílého znaku
        $string = $read;
        while ($string != "\n" && !ctype_space($read = fgetc($this->File)))
        {
            $string .= $read;
            if (feof($this->File)) break;
        }
        if ($read == "\n" && strlen($string) > 1) //konec slova je na konci řádku -> příští token bude typu EOL
        {
            fseek($this->File, -1, SEEK_CUR);
        }
        return $string;
    }

    private function ResolveArgType()
    {

    }
}
?>