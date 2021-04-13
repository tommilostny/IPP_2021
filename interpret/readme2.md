## Implementační dokumentace k 2. úloze do IPP 2020/2021
Jméno a příjmení: Tomáš Milostný

Login: xmilos02

---
## [interpret.py](interpret/interpret.py)
Hlavní program interpret XML reprezentace jazyka IPPcode21.

Zpracovává následující parametry příkazové řádky knihovnou **argparse**:
* ``--help`` - vypíše nápovědu k programu na standardní výstup a skončí
* ``--source`` - vstupní soubor XML reprezentace kódu (pokud chybí, XML je načítáno ze standardního vstupu)
* ``--input`` - vstupní soubor pro interpretaci (používaný instrukcí *READ* místo standardního vstupu)

Jestliže je zadán alespoň jeden z parametrů ``--source`` nebo ``--input``
(aby bylo jasné, který ze vstupů používá *stdin*), interpret pokračuje následujícím způsobem:

1. Spustí se parsování XML zdrojového souboru knihovnou **xml.etree.ElementTree**,
    která zkontrolu formát XML a vytvoří stromovou strukturu dále přístupnou v programu.
2. Zkontroluje se kořenový element - jedná se o tag ``<program>``,
    má pouze podporované atributy (*language*, *name*, *description*)
    a specifikuje správný jazyk *``IPPcode21``*.
3. V cyklu načítá potomky kořenového elementu, který je předán funkci **``decode_opcode``** modulu **``opcodes_mapper``**.
    Pokud je element v pořádku je vrácen objekt dědící z bázové třídy instrukčních typů **``InstructionBase``**, který se vloží do seznamu instrukcí programu.
4. Jakmile jsou všechny instrukce vytvořeny, je jejich seznam seřazen dle atributu *``order``* a registrují se všechny návěští (jelikož je možné zpracovat vstup, kde jsou instrukční elementy ve špatném pořadí).
5. Následuje smyčka vykonávání programu, kde jsou postupně ze seznamu instrukcí spouštěny jednotlivé instrukce voláním metody **``invoke``**.

### Instrukce
Jádrem zpracování instrukcí je bázová třída **``InstructionBase``** ze souboru [instruction_base.py](interpret/instructions/instruction_base.py),
která definuje konstruktor a metodu **``invoke``** společné pro všechny implementace instrukcí.

Parametry konstruktoru instrukce jsou element programu a sezname syntaktických symbolů
(používá se pro kontrolu typů argumentů (*var*, *symb*, *label*, *type*) a počet argumentů).
Následuje kontrola atributů **``opcode``** a **``order``** (který je rovněž zkontrolován na duplicitu, aby bylo jasné pořadí sekvence instrukcí).

Instrukce si následné do seznamu objektů typu **``Argument``** načte potomky XML elementu instukce.
Konstruktoru argumentu je krom elementu předán také syntaktický symbol na pozici právě načítaného argumentu.

Konkrétní třídy jsou dále v adresáři **instructions** implementovány v samostatných modulech dle kategorie a způsobu použití instrukce:

* [arithmetic.py](interpret/instructions/arithmetic.py)
    - Aritmetické instrukce **ADD**, **SUB**, **MUL**, **IDIV**.
    - Obsahuje také aritmetickou bázovou třídu, kterou tyto instrukce implementují
        (mají společnou sémantiku s rozdílem provedené operace).
    - Zděděné třídy volají společnou metodu **``invoke``**, které předají parametr operace jako lambda výraz.
* [boolean.py](interpret/instructions/boolean.py)
    - Booleovské instrukce **AND**, **OR**, **NOT**.
    - Podobně jako modul aritmetických instrukcí obsahuje bázovou třídu pro booleovské operace.
        Není využita instrukcí ``Not``, protože zpracovává pouze dva argumenty.
* [convertions.py](interpret/instructions/convertions.py)
    - Konverzní instrukce **INT2CHAR**, **STRI2INT**.
* [debug.py](interpret/instructions/debug.py)
    - Ladící instrukce **DPRINT**, **BREAK**.
    - Modul obsahuje také proměnné, které jsou použity pro sledování běhu programu.
        Počítá provedené instrukce a udržuje si pozici v seznamu instrukcí.
        Program je těmito proměnnými sledován, jen když je nastaven příznak v konstruktoru instrukce ``Break``.
* [flow_control.py](interpret/instructions/flow_control.py)
    - Instrukce řízení toku programu **LABEL**, **JUMP**, **JUMPIFEQ**, **JUMPIFNEQ**, **EXIT**.
    - Obsahuje seznam instrukcí (rovněž používán v interpretu pro navigaci v programu),
        slovník návěští (klíčem je jméno návěští, ukazuje na index v seznamu instrukcí)
        a programový čítač instrukcí (udržuje aktuální pozici v programu/seznamu instrukcí).
    - Třída ``Label`` neimplementuje metodu ``invoke`` jako ostatní instrukce,
        ale metodu **``register``**, která je volaná pro každý ``Label`` před spuštěním hlavní programové smyčky,
        a zaregistruje návěští specifikované v argumentu do slovníku návěští.
    - Metoda **``invoke``** instrukcí skoku, narozdíl od ostatních instrukcí bez návratové hodnotu, vrací hodnotu typu ``int`` jako novou pozici programového čítače, specifikovanou v argumentu návěští.
    Tato hodnota je pak přijata v hlavní smyčce programu interpretu.
    - Instrukce podmíněných skoků mají rovněž společnou bázovou třídu (opět mají stejnou sémantiku pouze s rozdílem typu porovnání).
* [frames.py](interpret/instructions/frames.py)
    - Instrukce pracující s datovými rámci **MOVE**, **CREATEFRAME**, **PUSHFRAME**, **POPFRAME**, **DEFVAR**.
    - Obsahuje slovníky ``global_frame``, ``temporary_frame`` a seznam slovníků ``local_frames`` a funkce **``get``**, **``set``**, které s rámci pracují a jsou využívány i ostatními moduly pro jednodušší práci s proměnnými
    (hlídají stav inicializace, přístup k validnímu rámci, označenému ve jménu proměnné).
    - Funkce ``get`` rovněž umožňuje vrátit hodnotu literálu, pokud typ argumentu není *var*.
    - Funkce ``set`` je rovněž instrukcí ``Defvar`` použita k definici proměnné, jinak je povolen přístup pouze k již inicializovaným proměnným.
* [function.py](interpret/instructions/function.py)
    - Instrukce volání funckí **CALL**, **RETURN**.
    - Obsahuje zásovník volání, do kterého instrukce ``Call`` ukládá inkrementovaný aktuální stav programového čítače (návratovou adresu).
    - ``Return`` opět nastaví programový čítač na hodnotu z vrcholu zásobníku volání
    - Je využito mechanismu návratu hodnoty typu ``int`` podobně jako skokové instrukce.
* [io.py](interpret/instructions/io.py)
    - Vstup/výstupní instrukce **WRITE**, **READ**.
    - Obsahuje vstupní soubor interpretu, který může být ze standardního vstupu přepsán na soubor parametrem příkazové řádky *``--input``*.
* [relational.py](interpret/instructions/relational.py)
    - Relační porovnávací instrukce **LT**, **GT**, **EQ**.
    - Podobně jako modul booleovských instrukcí obsahuje bázovou třídu pro relační porovnávání.
* [stack.py](interpret/instructions/stack.py)
    - Zásobníkové instrukce **PUSHS**, **POPS**.
    - Obsahuje datový zásobník.
* [string.py](interpret/instructions/string.py)
    - Instrukce pracující s řetětězci **CONCAT**, **STRLEN**, **GETCHAR**, **SETCHAR**.
* [type.py](interpret/instructions/type.py)
    - Instrukce pro zjištění typu proměnné nebo literálu **TYPE**.

### [argument.py](interpret/argument.py)
Obsahuje třídu **``Argument``** reprezentující argument instrukce programu.

Konstruktor této třídy kontroluje validitu elementu ``<arg(číslo)>``, atributu *type*
a dle čísla argumentu také zda se jedná o validní typ na základě syntaktického symbolu.

### [opcodes_mapper.py](interpret/opcodes_mapper.py)
Účelem tohoto modulu je mapování řetězce operačního kódu na objekt instrukce implementující **``InstructionBase``**.

Obsahuje slovník **``OPCDODES``**, jehož klíčem je uppercase operační kód ukazující na slovníkovou strukturu s klíči:
- *class* - typ třídy z instrukčních modulů.
- *syntax* - syntaktické symboly (var, symb, label, type), určují typy a počet argumentů, které daná instrukce podporuje.

### [error.py](interpret/error.py)
Modul obsahující funkce pro výpis chyby a ukončení programu s příslušným chybovým kódem.
Pokud je vstupní soubor nastaven parametrem ``--input``, je tento soubor uzavřen.

Funkce ``exit_instruction_error`` je specializovaná na výpis chyb při vykonávání instrukcí
a chybový výstup je obohacen o informace o dané instrukci.

---
## [test.php](test/test.php)
