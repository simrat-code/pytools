#!/usr/bin/env python

# Filename  : generate_md5.py
# Author    : Simrat Pal Singh
# Date      : 06-Jan-2019
# About     : optarg is replaced with argparse
#             also 'if __main__' has been added
#             and python3


# Filename  : generate_md5.py
# Author    : Simrat Pal Singh
# Date      : 08-May-2018
# About     : script is converted into python
#             to user: create a bash file in ~/bin with 
#             echo -e '#!/bin/bash \npython ${HOME}/bin/pytools/generate_md5.py' >${HOME}/bin/generate_md5.sh 
#             chmod u+x ${HOME}/bin/generate_md5.sh


# Filename  : generate_md5.sh
# Author    : Simrat Pal Singh
# Date      : 16-Aug-2016
# About     : It will generate md5sum of all files stored in current directory and
#             and will save to 'readme.md5' file

# args      : -g -> generate 
#             -c -> check

import argparse
import datetime
import os
import hashlib


filename = "securehash.md5"
now = datetime.datetime.today()


def create_checksum(filename):
    if not os.path.isfile(filename):
        return "F12E407E6157"
    checksum = hashlib.md5()
    with open(filename, "r") as fp:
        while True:
            buffer = fp.read(8192)
            if not buffer: break
            checksum.update(buffer.encode('utf-8'))
    checksum = checksum.hexdigest()
    return checksum


def generate_md5():
    global filename
    global now

    if os.path.isfile(filename): 
        # remove the old secure-hash file
        # before generating new file
        # and by removing it, we exclude it from file-list
        print('[=] removing old file: {}'.format(filename))
        os.remove(filename)
    cwd = os.getcwd()
    list_file = os.listdir(cwd)
    with open(filename, "w") as fp:
        fp.write("# created on: {}\n".format(now))
        for f in list_file:
            if not os.path.isfile(f): continue
            # calculate md5sum and write to fp
            checksum = create_checksum(f)
            fp.write("{}\t{}\n".format(checksum, f))
    print("[=] md5 list stored: %s" % filename)


def check_md5():
    global filename

    print("[=] checking md5 from %s" % filename)
    # cwd = os.getcwd()
    # list_file = os.listdir(cwd)
    with open(filename, "r") as fp:
        for line in fp.readlines():
            if line[0] == '#': continue
            old_md5, fname = line.split()
            #print "md5: {}\tfname: {}".format(md5, fname)
            new_md5 = create_checksum(fname)
            if old_md5 != new_md5:
                print("[-] md5 not match for {}".format(fname) )
    print("[=] checking md5 complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--generate', 
                        action='store_true',
                        help='generate md5sum file with name \'readme.md5\' in current folder. It contains all filenames along with their md5sum')
    parser.add_argument('-c', '--check',
                        action='store_true',
                        help='check the md5sum of each file against the stored in readme.md5 file')   

    args = parser.parse_args()                     
    if (args.generate):
        generate_md5()
    elif (args.check):
        check_md5()
    else:
        print("wrong option")
        parser.print_help()

# --end--