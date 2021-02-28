<?php

include_once("scanner.php");
include_once("argument.php");
include_once("error.php");

/// Třída reprezentující instrukci jazyka IPPcode21.
class Instruction
{
	private $Arguments = array();
	private $Order;
	private $Opcode;

	public function __construct(Token $token, int $order, Scanner $scanner)
	{
		if ($token->Type != TokenType::OPCODE)
			ExitOpcodeError($token->Attribute, $token->Line, $token->Position);

		$this->Opcode = strtoupper($token->Attribute);
		$this->Order = $order;
		
		foreach (self::OPCODES[$this->Opcode] as $term)
		{
			$token = $scanner->GetNextToken();

			if ($term == "\n")
			{
				if ($token->Type != TokenType::EOL && $token->Type != TokenType::EOF)
					ExitTokenTypeError($token->Attribute, $token->Type, TokenType::EOL, $token->Line, $token->Position);
				continue;
			}

			$argument = new Argument($token, count($this->Arguments) + 1, $term);
			array_push($this->Arguments, $argument);
		}
	}

	/// Operační kódy IPPcode21 a terminální symboly syntaxe jejich argumentů.
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

	/// Zjistí, zda je zadaný řetězec validní operační kód instrukce jazyka IPPcode21 (je klíčem v poli OPCODES).
	public function IsOpcode(string $string)
	{
		return array_key_exists(strtoupper($string), self::OPCODES);
	}

	/// Vytiskne XML reprezentaci instrukce a jejích argumentů (s využitím knihovny XMLWriter).
	public function Print(XMLWriter $xw)
	{
		$xw->startElement("instruction");
		$xw->writeAttribute("order", $this->Order);
		$xw->writeAttribute("opcode", $this->Opcode);
		
		foreach ($this->Arguments as $argument)
			$argument->Print($xw);

		$xw->endElement();
	}
}
?>