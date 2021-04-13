parse-interpret:
	php parse/parse.php < samples/test.ipp21 > samples/test.xml
	python3 interpret/interpret.py --source samples/test.xml --input samples/inputs.txt

zip2:
	cd interpret                                                                   &&\
	zip ../xmilos02.zip * instructions/* -x __pycache__/ instructions/__pycache__/ &&\
	cd ../test                                                                     &&\
	zip ../xmilos02.zip *

interpret-help:
	python3 interpret/interpret.py --help
