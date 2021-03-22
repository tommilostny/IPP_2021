import xml.etree.ElementTree as XmlParser
from argparse import ArgumentParser
from sys import stderr


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

def check_program_language(program:XmlParser.Element):
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
		print(f"{program.tag} has attribute(s) {program.attrib}") ##TODO: loop loading instructions, return them
		for instruction in program:
			print(f"{instruction.tag} has attribute(s) {instruction.attrib}")
			for argument in instruction:
				print(f"\t{argument.tag} has attribute(s) {argument.attrib} and value:\t{argument.text}")


args = parse_arguments()
instructions = parse_xml(args.source)
