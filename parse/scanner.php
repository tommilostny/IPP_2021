<?php

include_once("instruction.php");
include_once("argument.php");
include_once("error.php");

/// Typy tokenů vyskytující se v jazyce IPPcode21
abstract class TokenType
{
	const EOL = "Konec řádku";
	const EOF = "Konec souboru";
	const HEADER = "Hlavička";
	const OPCODE = "Operační kód instrukce";
	const ARGUMENT = "Argument";
}

/// Reprezentace datové struktury tokenu, drží informace o typu, jeho atribut a další.
class Token
{
	var $Type = NULL;
	var $Attribute = NULL;
	var $Line;
	var $Position;
}

/// Třída lexikálního analyzátoru, drží si informace o vstupním souboru.
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

	/// Čte soubor a vrátí odpovídající token, nebo skončí s lexikální chybou.
	public function GetNextToken()
	{
		//Vytvoření nového objektu třidy Token, kontrola konce souboru před čtením
		if (!$this->EofCheckSet($token = new Token()))
		{
			//Uložení pozice v souboru
			$token->Line = $this->Line;
			$token->Position = $this->Position;

			//Načtení slova ze vstupního souboru, kontrola konce řádku
			if (($word = $this->LoadWord()) == "\n")
			{
				$token->Type = TokenType::EOL;
			}
			//Kontrola hlavičky (jazyk dle parametru konstruktoru (IPPcode21))
			else if (preg_match("/^\.$this->Language$/", $word))
			{
				$token->Type = TokenType::HEADER;
				$token->Attribute = $this->Language;
			}
			//Kontrola operačního kódu metodou z třídy Instruction
			else if (Instruction::IsOpcode($word))
			{
				$token->Type = TokenType::OPCODE;
				$token->Attribute = $word;
			}
			//Kontrola argumentu metodou z třídy Argument
			else if (($type = Argument::ResolveArgumentType($word)) != NULL)
			{
				$token->Type = TokenType::ARGUMENT;
				$token->Attribute = array($type, $word);
			}
			//Načtené slovo neodpovídá základním typům tokenu, je konec souboru nebo lexikální chyba
			else if (!$this->EofCheckSet($token))
			{
				ExitLexicalError($word, $token->Line, $token->Position);
			}
		}
		return $token;
	}

	/// Čte vstupní soubor, přeskakuje bílé znaky a komentáře, vrátí se se slovem ke kontrole.
	private function LoadWord()
	{
		//Přeskočit bílé znaky a komentáře
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

		//Načtení slova do dalšího bílého znaku
		$string = $read;
		while ($string != "\n" && !ctype_space($read = $this->ReadChar()) && $read != "#")
		{
			$string .= $read;

			if (feof($this->File))
				break;
		}

		//Konec slova je na konci řádku nebo nalezen začátek komentáře -> příští token bude typu EOL
		if (($read == "\n" && strlen($string) > 1) || $read == "#")
		{
			fseek($this->File, -1, SEEK_CUR);
			$this->Line--;
		}
		return $string;
	}

	/// Kontrola konce souboru, případně nastavení odpovídajícího typu tokenu
	private function EofCheckSet(Token $token)
	{
		if (feof($this->File))
		{
			$token->Type = TokenType::EOF;
			return true;
		}
		return false;
	}

	/// Čte znak ze vstupního souboru, upravuje informaci o pozici v souboru.
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