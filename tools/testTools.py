import copy

from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.ParameterSet.Types  import InputTag    
from FWCore.ParameterSet.Config  import Process  

class ChangeSource(ConfigToolBase):

    """ Test Tool
    """
    
    _label='ChangeSource'
    
    _defaultParameters={}
    
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'process','No default value. Set your own', 'The process',cms.Process)
        self.addParameter(self._defaultParameters,'source','No default value. Set your own', ' Source')
        self.addParameter(self._defaultParameters,'events','No default value. Set your own', ' events',int)
        self.addParameter(self._defaultParameters,'bool','No default value. Set your own', ' bool',bool)
        self._parameters=copy.deepcopy(self._defaultParameters)
        
    def getDefaultParameters(self):
        return self._defaultParameters
   
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.testTools import *\n"
        dumpPython = "\nchangeSource(process, "
        dumpPython += '"'+str(self.getvalue('source'))+'"'+","
        dumpPython += str(self.getvalue('events'))+","
        dumpPython += str(self.getvalue('bool'))+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,source=None,events=None, bool=None) :
        if  source is None:
            source=self._defaultParameters['source'].value 
        self.setParameter('process',process)
        self.setParameter('source',source)
        self.setParameter('events',events)
        self.setParameter('bool',bool)
        self.apply() 
        
    def apply(self):
                
        process=self._parameters['process'].value
        source=self._parameters['source'].value
        events=self._parameters['events'].value
        bool=self._parameters['bool'].value
        process.disableRecording()

        process.source.fileNames=cms.untracked.vstring(source)
        
        process.enableRecording()
        action=self.__copy__()
        process.addAction(action)

    
changeSource=ChangeSource()
