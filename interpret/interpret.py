import xml.etree.ElementTree as XmlParser
from argparse import ArgumentParser
from sys import stderr
from typing import List, Union

from instruction import *
from opcodes import decode_opcode


def parse_arguments():
	parser = ArgumentParser()
	parser.add_argument("--source", help="XML file representing IPPcode21 source code")
	parser.add_argument("--input", help="file with inputs for interpretation of the source code")
	return parser.parse_args()


def load_xml_from_file(file_name:str) -> Union[Element, None]:
	try:
		return XmlParser.parse(file_name).getroot()
	except XmlParser.ParseError as error:
		stderr.write(f"{error}\n")


def load_xml_from_stdin() -> Union[Element, None]:
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


def parse_xml(file_name:str) -> List[Instruction]:
	program = load_xml_from_file(file_name) if file_name is not None else load_xml_from_stdin()
	instructions = []
	
	if program is not None and check_program_language(program):
		for instruction in program:
			try:
				instructions.append(decode_opcode(instruction))
			except Exception as e:
				stderr.write(f"{e}\n")
				return None
	instructions.sort(key=lambda x: x.order)
	return instructions


if __name__ == "__main__":
	args = parse_arguments()
	instructions = parse_xml(args.source)

	if instructions is not None:
	###test loop, remove later, silly ;)
		for i in instructions:
			#print(type(i), i.order, end=" ")
			#for a in i.arguments:
			#	print(a.type, a.value, end=", ")
			i.invoke()
			#print()
