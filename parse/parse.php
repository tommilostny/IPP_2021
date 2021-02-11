<?php # IPP parser (autor: Tomáš Milostný, xmilos02)

//Třída Scanner pro lexikální analýzu
include_once("scanner.php");
$scanner = new Scanner();

const SUPPORTED_LANG = "IPPcode21";

//Načtení prvního tokenu a kontrola hlavičky (chybná hlavička -> kód 21)
$token = $scanner->GetNextToken();
if ($token->Type != HEADER || $token->Attribute != SUPPORTED_LANG)
{
    fwrite(STDERR, "Chybná hlavička. Nutno specifikovat podporovaný jazyk ". SUPPORTED_LANG . ".\n");
    exit(21);
}

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<program language=\"" . $token->Attribute . "\">\n";

//TODO: načtení instrukcí programu

echo "</program>\n"; //Konec programu
?>