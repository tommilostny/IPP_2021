<?php

include_once("scanner.php");

/// Třída reprezentující argument instrukce jazyka IPPcode21.
class Argument
{
	private $Type;
	private $Value;
	private $Order;

	public function __construct(Token $token, int $order, string $syntaxSymbol)
	{
		//Token operačního kódu instrukce -> argument typu návěští
		$labelOpcodeException = $syntaxSymbol == "label" && $token->Type == TokenType::OPCODE;

		if (!$labelOpcodeException)
		{
			//kontrola běžného typu argumentu
			if ($token->Type != TokenType::ARGUMENT)
				ExitTokenTypeError($token->Attribute, $token->Type, TokenType::ARGUMENT, $token->Line, $token->Position);

			$this->Type = $token->Attribute[0];
			$this->Value = $token->Attribute[1];
		}
		else //opcode návěští
		{
			$this->Type = "label";
			$this->Value = $token->Attribute;
		}
		$this->Order = $order;

		//Kontrola zda očekáváný terminální symbol odpovídá realitě
		switch ($syntaxSymbol)
		{
			case "var": $syntaxError = $this->Type != "var";
				break;
			case "symb": $syntaxError = !in_array($this->Type, array("int", "bool", "string", "nil", "var"));
				break;
			case "label": $syntaxError = $this->Type != "label";
				break;
			case "type": $syntaxError = $this->Type != "type";
				break;
		}
		if ($syntaxError)
			ExitArgTypeError($this->Type, $this->Value, $syntaxSymbol, $token->Line, $token->Position);
		
		$this->Value = preg_replace("/^(string|int|bool|nil)@/", "", $this->Value);
	}

	/// Možné typy argumentů reprezentovány klíčem (regulární výraz) a hodnotou (jméno typu).
	private const ARGTYPES = array
	(
		"/^int@(-|\+)?\d+$/" => "int",
		"/^bool@(true|false)$/" => "bool",
		"/^string@(((\\\)\d\d\d)|[^\\\])*$/" => "string",
		"/^(G|L|T)F@([a-zA-Z]|\d|_|-|\\$|&|%|\*|!|\?)+$/" => "var",
		"/^(int|bool|string)$/" => "type", 
		"/^(nil@nil)$/" => "nil",
		"/^([a-zA-Z]|\d|_|-|\\$|&|%|\*|!|\?)+$/" => "label"
	);

	/// Zjistí, zda zadaný řetězec odpovídá některému z klíčů v poli ARGTYPES.
	/// Vrací jméno typu nebo NULL.
	public function ResolveArgumentType(string $string)
	{
		foreach (self::ARGTYPES as $pattern => $type)
		{
			if (preg_match($pattern, $string))
				return $type;
		}
		return NULL;
	}

	/// Vytiskne XML reprezentaci argumentu (s využitím knihovny XMLWriter).
	public function Print(XMLWriter $xw)
	{
		$xw->startElement("arg$this->Order");
		$xw->writeAttribute("type", $this->Type);

		if (strlen($this->Value) > 0)
			$xw->text($this->Value);
		
		$xw->endElement();
	}
}

?>