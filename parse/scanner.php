<?php # Lexikální analyzátor

include_once("instruction.php");

class TokenType
{
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
        $currText = "";
        $continueRead = true;
        $loadingHeader = false;

        while ($continueRead)
        {
            if (feof($this->File))
            {
                $token->Type = TokenType::EOF;
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
                    $token->Type = TokenType::HEADER;
                    break;
                }

                $currText .= $lastChar;
            }
        }
        return $token;
    }
}

?>