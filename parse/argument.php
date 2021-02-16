<?php

class Argument
{
    private const ARGTYPES = array
    (
        "/^int@(-)?\d+/" => "int",
        "/^(bool@)((true)|(false))$/" => "bool",
        "/^string@/" => "string",
        "/^((GF)|(LF)|(TF))@([a-z]|[A-Z]|\d|_|-|\\$|&|%|\*|!)+$/" => "var",
        "/^(int|bool|string)$/" => "type", 
        "/^(nil@nil)$/" => "nil",
        "/./" => "label"
    );

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
}

?>