#!/usr/bin/env python3
# or you can use 'sed' command 
# sed '/^$/d' infile.txt > outfile.txt

import os
import sys
import optparse


class FileWithEmptyLines:
    def __init__(self):
        self.verbose = False
        self.infile = "with_empty.txt"
        self.outfile = "out_noempty.txt"


    def set_source_file(self, fname):
        self.infile = fname


    def set_dest_file(self, fname):
        self.outfile = fname


    def set_verbose(self, option=True):
        self.verbose = option


    def print_filename(self):
        print("in file : %s" % self.infile)
        print("out file: %s" % self.outfile)


    def remove_empty_lines(self):
        if not os.path.isfile(self.infile):
            print("File not exist: %s" % self.infile)
            return
        fh_in = open(self.infile, "r")
        fh_out = open(self.outfile, 'w')
    
        for line in fh_in.readlines():
            if line.rstrip() == "":
                continue
            if self.verbose:
                print("LINE: %s" % line, end=' ')
            fh_out.writelines(line)
    
        fh_in.close()
        fh_out.close()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-v', '--versose', dest="verbose", 
            default=False,
            action="store_true",
            help="echo each printable line",
            metavar="VERBOSE")
    parser.add_option('-s', '--source', dest="source",
            help="source file to read from",
            metavar="SOURCE")
    parser.add_option('-o', '--outfile', dest="outfile",
            help="filtered data written to outfile",
            metavar="OUTFILE")
    (options, args) = parser.parse_args()

    fm = FileWithEmptyLines()
    if options.source:
        fm.set_source_file(options.source)
    if options.outfile :
        fm.set_dest_file(options.outfile)
    if options.verbose:
        fm.set_verbose()

    fm.print_filename()
    fm.remove_empty_lines()

# -- end --

