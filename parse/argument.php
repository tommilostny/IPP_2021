<?php

include_once("scanner.php");

class Argument
{
    private const ARGTYPES = array
    (
        "/^int@(-)?\d+/" => "int",
        "/^(bool@)((true)|(false))$/" => "bool",
        "/^string@/" => "string",
        "/^(G|L|T)F@([a-z]|[A-Z]|\d|_|-|\\$|&|%|\*|!)+$/" => "var",
        "/^(int|bool|string)$/" => "type", 
        "/^(nil@nil)$/" => "nil",
        "/./" => "label"
    );

    private const SYMBS = array("int", "bool", "string", "nil", "var");

    private $Type;
    private $Value;
    private $Order;

    public function __construct(Token $token, int $order, string $syntaxSymbol)
    {
        if ($token->Type != TokenType::ARGUMENT)
        {
            ExitOtherError($token->Attribute);
        }
        $this->Type = $token->Attribute[0];
        $this->Value = $token->Attribute[1];
        $this->Order = $order;

        switch ($syntaxSymbol)
        {
            case "var":
                if ($this->Type != "var")
                {
                    ExitOtherError($this->Type);
                }
                break;
            case "symb":
                if (!$this->IsSymb($this->Type))
                {
                    ExitOtherError($this->Type);
                }
                break;
            case "label":
                if ($this->Type != "label")
                {
                    ExitOtherError($this->Type);
                }
                break;
            case "type":
                if ($this->Type != "type")
                {
                    ExitOtherError($this->Type);
                }
                break;
        }
    }

    public function ResolveArgumentType(string $string)
    {
        foreach (self::ARGTYPES as $pattern => $type)
        {
            if (preg_match($pattern, $string))
            {
                return $type;
            }
        }
        return NULL;
    }

    public function Print()
    {
        echo "\t\t<arg$this->Order type=\"$this->Type\"";
        if (strlen($this->Value) > 0)
        {
            echo ">$this->Value</arg$this->Order>\n";
        }
        else
        {
            echo "/>\n";
        }
    }

    private function IsSymb(string $type)
    {
        return in_array($type, self::SYMBS);
    }
}

?>