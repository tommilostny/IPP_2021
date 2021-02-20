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

$lang = $token->Attribute;
$instructions = array();

for ($order = 1; ($token = $scanner->GetNextToken())->Type != TokenType::EOF;)
{
    //přeskočit prázdné řádky
    if ($token->Type == TokenType::EOL) continue;

    $instruction = new Instruction($token, $order++, $scanner);
    array_push($instructions, $instruction);
}

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<program language=\"$lang\">\n";

foreach ($instructions as $instruction)
{
    $instruction->Print();
}
echo "</program>\n"; //Konec programu
?>