#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.GuiBrowsers.ConfigToolBase import *
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
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
   
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
            #dumpPython = self._comment
        dumpPython += "\nchangeSource(process, "
        dumpPython +='"'+ str(self.getvalue('source'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,source=None) :
        if  source is None:
            source=self._defaultParameters['source'].value 
        self.setParameter('source',source)
        self.apply(process) 
        
    def apply(self, process):
                
        source=self._parameters['source'].value
        if hasattr(process, "addAction"):
            process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

    
changeSource=ChangeSource()
