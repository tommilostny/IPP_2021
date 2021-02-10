<?php

class Scanner
{
    private $File = STDIN;

    public function Read()
    {
        return fgetc($this->File);
    }
}

?>