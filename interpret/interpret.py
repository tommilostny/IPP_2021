import xml.etree.ElementTree as ETree
from argparse import ArgumentParser
from sys import exit, stderr, stdin

import instructions.flow_control as flow_control
import instructions.io as io
from instructions.debug import log_program_progress
from opcodes_mapper import decode_opcode


def parse_arguments():
	parser = ArgumentParser()
	parser.add_argument("--source", help="XML file representing IPPcode21 source code")
	parser.add_argument("--input", help="file with inputs for interpretation of the source code")
	return parser.parse_args()


def load_xml_tree(file_name:str):
	try:
		return ETree.parse(file_name).getroot()
	except ETree.ParseError as error:
		stderr.write(f"XML parser error: {error}\n")
		exit(31)


def check_program_element(program:ETree.Element):
	if program.tag != "program":
		stderr.write(f"Bad tag: \"{program.tag}\"\nExpected \"program\".\n")
		exit(32)
	
	correct_attribs = False
	for count, att in enumerate(program.attrib.keys()):
		if att == "language" and program.attrib[att] == "IPPcode21":
			correct_attribs = True

		elif att not in [ "name", "description" ]:
			correct_attribs = False
			break
	
	if not correct_attribs or count < 0 or count > 2:
		stderr.write(f"Bad program tag {program}: {program.attrib}\n")
		exit(32)


def parse_xml(file_name:str):
	program = load_xml_tree(file_name) if file_name is not None else load_xml_tree(stdin) #Načtení XML stromu ze souboru/stdin
	
	check_program_element(program) #Hlavní tag <program /> je validní?

	for instruction in program: #Načtení a dekódování všech instrukcí na třídy
		try:
			flow_control.instructions.append(decode_opcode(instruction))
		except Exception as e:
			stderr.write(f"{e}.\n")
			exit(53)

	flow_control.instructions.sort(key=lambda x: x.order) #Seřazení instrukcí podle pořadí (můžou být spřeházené)
	flow_control.register_all_labels()                    #Registrace všech návěští v seznamu instrukcí


if __name__ == "__main__":
	args = parse_arguments()

	if args.source is None and args.input is None:
		stderr.write("Either --source or --input parameter needs to be specified.\n")
		stderr.write("To display help run the program with --help.\n")
		exit(10)
	
	if args.input is not None: #Zadán argument --input (otevření vstupního souboru pro čtení místo stdin)
		try:
			io.input_file = open(args.input, "r")
		except FileNotFoundError as e:
			stderr.write(f"{e}\n")
			exit(11)

	parse_xml(args.source)

	while flow_control.instruction_counter < len(flow_control.instructions): #Hlavní smyčka programu

		#Instrukce skoku vrací int s pozicí cílové instrukce label.
		#Ostatní instrukce vrací None -> inkrementace pozice následující instrukce.
		next_instr = flow_control.instructions[flow_control.instruction_counter].invoke()

		if next_instr is None:
			flow_control.instruction_counter += 1
		else:
			flow_control.instruction_counter = next_instr

		log_program_progress() #logování ladících informací pro instrukci BREAK

	if args.input is not None:
		io.input_file.close()
