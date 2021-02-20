<?php # Lexikální analyzátor

include_once("instruction.php");
include_once("argument.php");

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
    public $Line;
    public $Position;
}

class Scanner
{
    private $File = STDIN;
    private $Line = 1;
    private $Position = 0;

    public function GetNextToken()
    {
        if (!$this->EofCheckSet($token = new Token()))
        {
            switch ($word = $this->LoadWord())
            {
            case ".":
                $token->Type = TokenType::HEADER;
                $token->Attribute = $this->LoadWord();
                break;
            case "\n":
                $token->Type = TokenType::EOL;
                break;
            default:
                if (Instruction::IsOpcode($word))
                {
                    $token->Type = TokenType::OPCODE;
                    $token->Attribute = strtoupper($word);
                }
                else if (($type = Argument::ResolveArgumentType($word)) != NULL)
                {
                    $token->Type = TokenType::ARGUMENT;
                    $token->Attribute = array($type, preg_replace("/^(string|int|bool|nil)@/", "", $word));
                }
                else if (!$this->EofCheckSet($token))
                {
                    $token->Type = TokenType::LEX_ERROR;
                    $token->Attribute = $word;
                }
                break;
            }
        }
        $token->Line = $this->Line;
        $token->Position = $this->Position;
        return $token;
    }

    private function LoadWord()
    {
        //přeskočit bílé znaky a komentáře
        $inComment = false;
        $read = $this->ReadChar();
        while ($inComment || (ctype_space($read) && $read != "\n") || (!$inComment && $read == "#"))
        {
            if ($read == "\n" && $inComment)
            {
                fseek($this->File, -1, SEEK_CUR);
                $inComment = false;
            }
            else if ($read == "#")
            {
                $inComment = true;
            }

            if (feof($this->File)) break;
            $read = $this->ReadChar();
        }

        //načtení slova do dalšího bílého znaku
        $string = $read;
        while ($string != "\n" && !ctype_space($read = $this->ReadChar()))
        {
            if ($read == "#") break;

            $string .= $read;

            if (feof($this->File)) break;
        }

        //konec slova je na konci řádku nebo nalezen začátek komentáře -> příští token bude typu EOL
        if (($read == "\n" && strlen($string) > 1) || $read == "#")
        {
            fseek($this->File, -1, SEEK_CUR);
        }
        return $string;
    }

    private function EofCheckSet(Token $token)
    {
        if (feof($this->File))
        {
            $token->Type = TokenType::EOF;
            return true;
        }
        return false;
    }

    private function ReadChar()
    {
        $read = fgetc($this->File);
        if ($read == "\n")
        {
            $this->Line++;
            $this->Position = 0;
        }
        else
        {
            $this->Position++;
        }
        return $read;
    }
}