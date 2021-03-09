<?php

/// Funkce pro zpracování chyb parseru IPPcode21.
/// Vypisuje na standardní chybový výstup.

ini_set('display_errors', 'stderr');

const ERROR_PARAMETER = 10;
const ERROR_INPUT_FILE = 11;
const ERROR_OUTPUT_FILE = 12;

const ERROR_HEADER = 21;
const ERROR_OPCODE = 22;
const ERROR_OTHER = 23;

const ERROR_INTERNAL = 99;

/// Pomocná funkce pro výpis pozice v souboru.
function ErrorLinePosition(int $line, int $position)
{
	fwrite(STDERR, "Řádek $line, Pozice $position: ");
}

/// Chyba při zpracování parametru programu.
function ExitErrorParameter(string $param)
{
	fwrite(STDERR, "Chybný parametr programu: $param\n");
	exit(ERROR_PARAMETER);
}

/// Chybná hlavička (načten jiný typ tokenu, špatný jazyk, ...).
function ExitHeaderError(string $input, string $correctLang, int $line, int $position)
{
	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybná hlavička \"$input\".\nNutno specifikovat podporovaný jazyk \".$correctLang\".\n");
	exit(ERROR_HEADER);
}

/// Chyba typu vstupního argumentu, neodpovídá očekávanému terminálnímu symbolu.
function ExitArgTypeError(string $inputType, string $inputValue, string $expectedType, int $line, int $position)
{
	$moreInfo = "";
	if ($expectedType == "symb")
		$moreInfo = " (proměnná nebo literál)";

	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybný typ argumentu: \"$inputValue\" je \"$inputType\".\nOčekávaný typ: \"$expectedType\"$moreInfo.\n");
	exit(ERROR_OTHER);
}

/// Chyba typu vstupního tokenu, neodpovídá očekávanému typu.
function ExitTokenTypeError($value, string $type, string $expectedType, int $line, int $position)
{
	if (is_array($value))
		$value = $value[1];

	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybný typ tokenu: \"$value\" je \"$type\".\nOčekávaný typ: \"$expectedType\"\n");
	exit(ERROR_OTHER);
}

/// Chyba operačního kódu (načten neočekávaný token).
function ExitOpcodeError($value, int $line, int $position)
{
	if (is_array($value))
		$value = $value[1];

	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybný operační kód: \"$value\".\n");
	exit(ERROR_OPCODE);
}

/// Chyba lexikálního analyzátoru, chyba ve vstupním souboru.
function ExitLexicalError(string $word, int $line, int $position)
{
	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Lexikální chyba: \"$word\".\n");
	exit(ERROR_OTHER);
}

?>