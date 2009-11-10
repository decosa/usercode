from FWCore.GuiBrowsers.ConfigToolBase import *
#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.ParameterSet.Types  import InputTag    

class ChangeSource(ConfigToolBase):

    """ Test Tool
    """
    
    _label='ChangeSource'
    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'source','No default value. Set your own', ' Source')
        self._parameters=copy.deepcopy(self._defaultParameters)
        
    def getDefaultParameters(self):
        return self._defaultParameters
   
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython = "\nchangeSource(process, "
        dumpPython +='"'+ str(self.getvalue('source'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,source=None) :
        if  source is None:
            source=self._defaultParameters['source'].value 
        self.setParameter('source',source)
        self.apply(process) 
        
    def apply(self, process):
                
        source=self._parameters['source'].value
        process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        process.enableRecording()
        action=self.__copy__()
        process.addAction(action)

    
changeSource=ChangeSource()
