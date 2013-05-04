import os
import subprocess
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def get_args():
	if len(sys.argv) == 1:
		print "You need to specify path to dSYM file"
		print "Usage: Symbolicate.py FILE_DIR"
		return
	else:
		path = str(sys.argv[1])
		return path

def parse_file():
    if os.path.exists(HERE):
    	file_name = os.path.join(HERE, 'bugsense.txt')
    	with open(file_name) as f:
    		contents = f.readlines()
    else:
    	print 'Path doesn\'t exist'
    	return

    list_of_symbols = []
    for line in contents:
    	line = line.split()
    	list_of_symbols.append(line[2])

    return list_of_symbols

def symbolicate(list_of_symbols, path_to_dsym):
	req_file = 'Contents/Resources/DWARF'
	req_file = os.path.join(path_to_dsym, req_file)
	print req_file

	report = []
	if os.path.exists(req_file):
		f = str(subprocess.check_output(["ls", req_file])).replace('\n', '')
		for symbol in list_of_symbols:
			report.append(str(subprocess.check_output(["atos", "-arch", "armv7", "-o", os.path.join(req_file, f), symbol])).replace('\n', ''))
		return report
	else:
		print 'Error opening dSYM file. Check file path'
		return

def display_results(report):
	print "Symbolicated results:"
	for r in report:
		print "\t" + r

def __main__():
	path_to_dsym = get_args()
	symbols = parse_file()

	if path_to_dsym != None and symbols != None:
		result = symbolicate(list_of_symbols = symbols, path_to_dsym = path_to_dsym)
		if result != None:
			display_results(result)


if __name__ == '__main__':
	__main__()

