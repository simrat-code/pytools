#!/usr/bin/env python

# Filename  : generate_md5.py
# Author    : Simrat Pal Singh
# Date      : 08-May-2018
#
# About     : script is converted into python


# Filename  : generate_md5.sh
# Author    : Simrat Pal Singh
# Date      : 16-Aug-2016
#
# About     : It will generate md5sum of all files stored in current directory and
#             and will save to 'readme.md5' file

# args      : -g -> generate 
#             -c -> check

import optparse
import datetime
import os
import hashlib


filename = "readme.md5"
now = datetime.datetime.today()


def create_checksum(filename):
    checksum = hashlib.md5()
    with open(filename, "r") as fp:
        while True:
            buffer = fp.read(8192)
            if not buffer: break
            checksum.update(buffer)
    checksum = checksum.hexdigest()
    return checksum


def generate_md5():
    global filename
    global now

    os.remove(filename)
    cwd = os.getcwd()
    list_file = os.listdir(cwd)
    with open(filename, "w") as fp:
        fp.write("# created on: {}\n".format(now))
        for f in list_file:
            if not os.path.isfile(f): continue
            # calculat md5sum and write to fp
            checksum = create_checksum(f)
            fp.write("{}\t{}\n".format(checksum, f))


def check_md5():
    global filename


parser = optparse.OptionParser()
parser.add_option('-g', '--generate', dest='generate',
        default=False,
        action='store_true',
        help="generate md5sum file with name \'readme.md5\' in current folder. It contains all filenames along with their md5sum",
        metavar='GENERATE')
parser.add_option('-c', '--check', dest='check',
        default=False,
        action= 'store_true',
        help="check the md5sum of each file against the stored in readme.md5 file",
        metavar='CHECK')

(options, args) =  parser.parse_args()

    
if options.generate:
    generate_md5()
elif options.check:
    check_md5()
else:
    print "wrong option"
    parser.print_help()


