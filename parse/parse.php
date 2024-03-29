<?php

/// IPPcode21 parser (autor: Tomáš Milostný, xmilos02)

include_once("error.php");

if ($argc >= 2) //Kontrola parametru --help
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

include_once("scanner.php");
include_once("instruction.php");

$supportedLang = "IPPcode21";
$scanner = new Scanner($supportedLang);
$instructions = array();
$headerLoaded = false;

while (($token = $scanner->GetNextToken())->Type != TokenType::EOF)
{
	if ($token->Type == TokenType::EOL) //Přeskočit prázdné řádky/komentáře
		continue;

	if (!$headerLoaded) //Načtení hlavičky
	{
		if ($token->Type != TokenType::HEADER)
			ExitHeaderError($token->Attribute, $supportedLang, $token->Line, $token->Position);

		$headerLoaded = true;
		continue;
	}

	//Načtení instrukce programu
	$instruction = new Instruction($token, count($instructions) + 1, $scanner);
	array_push($instructions, $instruction);
}

//Načtení instrukcí proběhlo v pořádku -> výpis XML reprezentace
$xw = new XMLWriter();
$xw->openMemory();
$xw->startDocument("1.0", "UTF-8");
$xw->startElement("program");
$xw->writeAttribute("language", $supportedLang);

foreach ($instructions as $instruction)
	$instruction->Print($xw);

$xw->endElement(); //Konec programu
$xw->endDocument();//Konec dokumentu
echo $xw->flush(); //Výpis XML na stdout

?>