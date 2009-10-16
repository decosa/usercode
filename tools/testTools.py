import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.ParameterSet.Types  import InputTag    
from FWCore.ParameterSet.Config  import Process  

class ChangeSource(ConfigToolBase):

    _label='ChangeSource'

    """
    """      
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython = "\nchangeSource(process, "
        dumpPython += str(self.getvalue('source'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,
                 source
                    ) :
       

        self.addParameter('process',process, 'The process')
        self.addParameter('source',source, ' Source')
        print type(source)
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(source,str),self.typeError(source,'string')
        self.doCall() 
        
    def doCall(self):
                
        process=self._parameters['process'].value
        source=self._parameters['source'].value
        process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

    
changeSource=ChangeSource()
