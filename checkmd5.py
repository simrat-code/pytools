#!/usr/bin/env python3
"""
Use to purge the archives (.tar.gz) which have same md5sum
Note: while creating archive pass '-n' to gzip so it exclude timestamp from archive
which will result in different md5 hash even for same file(s).

GZIP=-n tar -cvz /pathA/myfolder -f /pathB/myarchive.tar.gz 

checkmd5.py 
    no argument to ask for purging.

checkmd5.py fileA [fileB ...]
    list of files to get the md5sum.
"""

import hashlib
import sys
import os

main_path = "."

def md5(fname):
    hashsum = hashlib.md5()
    with open(fname, 'rb') as fp:
        # b'' is sentinal value for iter(), 
        # which represents end of sequence
        for chunk in iter(lambda: fp.read(4096), b""):  
            hashsum.update(chunk)
    return hashsum.hexdigest()


def purgeFiles():
    oldsum = "none"
    oldfname = None
    files = os.listdir(main_path)
    files.sort()
    for fname in files:
        if not fname.endswith(".tar.gz"): continue
        newsum = md5(fname)
        if newsum == oldsum:
            if os.path.exists(oldfname): os.remove(oldfname)
        else: 
            oldsum = newsum
        oldfname = fname

def main(argv):
    if not isinstance(argv, list):
        raise ValueError("argument must be list")

    if len(argv) == 1 :
        choice = input("purging current folder <y/n>: ")
        if choice in ("y", "Y"):
            purgeFiles()

    elif argv[1] in ("-h", "--help"):
        print("Usage:")
        print(__doc__)

    else:
        for f in argv[1:]: print(f"{md5(f)}  {f}")
    

if __name__ == '__main__':
    main(sys.argv)
    print(" ---- done ---- ")

