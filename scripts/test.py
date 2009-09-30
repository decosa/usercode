from read_provenance import *
from diff_provenance import *
import unittest


if __name__=="__main__":
    
    class testEdmProvDiff(unittest.TestCase):

        def setUp(self):
            self._r=filereader()
            self._d=difference(str(2))

        def testStartswith(self):
            """ Check the function startswith() of class filereader
            """
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
            """ Check the modules names stored in the dictionary by the readfile function
                of the filereader class, and thei order.
            """
            print 'start key test'
            moduleblock1={}
            moduleblock2={}
            moduleblock1=self._r.readfile('newfile')
            moduleblock2=self._r.readfile('newfile2')

            #print moduleblock1
            #print moduleblock2
            keys1=moduleblock1.keys()
            keys2=moduleblock2.keys()

            self.assertEqual(keys1,['genCandidatesForMET HLT','genMetCalo HLT','genParticles HLT', 'genParticleForJet HLT'])
            self.assertEqual(keys2,['genCandidatesForMET HLT','genMetCalo HLT','genParticles HLT', 'genParticleForJet HLT'])
            print 'end key test'
        def testValueModule(self):
            """ Check the modules stored in the dictionary by the readfile function
                of the filereader class.
            """
            moduleblock={}
            file='newfile'
            moduleblock=self._r.readfile(file)
            key='genCandidatesForMET HLT'
            try:
                value=moduleblock[key]
            except KeyError:
                print "No module "+key+" in file "+file 
            block=['Module: genCandidatesForMET HLT', ' parameters: {', '  excludeResonances: bool tracked  = false', '  partonicFinalState: bool tracked  = false']  ### eliminare le parentesi!!!!
            self.assertEqual(block,value)

        def testListDifferences(self):
            """ Check the differences between the parameters of a same module
                ran on two different edm files with different parameter values
            """
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
            result=['excludeResonances: bool tracked  = false  [first file]','                                   true  [second file]', 'partonicFinalState: bool tracked  = false  [first file]','                                    true  [second file]']
            self.assertEqual(result, self._d.list_diff(module1,module2,file1,file2))

                    
            
    unittest.main()
