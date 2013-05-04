import os, subprocess, re, sys, getopt

HERE = os.path.dirname(os.path.abspath(__file__))

def get_args(argv):
	path_to_dsym = None

	try:
		opts, args = getopt.getopt(argv,"hd:",["directory=", "help"])
	except getopt.GetoptError:
		print 'Run Symbolicate.py -h --help for more info'
		sys.exit(2)
   
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print 'Usage: python Symbolicate.py'
			print 'Options:'
			print '     -h, --help \t\t Show this help message and exit'
			print '     -d, --directory \t\t Manually set a directory to point to the dSYM file'
			sys.exit()
		elif opt in ("-d", "--directory"):
			path_to_dsym = arg

	return path_to_dsym


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
	default_dir = "put_dSYM_here"

	if path_to_dsym is None:
		f = str(subprocess.check_output(["ls", default_dir])).replace('\n', '')
		if len(f.split()) < 1:
			print "Default directory \"" + default_dir + "\" empty"
			return
		elif len(f.split()) > 1:
			print "To many files in default directory \"" + default_dir + "\""
			return
		req_file = os.path.join(f, req_file)
		req_file = os.path.join(default_dir, req_file)
	else:
		req_file = os.path.join(path_to_dsym, req_file)

	req_file = os.path.abspath(req_file)
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

def __main__(argv):
	path_to_dsym = get_args(argv)
	symbols = parse_file()

	if len(symbols) != 0:
		result = symbolicate(list_of_symbols = symbols, path_to_dsym = path_to_dsym)
		if result != None:
			display_results(result)
	else:
		print "No data detected in bugsense.txt file"


if __name__ == '__main__':
	__main__(sys.argv[1:])

