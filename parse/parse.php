<?php

include_once("scanner.php");

$scanner = new Scanner();

for ($i = 0; $i < 30; $i++)
{ 
    echo $scanner->Read();
}
echo "\n"
?>