<?php # IPP parser (autor: Tomáš Milostný, xmilos02)

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

$order = 1;
while (($token = $scanner->GetNextToken())->Type != TokenType::EOF)
{
    //TODO: Load arguments based on syntax defined in OPCODES dictionary
    if ($token->Type == TokenType::OPCODE)
    {
        echo "\t<instruction order=\"" . $order++ . "\" opcode=\"" . $token->Attribute . "\">\n";

        //TODO: Print argument tags

        echo "\t</instruction>\n"; //Konec instrukce
    }
}

echo "</program>\n"; //Konec programu
?>