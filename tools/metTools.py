
#import FWCore.ParameterSet.Config as cms

import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.ParameterSet.Config  import Process

class AddTcMET(ConfigToolBase):

    _label='AddTcMET'
    
    """
    ------------------------------------------------------------------
    add track corrected MET collection to patEventContent:
    
    process : process
    ------------------------------------------------------------------
    """

  
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.metTools import *\n"
        dumpPython = "\naddTcMET(process, "
        dumpPython += str(self.getvalue('postfixLabel'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    

    def __call__(self,process,
                 postfixLabel = 'TC'):



        self.addParameter('process',process, 'The  process')
        self.addParameter('postfixLabel',postfixLabel, '')
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(postfixLabel,str):
            raise typeError(self.typeError(postfixLabel,'string'))
        self.doCall()

    def doCall(self):

        process=self._parameters['process'].value
        postfixLabel=self._parameters['postfixLabel'].value
        process.disableRecording()
    ## add module as process to the default sequence
        def addAlso (label,value):
            existing = getattr(process, label)
            setattr( process, label+postfixLabel, value)
            process.patDefaultSequence.replace( existing, existing*value )        
            
    ## clone and add a module as process to the
    ## default sequence
        def addClone(label,**replaceStatements):
            new = getattr(process, label).clone(**replaceStatements)
            addAlso(label, new)

    ## addClone('corMetType1Icone5Muons', uncorMETInputTag = cms.InputTag("tcMet"))
        addClone('layer1METs', metSource = cms.InputTag("tcMet"))

    ## add new met collections output to the pat summary
        process.allLayer1Summary.candidates += [ cms.InputTag('layer1METs'+postfixLabel) ]
        process.enableRecording()
        action=self.__copy__()
        process.addAction(action)

                                                        

addTcMET=AddTcMET()


class AddPfMET(ConfigToolBase):

    _label='AddPfMET'
    

    """
    ------------------------------------------------------------------
    add pflow MET collection to patEventContent:
    
    process : process
    ------------------------------------------------------------------
    """
    
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.metTools import *\n"
        dumpPython = "\naddPfMET(process, "
        dumpPython += str(self.getvalue('postfixLabel'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
            
    def __call__(self,process,
                 postfixLabel = 'PF'):

        self.addParameter('process',process, 'The process')
        self.addParameter('postfixLabel',postfixLabel, '')
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(postfixLabel,str):
            raise TypeError(self.typeError(postfixLabel,'string'))
        self.doCall()

    def doCall(self):
        
        process=self._parameters['process'].value
        postfixLabel=self._parameters['postfixLabel'].value
        process.disableRecording()                                
    ## add module as process to the default sequence
        def addAlso (label,value):
            existing = getattr(process, label)
            setattr( process, label+postfixLabel, value)
            process.patDefaultSequence.replace( existing, existing*value )        
            
    ## clone and add a module as process to the
    ## default sequence
        def addClone(label,**replaceStatements):
            new = getattr(process, label).clone(**replaceStatements)
            addAlso(label, new)
            
    ## addClone('corMetType1Icone5Muons', uncorMETInputTag = cms.InputTag("tcMet"))
        addClone('layer1METs', metSource = cms.InputTag("pfMet"), addMuonCorrections = False)
                
    ## add new met collections output to the pat summary
        process.allLayer1Summary.candidates += [ cms.InputTag('layer1METs'+postfixLabel) ]
        process.enableRecording()
        action=self.__copy__()
        process.addAction(action)
                

                
addPfMET=AddPfMET()
