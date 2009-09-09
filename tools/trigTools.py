#import FWCore.ParameterSet.Config as cms
import copy
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from PhysicsTools.PatAlgos.patEventContent_cff import *

class SwitchOnTrigger(ConfigToolBase):
    
    def __call__(self, process ):
        """ Enables trigger information in PAT  """

        self.addParameter('process',process, 'description: process')
            
        process=self._parameters['process'].value
    
    ## add trigger modules to path
        process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
        process.patDefaultSequence += process.patTriggerSequence

    ## configure pat trigger
        process.patTrigger.onlyStandAlone = False
        
    ## add trigger specific event content to PAT event content
        process.out.outputCommands += patTriggerEventContent
        for matchLabel in process.patTriggerEvent.patTriggerMatches:
            process.out.outputCommands += [ 'keep patTriggerObjectsedmAssociation_patTriggerEvent_' + matchLabel + '_*' ]

            action = Action("SwitchOnTrigger",copy.copy(self._parameters),self)
            process.addAction(action)

switchOnTrigger=SwitchOnTrigger()

class SwitchOnTriggerStandAlone(ConfigToolBase):

    def __call__(self, process ):
    ## add trigger modules to path

        self.addParameter('process',process, 'description: process')
        
        process=self._parameters['process'].value
        
        process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
        process.patDefaultSequence += process.patTriggerSequence
        
    ## configure pat trigger
        process.patTrigger.onlyStandAlone = True
        process.patTriggerSequence.remove( process.patTriggerEvent )
        process.out.outputCommands += patTriggerStandAloneEventContent

        action = Action("SwitchOnTriggerStandAlone",copy.copy(self._parameters),self)
        process.addAction(action)
               
switchOnTriggerStandAlone=SwitchOnTriggerStandAlone()

class SwitchOnTriggerAll(ConfigToolBase):
    def __call__( process ):

        self.addParameter('process',process, 'description: process')
        
        process=self._parameters['process'].value
                  
        switchOnTrigger( process )
        process.out.outputCommands += patTriggerStandAloneEventContent
        action = Action("SwitchOnTriggerAll",copy.copy(self._parameters),self)
        process.addAction(action)

switchOnTriggerAll=SwitchOnTriggerAll()

class SwitchOnTriggerMatchEmbedding(ConfigToolBase):
    def __call__(self,process ):
        self.addParameter('process',process, 'description: process')
        process=self._parameters['process'].value
                 
        process.patTriggerSequence += process.patTriggerMatchEmbedder
        process.out.outputCommands += patEventContentTriggerMatch
        action = Action("SwitchOnTriggerMatchEmbedding",copy.copy(self._parameters),self)
        process.addAction(action)
switchOnTriggerMatchEmbedding=SwitchOnTriggerMatchEmbedding()
