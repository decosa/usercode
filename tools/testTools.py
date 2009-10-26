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
        self._parameters=self.parameters()
        
    def getDefaultParameters(self):
        return self._defaultParameters

    def setParameterNew(self,name,value):
        ConfigToolBase.setParameterNew(self,name, value)
        self.typeErrorNew(value,self._defaultParameters[name].type)
    
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython = "\nchangeSource(process, "
        dumpPython += str(self.getvalueNew('source'))+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,
                 source=None
                    ) :
       
        if  source is None:
            source=self._defaultParameters['source'].value 
        self.setParameterNew('process',process)
        self.setParameterNew('source',source)
        self.apply() 
        
    def apply(self):
                
        process=self._parameters['process']
        source=self._parameters['source']
        process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

    
changeSource=ChangeSource()
