#!/usr/bin/python
import os
import re
import sys
from optparse import OptionParser

#skip_regexs = ["^\,$", "^\{$", "^\}$", "^\"type", "^\"feature", "^.*$"]
skip_regexs = ["^\,$", "^\s*$", "^\{$", "^\}$", "^\[$", "^\]$", "^\"type", "^\"feature"]

def parseargs():
    """ Parse command line arguments """

    parser = OptionParser()

    parser.add_option('-i', '--in', dest="in_file", type="string", default=None,
                      help="name of input file to process")

    parser.add_option('-o', '--out', dest="out_file", type="string", default=None,
                      help="name of output file to write")

    opt, arg = parser.parse_args()

    if not (opt.in_file or opt.out_file):
        print "Error: must specify an --in and an --out file"
        sys.exit(1)

    return opt, arg


if __name__=="__main__":
    options, args = parseargs()

    infh = open(options.in_file, 'r')
    outfh = open(options.out_file, 'w')

    myre = re.compile("|".join(skip_regexs))

    for line in infh.readlines():
        if not re.match(myre, line):
            templine = line.rstrip()
            outfh.write(templine+'\n')
