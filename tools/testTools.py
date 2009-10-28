import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.ParameterSet.Types  import InputTag    
from FWCore.ParameterSet.Config  import Process  

class ChangeSource(ConfigToolBase):

    """
    """
    
    _label='ChangeSource'
    
    _defaultParameters={}
    
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameterNew(self._defaultParameters,'process','No default value. Set your own', 'The process',cms.Process)
        self.addParameterNew(self._defaultParameters,'source','No default value. Set your own', ' Source')
        self._parameters=copy.deepcopy(self._defaultParameters)
        #self._parameters=self.parameters()
        
    def getDefaultParameters(self):
        return self._defaultParameters

    #def setParameter(self,name,value):
        #ConfigToolBase.setParameter(self,name, value)
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython = "\nchangeSource(process, "
        dumpPython += str(self.getvalue('source'))+')'+'\n'

        return (dumpPythonImport,dumpPython)

    def __call__(self,process,
                 source=None
                    ) :
       
        if  source is None:
            source=self._defaultParameters['source'].value 
        self.setParameter('process',process)
        self.setParameter('source',source)
        self.apply() 
        
    def apply(self):
                
        process=self._parameters['process'].value
        source=self._parameters['source'].value
        process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        process.enableRecording()
        action=self.__copy__()
        process.addAction(action)

    
changeSource=ChangeSource()
