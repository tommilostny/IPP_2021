<?php

ini_set('display_errors', 'stderr');
include_once("scanner.php");

//Chybové kódy
const ERROR_PARAMETER = 10;
const ERROR_INPUT_FILE = 11;
const ERROR_OUTPUT_FILE = 12;

const ERROR_HEADER = 21;
const ERROR_OPCODE = 22;
const ERROR_OTHER = 23;

const ERROR_INTERNAL = 99;

function ExitErrorParameter(string $param)
{
	fwrite(STDERR, "Chybný parametr programu: $param\n");
	exit(ERROR_PARAMETER);
}

function ErrorLinePosition(Token $token)
{
	fwrite(STDERR, "Řádek $token->Line, Pozice $token->Position: ");
}

function ExitHeaderError(string $input, string $correctLang)
{
	fwrite(STDERR, "Chybná hlavička \"$input\".\nNutno specifikovat podporovaný jazyk \".$correctLang\".\n");
	exit(ERROR_HEADER);
}

function ExitOpcodeError(Token $token)
{
	ErrorLinePosition($token);
	fwrite(STDERR, "Chybný operační kód: \"".(is_array($token->Attribute) ? $token->Attribute[1] : $token->Attribute)."\".\n");
	exit(ERROR_OPCODE);
}

function ExitOtherError($input)
{
	fwrite(STDERR, "Chybná syntaxe: \"". $input . "\".\n");
	exit(ERROR_OTHER);
}

?>