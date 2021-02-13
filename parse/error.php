<?php

//Podporovaný jazyk IPP
const SUPPORTED_LANG = "IPPcode21";

//Chybové kódy
const ERROR_MISSING_PARAMETER = 10;
const ERROR_INPUT_FILE = 11;
const ERROR_OUTPUT_FILE = 12;

const ERROR_HEADER = 21;
const ERROR_OPCODE = 22;
const ERROR_OTHER = 23;

const ERROR_INTERNAL = 99;

//Vytisknout chybu hlavičky na standardní chybový výstup a ukončit program.
function ExitHeaderError()
{
    fwrite(STDERR, "Chybná hlavička. Nutno specifikovat podporovaný jazyk \"". SUPPORTED_LANG . "\".\n");
    exit(ERROR_HEADER);
}

?>