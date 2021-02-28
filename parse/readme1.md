## Implementační dokumentace k 1. úloze do IPP 2020/2021
Jméno a příjmení: Tomáš Milostný

Login: xmilos02

---
### [parse.php](parse.php)
Hlavní program parser jazyka IPPcode21.

Zpracovává parametr ``--help``:
- Vypíše nápovědu k programu na standardní výstup a skončí.

Jestliže nebyl zadán žádný parametr, program pokračuje načítáním vstupního programu následujícím způsobem:

1. V hlavní smyčce se předá řízení lexikálnímu analyzátoru ``Scanner``, který prvně zkontroluje hlavičku programu specifikující jazyk programu ve formátu *"``.IFJcode21``"*. Jestliže na vstupu hlavička není, nebo je ve špatném formátu, program zde skončí s chybou.

2. Následně se načítají instrukce programu do pole objektů typu ``Instruction``, které si dále načítají a kontrolují syntaxi svých argumentů.

3. Pokud byly všechny instrukce programu správně načteny, je XML reprezentace struktury programu vypsána na standardní výstup s využitím knihovny ``XMLWriter`` a metodami ``Print`` tříd ``Instruction`` a ``Argument``.
---
### [scanner.php](scanner.php)
Lexikální analyzátor IPPcode21 obsahuje následující třídy:
- **``TokenType``** - Obsahuje konstanty typů tokenů
- **``Token``** - Datová struktura tokenu (typ, atribut)
- **``Scanner``** - Hlavní třída lexikálního analyzátoru.
    - Pracuje se souborem na vstupu (v případě tohoto projektu se standardním vstupem).
    - Parametrem kontruktoru je jazyk programu načítaný v hlavičce.
    - Obsahuje metodu **``GetNextToken``**, která čte vstup a dle načteného slova vrátí informace ve formě tokenu. Pracuje také s ``IsOpcode`` třídy ``Instruction`` a ``ResolveArgumentType`` třídy ``Argument`` během rozpoznávání, zda se jedná o operační kód instrukce nebo argument.
    - Pokud není rozpoznán typ tokenu, program končí s lexikální chybou.
    - Rovněž obsahuje pomocné privátní metody ``LoadWord`` (načte slovo ze vstupu, ignoruje mezery a komentáře), ``EofCheckSet`` (zkontroluje konec souboru, případně nastaví typ tokenu) a ``ReadChar`` (načte znak ze souboru, posouvá pozici v souboru).
---
### [instruction.php](instruction.php)
Třída **``Instruction``** uchovává informace o instrukci - její pořadí, operační kód a pole argumentů. Parametry konstruktoru této třídy jsou:
- ``Token $token`` - vstupní token, musí být typu *OPCODE*
- ``int $order`` - pořadí instrukce
- ``Scanner $scanner`` - lexikální analyzátor, načítá argumenty instrukce

Třída rovněž obsahuje konstantní asociativní pole **``OPCODES``**, které je použito jako slovník definující syntaxi jednotlivých operačních kódů instrukcí jazyka IPPcode21. Je také použito metodou ``IsOpcode``, která zjistí, zda zadaný řetězec v parametru odpovídá klíči v tomto poli.

Klíčem je operační kód instrukce a hodnotou je pole terminálních symbolů:
- *var* - proměnná
- *symb* - proměnná, literál (int, string, bool, nil)
- *label* - návěští
- *\n* - konec řádku
- *type* - datový typ (int, string, bool)

Pokud je vstupní token v pořádku, jsou načteny argumenty privátní metodou ``LoadArguments``, která podle aktuálního operačního kódu vybere položku slovníku ``OPCODES`` a v cyklu zkonroluje, zda posloupnost tokenů na vstupu odpovídá očekávaným terminálním symbolům, reprezentující argumenty instrukce. Vytvořený objekt typu ``Argument`` je uložen do pole argumentů.

---
### [argument.php](argument.php)
Třída **``Argument``** uchovává informace o argumentu instrukce - typ, pořadí a hodnota (jméno proměnné, hodnota literálu, ...). Parametry konstruktoru této třídy jsou:
- ``Token $token`` - vstupní token, musí být typu *ARGUMENT*
- ``int $order`` - pořadí argumentu
- ``string $syntaxSymbol`` - očekávaný terminální symbol syntaxe (viz. [*instruction.php*](readme1.md#instructionphp) - pole ``OPCODES``), porovná se s typem aktuálního argumentu z načteného tokenu

Třída rovněž obsahuje asociativní pole **``ARGTYPES``**. Klíčem pole je regulární výraz k danému typu. Je použito metodou ``ResolveArgumentType``, která zkontroluje zda řetězec v parametru odpovídá některému z regulárních výrazů v poli a vrátí příslušný typ nebo *NULL*.

---
### [error.php](error.php)
Obsahuje konstanty chybových kódů a specifické funkce ukončující program s chybou.

---