<?php # IPPcode21 parser (autor: Tomáš Milostný, xmilos02)

ini_set('display_errors', 'stderr');

include_once("scanner.php");
$scanner = new Scanner();

include_once("error.php");

//Načtení prvního tokenu a kontrola hlavičky (chybná hlavička -> kód 21)
$token = $scanner->GetNextToken();
if ($token->Type != TokenType::HEADER || $token->Attribute != SUPPORTED_LANG)
{
    ExitHeaderError();
}

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<program language=\"" . $token->Attribute . "\">\n";

$order = 1; # TODO: probably do not need (get from count of instructions array)
$instructions = array();

while (($token = $scanner->GetNextToken())->Type != TokenType::EOF)
{
    //přeskočit prázdné řádky
    if ($token->Type == TokenType::EOL) continue;

    //token obsahuje operační kód instrukce, načíst její argumenty
    if ($token->Type == TokenType::OPCODE) 
    {
        # TODO: push instruction to instructions array

        echo "\t<instruction order=\"" . $order++ . "\" opcode=\"" . $token->Attribute . "\">\n";


        echo "\t</instruction>\n"; //Konec instrukce
    }
}

# TODO: if all went well print all instructions from the array

echo "</program>\n"; //Konec programu
?>