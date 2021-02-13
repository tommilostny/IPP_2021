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

do
{
    $token = $scanner->GetNextToken();
    echo "Token type: " . $token->Type;
    echo "Token attribute: " . $token->Attribute;
    echo "\n";
}
while ($token->Type != TokenType::EOF);

echo "</program>\n"; //Konec programu
?>