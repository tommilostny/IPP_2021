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


def check_program_language(program:ETree.Element) -> bool:
	if program is not None:
		expected_tag = "program"
		expected_attrib = {"language": "IPPcode21"}
		if program.tag != expected_tag:
			stderr.write(f"Bad tag: \"{program.tag}\"\nExpected \"{expected_tag}\".\n")
			return False
		elif program.attrib != expected_attrib:
			stderr.write(f"Bad program tag attribute(s): {program.attrib}\nExpected {expected_attrib}.\n")
			return False
		return True
	return False


def parse_xml(file_name:str):
	program = load_xml_tree(file_name) if file_name is not None else load_xml_tree(stdin)
	
	if check_program_language(program):
		for instruction in program:
			try:
				flow_control.instructions.append(decode_opcode(instruction))
			except Exception as e:
				opcode = instruction.attrib["opcode"].upper()
				order = instruction.attrib["order"]
				stderr.write(f"{opcode}: (order: {order}) {e}.\n")
				exit(53)
	else: exit(32)

	flow_control.instructions.sort(key=lambda x: x.order)


if __name__ == "__main__":
	args = parse_arguments()

	if args.source is None and args.input is None:
		stderr.write("Either --source or --input parameter needs to be specified.\n")
		stderr.write("To display help run the program with --help.\n")
		exit(10)
	
	if args.input is not None:
		try:
			io.input_file = open(args.input, "r")
		except FileNotFoundError as e:
			stderr.write(f"{e}\n")
			exit(11)

	parse_xml(args.source)

	while flow_control.instruction_counter < len(flow_control.instructions):

		#Instrukce skoku vrací int s pozicí cílové instrukce label.
		#Ostatní instrukce vrací None -> inkrementace pozice následující instrukce.
		next_instr = flow_control.instructions[flow_control.instruction_counter].invoke()

		if next_instr is None:
			flow_control.instruction_counter += 1
		else:
			flow_control.instruction_counter = next_instr

		log_program_progress()

	if args.input is not None:
		io.input_file.close()
