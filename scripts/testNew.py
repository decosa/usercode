from readProv import *
from diffProv import *
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


        ### Modificare questo test! Non serve l'ordine ma solo il contenuto    
        def testKeys(self):
            """ Check the modules names stored in the dictionary by the readfile function
                of the filereader class, and thei order.
            """
            print 'start key test'
            moduleblock1={}
            moduleblock2={}
            moduleblock1=self._r.readfile('newfile')
            moduleblock2=self._r.readfile('newfile2')
            keys1=moduleblock1.keys()
            keys2=moduleblock2.keys()

            self.assertEqual(keys1,['HLT'])
            self.assertEqual(keys2,['HLT'])
            print 'end key test'

        def testValueModule(self):
            """ Check the modules stored in the dictionary by the readfile function
                of the filereader class.
            """
            print 'start testValueModule'
            moduleblock={}
            file='newfile'
            moduleblock=self._r.readfile(file)
            key='HLT'
            try:
                moduleblock[key]
            except KeyError:
                print "No process "+key + "run "   
            try:
                label=moduleblock[key][0][0]
            except ValueError:
                print "No module "+label +" in the process "+ key + ' in the file '+ file

            value=moduleblock[key][0][1]
            block=('Module: genCandidatesForMET HLT', ' parameters: {', '  excludeResonances: bool tracked  = false', '  partonicFinalState: bool tracked  = false') 
            self.assertEqual(block,value)
            print 'end testValueModule'
            
        def testListDifferences(self):
            """ Check the differences between the parameters of a same module
                ran on two different edm files with different parameter values
            """
            moduleblock1={}
            moduleblock2={}
            moduleblock1=self._r.readfile('newfile')
            moduleblock2=self._r.readfile('newfile2')
            key='HLT'
            module1=moduleblock1[key][0][1]
            module2=moduleblock2[key][0][1]
            print module1
            print module2
            file1= 'first file'
            file2= 'second file'
            result=['excludeResonances: bool tracked  = false  [first file]','                                   true  [second file]', 'partonicFinalState: bool tracked  = false  [first file]','                                    true  [second file]']
            self.assertEqual(result, self._d.list_diff(module1,module2,file1,file2))

                    
            
    unittest.main()
