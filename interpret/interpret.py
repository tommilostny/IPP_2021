import xml.etree.ElementTree as XmlParser
from argparse import ArgumentParser
from sys import exit, stderr

import instructions.flow_control as flow_control
from instructions.debug import log_program_progress
from opcodes_mapper import decode_opcode


def parse_arguments():
	parser = ArgumentParser()
	parser.add_argument("--source", help="XML file representing IPPcode21 source code")
	parser.add_argument("--input", help="file with inputs for interpretation of the source code")
	return parser.parse_args()


def load_xml_from_file(file_name:str):
	try:
		return XmlParser.parse(file_name).getroot()
	except XmlParser.ParseError as error:
		stderr.write(f"{error}\n")


def load_xml_from_stdin():
	return XmlParser.fromstring(input()) ##TODO: read the whole stdin


def check_program_language(program:XmlParser.Element) -> bool:
	expected_tag = "program"
	expected_attrib = {"language": "IPPcode21"}
	if program.tag != expected_tag:
		stderr.write(f"Bad tag: \"{program.tag}\"\nExpected \"{expected_tag}\".\n")
		return False
	elif program.attrib != expected_attrib:
		stderr.write(f"Bad program tag attribute(s): {program.attrib}\nExpected {expected_attrib}.\n")
		return False
	return True


def parse_xml(file_name:str):
	program = load_xml_from_file(file_name) if file_name is not None else load_xml_from_stdin()
	
	if program is not None and check_program_language(program):
		for instruction in program:
			try:
				flow_control.instructions.append(decode_opcode(instruction))
			except Exception as e:
				opcode = instruction.attrib["opcode"].upper()
				order = instruction.attrib["order"]
				stderr.write(f"{opcode}: (order: {order}) {e}.\n")
				exit(53)

	flow_control.instructions.sort(key=lambda x: x.order)


if __name__ == "__main__":
	args = parse_arguments()
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
