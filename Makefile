test-interpret:
	php parse/parse.php < samples/test.ipp21 > samples/test.xml
	python3 interpret/interpret.py --source samples/test.xml --input samples/inputs.txt
