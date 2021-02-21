<?php # IPPcode21 parser (autor: Tomáš Milostný, xmilos02)

ini_set('display_errors', 'stderr');
include_once("error.php");

//kontrola parametru --help
if ($argc >= 2)
{
	if ($argv[1] == "--help")
	{
		echo "IPPcode21 parser (autor: Tomáš Milostný)\n";
		echo "POUŽITÍ:\n\tphp parse.php [--help]\n";
		echo "POPIS:\nSkript typu filtr (parse.php v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPPcode21, zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní výstup XML reprezentaci programu.\n";
		echo "PARAMETRY:\n\t--help\tVýpis nápovědy.\n";
		exit(0);
	}
	else ExitErrorParameter($argv[1]);
}

include_once("instruction.php");
include_once("scanner.php");
$scanner = new Scanner();

//Načtení prvního tokenu a kontrola hlavičky (chybná hlavička -> kód 21)
$token = $scanner->GetNextToken();
if ($token->Type != TokenType::HEADER || $token->Attribute != SUPPORTED_LANG)
{
	ExitHeaderError();
}

$lang = $token->Attribute;
$instructions = array();

//Načtení instrukcí programu
for ($order = 1; ($token = $scanner->GetNextToken())->Type != TokenType::EOF;)
{
	//přeskočit prázdné řádky
	if ($token->Type == TokenType::EOL)
		continue;

	$instruction = new Instruction($token, $order++, $scanner);
	array_push($instructions, $instruction);
}

//Načtení instrukcí proběhlo v pořádku -> výpis XML reprezentace
$xw = new XMLWriter();
$xw->openMemory();
$xw->startDocument("1.0", "UTF-8");
$xw->startElement("program");
$xw->writeAttribute("language", $lang);

foreach ($instructions as $instruction)
	$instruction->Print($xw);

$xw->endElement(); //Konec programu
$xw->endDocument();//Konec dokumentu
echo $xw->flush(); //Výpis XML na stdout
?>