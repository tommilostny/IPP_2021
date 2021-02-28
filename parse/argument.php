<?php

include_once("scanner.php");

class Argument
{
	private $Type;
	private $Value;
	private $Order;

	private const SYMBS = array("int", "bool", "string", "nil", "var");

	public function __construct(Token $token, int $order, string $syntaxSymbol)
	{
		if ($token->Type != TokenType::ARGUMENT)
			ExitOtherError($token->Attribute);

		$this->Type = $token->Attribute[0];
		$this->Value = $token->Attribute[1];
		$this->Order = $order;

		switch ($syntaxSymbol)
		{
		case "var":
			if ($this->Type != "var")
				ExitOtherError($this->Type);
			break;
		case "symb":
			if (!in_array($this->Type, self::SYMBS))
				ExitOtherError($this->Type);
			break;
		case "label":
			if ($this->Type != "label")
				ExitOtherError($this->Type);
			break;
		case "type":
			if ($this->Type != "type")
				ExitOtherError($this->Type);
			break;
		}
	}

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

	public function ResolveArgumentType(string $string)
	{
		foreach (self::ARGTYPES as $pattern => $type)
		{
			if (preg_match($pattern, $string))
				return $type;
		}
		return NULL;
	}

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