
#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (c) 2014.

"""
.. module:: Symbolicate
    :plarform: Unix, Windows, OSX

.. modelauthor:: Adam Drakeford <adamdrakeford@gmail.com>
"""

import os
import sys
import getopt
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))


def get_args(argv):
    path_to_dsym = None

    try:
        opts, args = getopt.getopt(argv, 'hd:', ['directory=', 'help'])
    except getopt.GetoptError:
        print('Run Symbolicate.py -h --help for more info')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt in ("-d", "--directory"):
            path_to_dsym = arg

    return path_to_dsym


def print_help():
    print('Usage: python Symbolicate.py')
    print('Options:')
    print('\t -h, --help \t\t Show this help message and exit')
    print('\t -d, --directory \t Pass directory to the dSYM file as argument')


def parse_file():

    if not os.path.exists(HERE):
        print('Path doesn\'t exist')
        return

    file_name = os.path.join(HERE, 'put_bugsense_crash_here.txt')
    with open(file_name) as f:
        contents = f.readlines()

    list_of_symbols = []
    for line in contents:
        line = line.split()
        list_of_symbols.append(line[2])

    if len(list_of_symbols) == 0:
        print("No data detected in put_bugsense_crash_here.txt file")
        return

    return list_of_symbols


def symbolicate(list_of_symbols, path_to_dsym):

    req_file = 'Contents/Resources/DWARF'
    default_dir = "put_dSYM_here"

    if path_to_dsym is None:
        f = str(subprocess.check_output(["ls", default_dir])).replace('\n', '')
        if len(f.split()) < 1:
            print("Default directory {} empty".format(default_dir))
            return
        elif len(f.split()) > 1:
            print(
                "To many files in default directory {}"
                .format(default_dir)
            )
            return
        req_file = os.path.join(f, req_file)
        req_file = os.path.join(default_dir, req_file)
    else:
        req_file = os.path.join(path_to_dsym, req_file)

    req_file = os.path.abspath(req_file)
    print req_file

    if not os.path.exists(req_file):
        print('Error opening dSYM file. Check file path')
        return

    report = []
    f = str(subprocess.check_output(["ls", req_file])).replace('\n', '')
    for symbol in list_of_symbols:
        report.append(
            str(subprocess.check_output(["atos", "-arch", "armv7", "-o",
                os.path.join(req_file, f), symbol])).replace('\n', '')
        )
    return report


def display_results(report):
    print("Symbolicated results:")
    for r in report:
        print("\t{}".format(r))


def main(argv):
    path_to_dsym = get_args(argv)
    symbols = parse_file()

    if symbols is not None:
        result = symbolicate(symbols, path_to_dsym)
        if result is not None:
            display_results(result)


if __name__ == '__main__':
    main(sys.argv[1:])
