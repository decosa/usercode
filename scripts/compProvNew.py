#!/usr/bin/env python

# A script to compare the provenance of two input root files.
# It prints out informations about those modules which are common to the input files,
# but whose parameters are setted to different values, and about those modules
# present only in one of the two files.
# According to the level of verbosity, it will be report the name of these modules
# and details about the parameters and their values.
#
# author:  Annapaola de Cosa

from optparse import OptionParser
import sys
from subprocess import Popen, PIPE, STDOUT
from readProv import *
from diffProv import *


usage = "usage: %prog  filename1 filename2"
parser = OptionParser(usage=usage, version="%prog 0.1")
parser.add_option("-v", "--verbosity_level", dest="verbose", help="[0] to print short message [1], to print details about the differences of modules common to both files, [2] to print all the details about the differences between the two files")
(options, args) = parser.parse_args()

if len(args) != 2:
    print 'Incorrect usage'

def provenance(args):
    cmd="edmProvDump "+args    
    if sys.platform == "linux2":
        close_fds = True
    else:
        close_fds = False  
    pipe = Popen(cmd, bufsize=1,stdin=PIPE, stdout=PIPE, stderr=PIPE, shell = True, close_fds=close_fds)
    provenance, provenanceerr=pipe.communicate()
    s=args[:args.index('.')]
    file=open(s,'w')    
    file.write(provenance)

    return s
try:
    prov1=provenance(args[0])
    prov2=provenance(args[1])
except IndexError:
    print "Specify input file names\nType './compProvNew.py -h' to visualize the arguments needed"     
f=filereader()
module1=f.readfile(prov1)
module2=f.readfile(prov2)
d=difference(options.verbose)
d.module_diff(module1,module2,args[0],args[1])

                                                            
