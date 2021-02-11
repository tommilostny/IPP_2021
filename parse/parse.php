<?php # IPP parser (autor: Tomáš Milostný, xmilos02)

//Třída Scanner pro lexikální analýzu
include_once("scanner.php");
$scanner = new Scanner();

//Zpracování chyb
include_once("error.php");

//Načtení prvního tokenu a kontrola hlavičky (chybná hlavička -> kód 21)
$token = $scanner->GetNextToken();
if ($token->Type != HEADER || $token->Attribute != SUPPORTED_LANG)
{
    ExitHeaderError();
}

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<program language=\"" . $token->Attribute . "\">\n";

//TODO: načtení instrukcí programu

echo "</program>\n"; //Konec programu
?>