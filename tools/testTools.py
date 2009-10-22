import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.ParameterSet.Types  import InputTag    
from FWCore.ParameterSet.Config  import Process  

class ChangeSource(ConfigToolBase):

    """
    """
    
    _label='ChangeSource'

    _defaultParameters={'process':'No default value. Set your own', 'source':'No default value. Set your own'}

    def getDefaultParameters(self):
        return self._defaultParameters
    
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython = "\nchangeSource(process, "
        dumpPython += str(self.getvalue('source'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,
                 source=_defaultParameters['source']
                    ) :
       

        self.addParameter('process',process, 'The process')
        self.addParameter('source',source, ' Source')
        print type(source)
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(source,str):
            raise TypeError(self.typeError(source,'string'))
        self.apply() 
        
    def apply(self):
                
        process=self._parameters['process'].value
        source=self._parameters['source'].value
        process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

    
changeSource=ChangeSource()
