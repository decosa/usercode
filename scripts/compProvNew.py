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
    f=filereader()
    module1=f.readfile(prov1)
    module2=f.readfile(prov2)
    #module1=f.readfile('newfile')
    #module2=f.readfile('newfile2')
    #print module1['HLT']
    #print module1['HLT'][0].value
    #print module1['HLT'][1].label
    #print module1['HLT'][1].value
    d=difference(options.verbose)
    d.module_diff(module1,module2,args[0],args[1])
except IndexError:
    print "Specify input file names\nType './compProv.py -h' to visualize the arguments needed"
    



if __name__=="__main__":
    import unittest
    class testEdmProvDiff(unittest.TestCase):
        
        def setUp(self):
            self._r=filereader()
            self._d=difference(2)
            
            def testStartswith(self):
                """ Check the function startswith() of class filereader  """
                r='Module: modulename'
                a=self._r.startswith(r)
                self.assertEqual(a, True)
                s='ESSource: modulename'
                b=self._r.startswith(s)
                self.assertEqual(b, True)
                t='ESModule: modulename'
                c=self._r.startswith(t)
                self.assertEqual(c, False)
                u='SModule: modulename'
                d=self._r.startswith(u)
                self.assertEqual(d, False)
        
            def testKeys(self):
                moduleblock1={}
                moduleblock2={}
                moduleblock1=self._r.readfile('newfile')
                moduleblock2=self._r.readfile('newfile2')
                keys1=moduleblock1.keys()
                keys2=moduleblock2.keys()
                
                self.assertEqual(keys1,['genCandidatesForMET HLT','genMetCalo HLT','genParticles HLT', 'genParticleForJet HLT'])
                self.assertEqual(keys2,['genCandidatesForMET HLT','genMetCalo HLT','genParticles HLT', 'genParticleForJet HLT'])
        
            def testValueModule(self):
                moduleblock={}
                file='newfile'
                moduleblock=self._r.readfile(file)
                key='genCandidatesForMET HLT'
                try:
                    value=moduleblock[key]
                except KeyError:
                    print "No module "+key+" in file "+file 
                block=['Module: genCandidatesForMET HLT', ' parameters: {', '  excludeResonances: bool tracked  = false', '  partonicFinalState: bool tracked  = false', '  src: InputTag tracked  = genParticles', '', '}{', '}{', '}', '']
                self.assertEqual(block,value)
                
            def testListDifferences(self):
                moduleblock1={}
                moduleblock2={}
                moduleblock1=self._r.readfile('newfile')
                moduleblock2=self._r.readfile('newfile2')
                key='genCandidatesForMET HLT'
                module1=moduleblock1[key]
                module2=moduleblock2[key]
                print module1
                print module2
                file1= 'first file'
                file2= 'second file'
                result=['excludeResonances: bool tracked  = false  [first file]','                                   true  [second file]', 'partonicFinalState: bool tracked  = false  [first file]','                                   true  [second file]']
                self.assertEqual(result, self._d.list_diff(module1,module2,file1,file2))
        

    #unittest.main()

                                                            
