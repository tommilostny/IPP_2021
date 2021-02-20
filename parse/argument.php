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

    public $Type;
    private $Value;
    private $Order;

    public function __construct(Token $token, int $order)
    {
        if ($token->Type != TokenType::ARGUMENT)
        {
            echo $token->Type;
            ExitOtherError($token->Attribute);
        }
        $this->Type = $token->Attribute[0];
        $this->Value = $token->Attribute[1];
        $this->Order = $order;
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

    private const SYMBS = array("int", "bool", "string", "nil", "var");

    public function IsSymb(string $type)
    {
        foreach (self::SYMBS as $symb)
        {
            if ($type == $symb) return true;
        }
        return false;
    }

    public function Print()
    {
        echo "    <arg$this->Order type=\"$this->Type\"";
        if (strlen($this->Value) > 0)
        {
            echo ">$this->Value</arg$this->Order>\n";
        }
        else
        {
            echo "/>\n";
        }
    }
}

?>