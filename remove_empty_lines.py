#!/usr/bin/env python

import os
import sys


def remove_empty_lines(f):
    if not os.path.isfile(f):
        print "does not exist %s" % f
        return
    fh_in = open(f, "r")
    fh_out = open("without_empty.txt", 'w')

    for line in fh_in.readlines():
        if line.rstrip() == "":
            continue
        print "LINE: %s" % line,
        fh_out.writelines(line)

    fh_in.close()
    fh_out.close()


if __name__ == "__main__":
    remove_empty_lines("with_empty.txt")

