from ConfigToolBase import *
from testTools import *
from FWCore.ParameterSet.Modules  import Source
import unittest



class testConfigToolBase(unittest.TestCase):

        def setUp(self):
            self._tool=ConfigToolBase()

        def testParameters(self):
            """ Test on methods to manage _parameters
            """
            print "Test on addParameter"
            self._tool.addParameter(self._tool._parameters,'A',1,"a")
            self._tool.addParameter(self._tool._parameters,'B',2,"b")
            self.assertEqual(self._tool._parameters.keys(),['A','B'])
            self.assertEqual(self._tool._parameters['A'].name,'A')
            self.assertEqual(self._tool._parameters['A'].value,1)
            self.assertEqual(self._tool._parameters['A'].description,"a")
            self.assertEqual(self._tool._parameters['A'].type,int)
            self.assertEqual(self._tool._parameters['B'].name,'B')
            self.assertEqual(self._tool._parameters['B'].value,2)
            self.assertEqual(self._tool._parameters['B'].description,"b")
            self.assertEqual(self._tool._parameters['B'].type,int)
            print "Test on setParameter"
            self._tool.setParameter('A',3)
            self.assertEqual(self._tool._parameters['A'].value,3)
            self._tool.setParameter('B',4)
            self.assertEqual(self._tool._parameters['B'].value,4)
            print "Test on getParameters and setParameters"
            aTool=ConfigToolBase()
            aTool.setParameters(self._tool.getParameters())
            self.assertEqual(aTool._parameters.keys(),['A','B'])
            self.assertEqual(aTool._parameters['A'].value,3)
            self.assertEqual(aTool._parameters['B'].value,4)
            print "Test on setting parameters of different tools "
            self._tool.setParameter('A',5)
            self.assertEqual(self._tool._parameters['A'].value,5)
            self._tool.setParameter('B',6)
            self.assertEqual(self._tool._parameters['B'].value,6)
            self.assertEqual(aTool._parameters['A'].value,3)
            self.assertEqual(aTool._parameters['B'].value,4)

        def testTypeError(self):
            """ Test on TypeError method
            """
            print "Test on typeError method "
            self._tool.addParameter(self._tool._parameters,'A',1,"a")
            self._tool.addParameter(self._tool._parameters,'B',"test","b")
            self._tool.addParameter(self._tool._parameters,'C',True,"c")
            self.assertRaises(TypeError, self._tool.setParameter,'A',"str")
            self.assertRaises(TypeError, self._tool.setParameter,'B',True)
            self.assertRaises(TypeError, self._tool.setParameter,'C',3)
           
        def testCopy(self):
            """ Test on __copy__
            """
            print "Test on __copy__ method "
            self._tool.addParameter(self._tool._parameters,'A',1,"a")
            self._tool.addParameter(self._tool._parameters,'B',True,"b")
            aTool=self._tool.__copy__()
            self._tool.setParameter('A',5)
            self._tool.setParameter('B',False)
            self.assertEqual(self._tool._parameters['A'].value,5)
            self.assertEqual(self._tool._parameters['B'].value,False)
            self.assertEqual(aTool._parameters['A'].value,1)
            self.assertEqual(aTool._parameters['B'].value,True)

        def testSetComment(self):
            """ Test on setComment
            """
            print "Test on setComment method "
            self.assertEqual(self._tool.setComment("Write a comment"),"#Write a comment\n")

        def testReset(self):
            """ Test on reset
            """
            print "Test on reset method "

            process=cms.Process("TEST")
	    process.source=Source("PoolSource",fileNames = cms.untracked.string("file:file.root"))
	    changeSource(process,"file:filename.root")
	    self.assertEqual(changeSource._defaultParameters['source'].value,"No default value. Set your own")
            self.assertEqual(changeSource._parameters['source'].value,"file:filename.root")
            changeSource.setParameter('source',"filename2.txt")
            self.assertEqual(changeSource._parameters['source'].value,"filename2.txt")
	    self.assertEqual(changeSource._defaultParameters['source'].value,"No default value. Set your own")
	    changeSource.reset()
	    self.assertEqual(changeSource._parameters['source'].value,"No default value. Set your own")
	    
if __name__=="__main__":
    unittest.main()
