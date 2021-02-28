<?php

ini_set('display_errors', 'stderr');

const ERROR_PARAMETER = 10;
const ERROR_INPUT_FILE = 11;
const ERROR_OUTPUT_FILE = 12;

const ERROR_HEADER = 21;
const ERROR_OPCODE = 22;
const ERROR_OTHER = 23;

const ERROR_INTERNAL = 99;

function ErrorLinePosition(int $line, int $position)
{
	fwrite(STDERR, "Řádek $line, Pozice $position: ");
}

function ExitErrorParameter(string $param)
{
	fwrite(STDERR, "Chybný parametr programu: $param\n");
	exit(ERROR_PARAMETER);
}

function ExitHeaderError(string $input, string $correctLang, int $line, int $position)
{
	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybná hlavička \"$input\".\nNutno specifikovat podporovaný jazyk \".$correctLang\".\n");
	exit(ERROR_HEADER);
}

function ExitArgTypeError(string $inputType, string $inputValue, string $expectedType, int $line, int $position)
{
	$moreInfo = "";
	if ($expectedType == "symb")
		$moreInfo = " (proměnná nebo literál)";

	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybný typ argumentu: \"$inputValue\" je \"$inputType\".\nOčekávaný typ: \"$expectedType\"$moreInfo.\n");
	exit(ERROR_OTHER);
}

function ExitTokenTypeError($value, string $type, string $expectedType, int $line, int $position)
{
	if (is_array($value))
		$value = $value[1];

	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybný typ tokenu: \"$value\" je \"$type\".\nOčekávaný typ: \"$expectedType\"\n");
	exit(ERROR_OTHER);
}

function ExitOpcodeError($value, int $line, int $position)
{
	if (is_array($value))
		$value = $value[1];

	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Chybný operační kód: \"$value\".\n");
	exit(ERROR_OPCODE);
}

function ExitLexicalError(string $word, int $line, int $position)
{
	ErrorLinePosition($line, $position);
	fwrite(STDERR, "Lexikální chyba: \"$word\".\n");
	exit(ERROR_OPCODE);
}

?>