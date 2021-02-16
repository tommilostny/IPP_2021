<?php

class Argument
{
    #TODO: update regexes probably
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

    private $Type;
    private $Value;

    public function __construct(string $type, $value)
    {
        $this->Type = $type;

        # TODO: process argument value based on type
        $this->Value = $value;
    }

    public function ResolveArgumentType(string $string)
    {
        foreach (self::ARGTYPES as $pattern => $type)
        {
            if (preg_match($pattern, $string))
            {
                echo "Found match: \"".$string."\" is ".$type.".\n"; //DEBUG print
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

    public function Print(int $argOrder)
    {
        #TODO: echo "<arg$argOrder>";
    }
}

?>