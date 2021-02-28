<?php # Lexikální analyzátor

include_once("instruction.php");
include_once("argument.php");
include_once("error.php");

class TokenType
{
	public const EOL = "Konec řádku";
	public const EOF = "Konec souboru";
	public const HEADER = "Hlavička";
	public const OPCODE = "Operační kód instrukce";
	public const ARGUMENT = "Argument";
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
	private $Language;

	public function __construct(string $lang)
	{
		$this->Language = $lang;
	}

	public function GetNextToken()
	{
		if (!$this->EofCheckSet($token = new Token()))
		{
			$token->Line = $this->Line;
			$token->Position = $this->Position;

			if (($word = $this->LoadWord()) == "\n")
			{
				$token->Type = TokenType::EOL;
			}
			else if (preg_match("/^\.$this->Language$/", $word))
			{
				$token->Type = TokenType::HEADER;
				$token->Attribute = $this->Language;
			}
			else if (Instruction::IsOpcode($word))
			{
				$token->Type = TokenType::OPCODE;
				$token->Attribute = $word;
			}
			else if (($type = Argument::ResolveArgumentType($word)) != NULL)
			{
				$token->Type = TokenType::ARGUMENT;
				$token->Attribute = array($type, $word);
			}
			else if (!$this->EofCheckSet($token))
			{
				ExitLexicalError($word, $token->Line, $token->Position);
			}
		}
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
				$this->Line--;
			}
			else if ($read == "#")
				$inComment = true;

			if (feof($this->File))
				break;

			$read = $this->ReadChar();
		}

		//načtení slova do dalšího bílého znaku
		$string = $read;
		while ($string != "\n" && !ctype_space($read = $this->ReadChar()) && $read != "#")
		{
			$string .= $read;

			if (feof($this->File))
				break;
		}

		//konec slova je na konci řádku nebo nalezen začátek komentáře -> příští token bude typu EOL
		if (($read == "\n" && strlen($string) > 1) || $read == "#")
		{
			fseek($this->File, -1, SEEK_CUR);
			$this->Line--;
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
		else $this->Position++;
		
		return $read;
	}
}