#import FWCore.ParameterSet.Config as cms
import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *


class RestrictInputToAOD(ConfigToolBase):
    
    """
        ------------------------------------------------------------------
        remove pat object production steps which rely on RECO event
        content:
        
        process : process
        name    : list of collection names; supported are 'Photons', 
        'Electrons',, 'Muons', 'Taus', 'Jets', 'METs', 'All'
        ------------------------------------------------------------------    
        """

    
    _label='RestrictInputToAOD'
    
    def dumpPython(self):
        
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n\nrestrictInputToAOD(process, "
        dumpPython += str(self.getvalue('names'))+'\n'
        return dumpPython

    
    def __call__(self,process,
                           names
                           ):
      
        self.addParameter('process',process, 'The process')
        self.addParameter('names',names, "list of collection names; supported are 'Photons', 'Electrons',, 'Muons', 'Taus', 'Jets', 'METs', 'All'")
        
        process=self._parameters['process'].value
        names=self._parameters['names'].value
        process.disableRecording()                                     
        for obj in range(len(names)):
            print "-----------------------------------------------------------------------------"
            print "WARNING: the following additional information can only be used on RECO format"
            if( names[obj] == 'Photons' or names[obj] == 'All' ):
                print "          * gamIsoDepositEcalFromHits"
                print "          * gamIsoFromDepsEcalFromHits" 
            ## get allLayer1Photons module
                photonProducer = getattr(process, 'allLayer1Photons')
            ## remove gamIsoDepositEcalFromHits from sequence and pat photon
                process.makeAllLayer1Photons.remove(process.gamIsoDepositEcalFromHits)
                process.makeAllLayer1Photons.remove(process.gamIsoFromDepsEcalFromHits)
                photonProducer.isoDeposits = cms.PSet(
                    tracker = cms.InputTag("gamIsoDepositTk"),
                    hcal = cms.InputTag("gamIsoDepositHcalFromTowers"),
                    )
                photonProducer.isolation = cms.PSet(tracker = cms.PSet(src = cms.InputTag("gamIsoFromDepsTk"),),
                                                    hcal = cms.PSet(src = cms.InputTag("gamIsoFromDepsHcalFromTowers"),),
                                                    )
                
            if( names[obj] == 'Electrons' or names[obj] == 'All' ):
                print "          * eidRobustHighEnergy"
                print "          * eleIsoDepositEcalFromHits"
                print "          * eleIsoFromDepsEcalFromHits" 
            ## get allLayer1Electrons module
                electronProducer = getattr(process, 'allLayer1Electrons')
            ## remove eidRobustHighEnergy from sequence and pat electron
                process.makeAllLayer1Electrons.remove(process.eidRobustHighEnergy)
                electronProducer.electronIDSources = cms.PSet(
                    eidRobustLoose = cms.InputTag("eidRobustLoose"),
                    eidRobustTight = cms.InputTag("eidRobustTight"),
                    eidLoose       = cms.InputTag("eidLoose"),
                    eidTight       = cms.InputTag("eidTight"),
                    )
            ## remove eleIsoDepositEcalFromHits from sequence and pat electron
                process.makeAllLayer1Electrons.remove(process.eleIsoDepositEcalFromHits)
                process.makeAllLayer1Electrons.remove(process.eleIsoFromDepsEcalFromHits)
                electronProducer.isoDeposits = cms.PSet(tracker = cms.InputTag("eleIsoDepositTk"),
                                                        hcal = cms.InputTag("eleIsoDepositHcalFromTowers"),
                                                        )
                electronProducer.isolation = cms.PSet(
                    tracker = cms.PSet(src = cms.InputTag("eleIsoFromDepsTk"),),
                    hcal = cms.PSet(src = cms.InputTag("eleIsoFromDepsHcalFromTowers"),),
                    )
                
            if( names[obj] == 'Jets' or names[obj] == 'All' ):
                print "          * jetID"
            ## get allLayer1Electrons module
                jetProducer = getattr(process, 'allLayer1Jets')
                jetProducer.addJetID = False
                jetProducer.jetID = cms.PSet()
        print "-----------------------------------------------------------------------------"

        process.enableRecording()
        action = Action("RestrictInputToAOD",copy.copy(self._parameters),self)
        process.addAction(action)
        
restrictInputToAOD=RestrictInputToAOD()          

class RemoveMCMatching(ConfigToolBase):
    
    """
    ------------------------------------------------------------------
    remove monte carlo matching from a given collection or all PAT
    candidate collections:
    
    process : process
    name    : collection name; supported are 'Photons', 'Electrons',
    'Muons', 'Taus', 'Jets', 'METs', 'All'
    ------------------------------------------------------------------    
    """

    _label='RemoveMCMatching'
    
    def dumpPython(self):
        
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n\nremoveMCMatching(process, "
        dumpPython += str(self.getvalue('name'))+'\n'
        return dumpPython

    def __call__(self,process,
                         name
                         ):
        self.addParameter('process',process, 'The process')
        self.addParameter('name',name, "name    : collection name; supported are 'Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All'")
                
        process=self._parameters['process'].value
        name=self._parameters['name'].value
        process.disableRecording()
        if( name == 'Photons'   or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'photonMatch', 'allLayer1Photons') 
        if( name == 'Electrons' or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'electronMatch', 'allLayer1Electrons') 
        if( name == 'Muons'     or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'muonMatch', 'allLayer1Muons') 
        if( name == 'Taus'      or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'tauMatch', 'allLayer1Taus')
        ## remove mc extra modules for taus
            process.patDefaultSequence.remove(process.tauGenJets)
            process.patDefaultSequence.remove(process.tauGenJetMatch)
        ## remove mc extra configs for taus
            tauProducer = getattr(process, 'allLayer1Taus')
            tauProducer.addGenJetMatch      = False
            tauProducer.embedGenJetMatch    = False
            tauProducer.genJetMatch         = ''         
        if( name == 'Jets'      or name == 'All' ):
        ## remove mc extra modules for jets
            process.patDefaultSequence.remove(process.jetPartonMatch)
            process.patDefaultSequence.remove(process.jetGenJetMatch)
            process.patDefaultSequence.remove(process.jetFlavourId)
        ## remove mc extra configs for jets
            jetProducer = getattr(process, 'allLayer1Jets')
            jetProducer.addGenPartonMatch   = False
            jetProducer.embedGenPartonMatch = False
            jetProducer.genPartonMatch      = ''
            jetProducer.addGenJetMatch      = False
            jetProducer.genJetMatch         = ''
            jetProducer.getJetMCFlavour     = False
            jetProducer.JetPartonMapSource  = ''       
        if( name == 'METs'      or name == 'All' ):
        ## remove mc extra configs for jets
            metProducer = getattr(process, 'layer1METs')        
            metProducer.addGenMET           = False
            metProducer.genMETSource        = ''       
        process.enableRecording()
        action = Action("removeMCMatching",copy.copy(self._parameters),self)
        process.addAction(action)

removeMCMatching=RemoveMCMatching()

class _RemoveMCMatchingForPATObject(ConfigToolBase):

      def __call__(self,process, matcherName, producerName):
        
        self.addParameter('process',process, 'the process')
        self.addParameter('matcherName',matcherName, 'name of matcher')
        self.addParameter('producerName',producerName, 'name of producer')
        
        process=self._parameters['process'].value
        matcherName=self._parameters['matcherName'].value
        producerName=self._parameters['producerName'].value
        process.disableRecording()

    ## remove mcMatcher from the default sequence
        objectMatcher = getattr(process, matcherName)
        process.patDefaultSequence.remove(objectMatcher)
    ## straighten photonProducer
        objectProducer = getattr(process, producerName)
        objectProducer.addGenMatch      = False
        objectProducer.embedGenMatch    = False
        objectProducer.genParticleMatch = ''    

_removeMCMatchingForPATObject=_RemoveMCMatchingForPATObject()


class RemoveAllPATObjectsBut(ConfigToolBase):

    """
    ------------------------------------------------------------------
    remove all PAT objects from the default sequence but a specific
    one:
    
    process : process
    name    : list of collection names; supported are 'Photons',
    'Electrons', 'Muons', 'Taus', 'Jets', 'METs'
    ------------------------------------------------------------------    
    """
    _label='RemoveAllPATObjectsBut'
    
    def dumpPython(self):
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n\nRemoveAllPATObjectsBut(process, "
        dumpPython += str(self.getvalue('names'))+'\n'
        return dumpPython 
   
    def __call__(self,process,
                 names
                 ):
          
        self.addParameter('process',process, 'the progess')
        self.addParameter('names',names, "name    : list of collection names; supported are 'Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs'")
        
        process=self._parameters['process'].value
        names=self._parameters['names'].value
        process.disableRecording()                                
        removeTheseObjectCollections = ['Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs']
        for obj in range(len(names)):
            removeTheseObjectCollections.remove(names[obj])
        removeSpecificPATObjects(process, removeTheseObjectCollections)
        process.enableRecording()
        action = Action("RemoveAllPATObjectsBut",copy.copy(self._parameters),self)
        process.addAction(action)
                
            
removeAllPATObjectsBut= RemoveAllPATObjectsBut()

class RemoveSpecificPATObjects(ConfigToolBase):

    """
    ------------------------------------------------------------------
    remove a specific PAT object from the default sequence:
    
    process : process
    names   : listr of collection names; supported are 'Photons',
    'Electrons', 'Muons', 'Taus', 'Jets', 'METs'
    ------------------------------------------------------------------    
    """
    _label='RemoveSpecificPATObjects'
    
    def dumpPython(self):
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n\nremoveSpecificPATObjects(process, "
        dumpPython += str(self.getvalue('names'))+'\n'
        return dumpPython 
    
    def __call__(process,
                 names
                 ):
        
        self.addParameter('process',process, 'the process')
        self.addParameter('names',names, "names   : listr of collection names; supported are 'Photons','Electrons', 'Muons', 'Taus', 'Jets', 'METs'")
        
        process=self._parameters['process'].value
        names=self._parameters['names'].value
        process.disableRecording()                          
    ## remove pre object production steps from the default sequence
        for obj in range(len(names)):
            if( names[obj] == 'Photons' ):
                process.patDefaultSequence.remove(getattr(process, 'patPhotonIsolation'))
                process.patDefaultSequence.remove(getattr(process, 'photonMatch'))            
            if( names[obj] == 'Electrons' ):
                process.patDefaultSequence.remove(getattr(process, 'patElectronId'))
                process.patDefaultSequence.remove(getattr(process, 'patElectronIsolation'))
                process.patDefaultSequence.remove(getattr(process, 'electronMatch'))        
            if( names[obj] == 'Muons' ):
                process.patDefaultSequence.remove(getattr(process, 'muonMatch'))
            if( names[obj] == 'Taus' ):
                process.patDefaultSequence.remove(getattr(process, 'patPFCandidateIsoDepositSelection'))
                process.patDefaultSequence.remove(getattr(process, 'patPFTauIsolation'))
                process.patDefaultSequence.remove(getattr(process, 'tauMatch'))
                process.patDefaultSequence.remove(getattr(process, 'tauGenJets'))
                process.patDefaultSequence.remove(getattr(process, 'tauGenJetMatch'))
            if( names[obj] == 'Jets' ):
                process.patDefaultSequence.remove(getattr(process, 'patJetCharge'))
                process.patDefaultSequence.remove(getattr(process, 'patJetCorrections'))
                process.patDefaultSequence.remove(getattr(process, 'jetPartonMatch'))
                process.patDefaultSequence.remove(getattr(process, 'jetGenJetMatch'))
                process.patDefaultSequence.remove(getattr(process, 'jetFlavourId'))                
            if( names[obj] == 'METs' ):
                process.patDefaultSequence.remove(getattr(process, 'patMETCorrections'))                
        ## remove cleaning for the moment; in principle only the removed object
        ## could be taken out of the checkOverlaps PSet
            removeCleaning(process)
        
        ## remove object production steps from the default sequence    
            if( names[obj] == 'METs' ):
                process.allLayer1Objects.remove( getattr(process, 'layer1'+names[obj]) )
            else:
                process.allLayer1Objects.remove( getattr(process, 'allLayer1'+names[obj]) )
                process.selectedLayer1Objects.remove( getattr(process, 'selectedLayer1'+names[obj]) )
                process.countLayer1Objects.remove( getattr(process, 'countLayer1'+names[obj]) )
        ## in the case of leptons, the lepton counter must be modified as well
            if( names[obj] == 'Electrons' ):
                print 'removed from lepton counter: electrons'
                process.countLayer1Leptons.countElectrons = False
            elif( names[obj] == 'Muons' ):
                print 'removed from lepton counter: muons'
                process.countLayer1Leptons.countMuons = False
            elif( names[obj] == 'Taus' ):
                print 'removed from lepton counter: taus'
                process.countLayer1Leptons.countTaus = False
        ## remove from summary
            if( names[obj] == 'METs' ):
                process.allLayer1Summary.candidates.remove( cms.InputTag('layer1'+names[obj]) )
            else:
                process.allLayer1Summary.candidates.remove( cms.InputTag('allLayer1'+names[obj]) )
                process.selectedLayer1Summary.candidates.remove( cms.InputTag('selectedLayer1'+names[obj]) )
                process.cleanLayer1Summary.candidates.remove( cms.InputTag('cleanLayer1'+names[obj]) )
        process.enableRecording()
        action = Action("RemoveSpecificPATObjects",copy.copy(self._parameters),self)
        process.addAction(action)
                
    
removeSpecificPATObjects=RemoveSpecificPATObjects()



class RemoveCleaning(ConfigToolBase):
    """
    ------------------------------------------------------------------
    remove PAT cleaning from the default sequence:
    
    process : process
    ------------------------------------------------------------------    
    """
    _label='RemoveCleaning'
    
    def dumpPython(self):
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n\nremoveCleaning(process) \n "
        return dumpPython 
    
    
    def removeCleaning(process):
    
        self.addParameter('process',process, 'the process')
                
        process=self._parameters['process'].value
        process.disableRecording()                               
    ## adapt single object counters
        for m in listModules(process.countLayer1Objects):
            if hasattr(m, 'src'): m.src = m.src.value().replace('cleanLayer1','selectedLayer1')
    ## adapt lepton counter
        countLept = process.countLayer1Leptons
        countLept.electronSource = countLept.electronSource.value().replace('cleanLayer1','selectedLayer1')
        countLept.muonSource = countLept.muonSource.value().replace('cleanLayer1','selectedLayer1')
        countLept.tauSource = countLept.tauSource.value().replace('cleanLayer1','selectedLayer1')
        process.patDefaultSequence.remove(process.cleanLayer1Objects)
    ## add selected layer1 objects to the pat output
        from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoLayer1Cleaning
        process.out.outputCommands = patEventContentNoLayer1Cleaning
        process.enableRecording()
        action = Action("RemoveCleaning",copy.copy(self._parameters),self)
        process.addAction(action)

removeCleaning=RemoveCleaning()                

class AddCleaning(ConfigToolBase):

    """
    ------------------------------------------------------------------
    add PAT cleaning from the default sequence:
    
    process : process
    ------------------------------------------------------------------    
    """
    _label='AddCleaning'
    
    def dumpPython(self):
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n\naddCleaning(process) \n "
        return dumpPython 
       
    def __call__(self,process):
    
        self.addParameter('process',process, 'the process')

        process=self._parameters['process'].value
        process.disableRecording()    

    ## adapt single object counters
        process.patDefaultSequence.replace(process.countLayer1Objects, process.cleanLayer1Objects * process.countLayer1Objects)
        for m in listModules(process.countLayer1Objects):
            if hasattr(m, 'src'): m.src = m.src.value().replace('selectedLayer1','cleanLayer1')
    ## adapt lepton counter
        countLept = process.countLayer1Leptons
        countLept.electronSource = countLept.electronSource.value().replace('selectedLayer1','cleanLayer1')
        countLept.muonSource = countLept.muonSource.value().replace('selectedLayer1','cleanLayer1')
        countLept.tauSource = countLept.tauSource.value().replace('selectedLayer1','cleanLayer1')
    ## add clean layer1 objects to the pat output
        from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
        process.out.outputCommands = patEventContent               
        process.enableRecording()
        action = Action("AddCleaning",copy.copy(self._parameters),self)
        process.addAction(action)
         
addCleaning=AddCleaning()
