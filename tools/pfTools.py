#import FWCore.ParameterSet.Config as cms


import copy
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.tauTools import *
from FWCore.ParameterSet.Modules  import EDProducer
from FWCore.ParameterSet.Types  import InputTag 
from FWCore.ParameterSet.Config  import Process

def warningIsolation():
    print "WARNING: particle based isolation must be studied"

class AdaptPFMuons(ConfigToolBase):

    """
    """
    _label='AdaptPFMuons'

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython = "\nadaptPFMuons(process, "
        dumpPython += str(self.getvalue('module'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
        
    
    def __call__(self,process,module):

        self.addParameter('process',process, 'the Process')
        self.addParameter('module',module, '')
        if not isinstance(process,Process):
            raise Typeerror(self.instanceError(process,'Process'))
        if not isinstance(module,EDProducer):
            raise TypeError(self.instanceError(module,'EDProducer'))
        self.doCall()

    def doCall(self):
        
        process=self._parameters['process'].value
        module=self._parameters['module'].value
        process.disableRecording()

        print "Adapting PF Muons "
        print "***************** "
        warningIsolation()
        print 
        module.useParticleFlow = True
        module.isolation   = cms.PSet()
        module.isoDeposits = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoDepMuonWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoDepMuonWithNeutral"),
            pfPhotons = cms.InputTag("isoDepMuonWithPhotons")
            )
        module.isolationValues = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoValMuonWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoValMuonWithNeutral"),
            pfPhotons = cms.InputTag("isoValMuonWithPhotons")
            )
        # matching the pfMuons, not the standard muons.
        process.muonMatch.src = module.pfMuonSource
        
        print " muon source:", module.pfMuonSource
        print " isolation  :",
        print module.isolationValues
        print " isodeposits: "
        print module.isoDeposits
        print
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

adaptPFMuons=AdaptPFMuons()


class AdaptPFElectrons(ConfigToolBase):

    """
    """
    _label='AdaptPFElectrons'

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython = "\nadaptPFElectrons(process, "
        dumpPython += str(self.getvalue('module'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
         
    def __call__(self,process,module):
        # module.useParticleFlow = True

        self.addParameter('process',process, 'the Process')
        self.addParameter('module',module, '')
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(module,EDProducer):
            raise TypeError(self.instanceError(module,'EDProducer'))
        self.doCall()

    def doCall(self):
        
        process=self._parameters['process'].value
        module=self._parameters['module'].value
        process.disableRecording()                                
        print "Adapting PF Electrons "
        print "********************* "
        warningIsolation()
        print 
        module.useParticleFlow = True
        module.isolation   = cms.PSet()
        module.isoDeposits = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoDepElectronWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoDepElectronWithNeutral"),
            pfPhotons = cms.InputTag("isoDepElectronWithPhotons")
            )
        module.isolationValues = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoValElectronWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoValElectronWithNeutral"),
            pfPhotons = cms.InputTag("isoValElectronWithPhotons")
            )
        
        # COLIN: since we take the egamma momentum for pat Electrons, we must
        # match the egamma electron to the gen electrons, and not the PFElectron.  
        # -> do not uncomment the line below.
        # process.electronMatch.src = module.pfElectronSource
        # COLIN: how do we depend on this matching choice? 
        
        print " PF electron source:", module.pfElectronSource
        print " isolation  :"
        print module.isolationValues
        print " isodeposits: "
        print module.isoDeposits
        print 
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

adaptPFElectrons=AdaptPFElectrons()
                


##     print "Temporarily switching off isolation & isoDeposits for PF Electrons"
##     module.isolation   = cms.PSet()
##     module.isoDeposits = cms.PSet()
##     print "Temporarily switching off electron ID for PF Electrons"
##     module.isolation   = cms.PSet()
##     module.addElectronID = False
##     if module.embedTrack.value(): 
##         module.embedTrack = False
##         print "Temporarily switching off electron track embedding"
##     if module.embedGsfTrack.value(): 
##         module.embedGsfTrack = False
##         print "Temporarily switching off electron gsf track embedding"
##     if module.embedSuperCluster.value(): 
##         module.embedSuperCluster = False
##         print "Temporarily switching off electron supercluster embedding"

def adaptPFPhotons(process,module):
    raise RuntimeError, "Photons are not supported yet"

def adaptPFJets(process,module):
    module.embedCaloTowers   = False

class AdaptPFTaus(ConfigToolBase):
    """
    """
    _label='AdaptPFTaus'

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython = "\nadaptPFTaus(process, "
        dumpPython += str(self.getvalue('tauType'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,tauType = 'fixedConePFTau' ):
        
        self.addParameter('process',process, 'the Process')
        self.addParameter('tauType',tauType, '')
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not  isinstance(tauType,str):
            raise TypeError(self.typeError(tauType,'string'))
        self.doCall()

    def doCall(self):        
        process=self._parameters['process'].value
        tauType=self._parameters['tauType'].value
        process.disableRecording() 

        # MICHAL: tauType can be changed only to shrinkig cone one, otherwise request is igonred
        oldTaus = process.allLayer1Taus.tauSource
        process.allLayer1Taus.tauSource = cms.InputTag("allLayer0Taus")
        
        if tauType == 'shrinkingConePFTau': 
            print "PF2PAT: tauType changed from default \'fixedConePFTau\' to \'shrinkingConePFTau\'"
            process.allLayer0TausDiscrimination.PFTauProducer = cms.InputTag(tauType+"Producer")
            process.allLayer0Taus.src = cms.InputTag(tauType+"Producer")
            process.pfTauSequence.replace(process.fixedConePFTauProducer,
                                          process.shrinkingConePFTauProducer)
            
        if (tauType != 'shrinkingConePFTau' and tauType != 'fixedConePFTau'):
            print "PF2PAT: TauType \'"+tauType+"\' is not supported. Default \'fixedConePFTau\' is used instead."
            tauType = 'fixedConePFTau'
            
        redoPFTauDiscriminators(process, cms.InputTag(tauType+'Producer'),
                                process.allLayer1Taus.tauSource,
                                tauType)
        switchToAnyPFTau(process, oldTaus, process.allLayer1Taus.tauSource, tauType)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)


adaptPFTaus=AdaptPFTaus()


class AddPFCandidates(ConfigToolBase):
    """ Tool to add particle flow candidates to the event content. An allLayer1PFCandidate, selectedLayer1PFCandidate,
        and a corresponding count filter will be added to the patDefaultSequence.
    """
    _label='AdaptPFCandidates'

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n\nadaptPFCandidates(process, "
        dumpPython = "\nadaptPFCandidates(process, "
        dumpPython += str(self.getvalue('src'))+ ", "
        dumpPython += str(self.getvalue('patLabel'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,src,patLabel='PFParticles',cut=""):

        self.addParameter('process',process, 'the Process')
        self.addParameter('src',src, 'source of particle flow candidates as an edm::Module')
        self.addParameter('patLabel',patLabel, "collection label for PAT (default is 'PFParticles')")
        self.addParameter('cut',cut, 'cut string for the selectedLayer1PFCandidate collection (default is "")')
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not  isinstance(src,InputTag):
            raise TypeError(self.instanceError(src,'InputTag'))
        if not  isinstance(patLabel,str):
            raise TypeError(self.typeError(patLabel,'string'))
        if not isinstance(cut,str):
            raise TypeError(self.typeError(cut,'string'))
        self.doCall()

    def doCall(self):        
        process=self._parameters['process'].value
        src=self._parameters['src'].value
        patLabel=self._parameters['patLabel'].value
        cut=self._parameters['cut'].value
        process.disableRecording()                              
        from PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi import allLayer1PFParticles
        # make modules
        producer = allLayer1PFParticles.clone(pfCandidateSource = src)
        filter   = cms.EDFilter("PATPFParticleSelector", 
                                src = cms.InputTag('allLayer1' + patLabel), 
                                cut = cms.string(cut))
        counter  = cms.EDFilter("PATCandViewCountFilter",
                                minNumber = cms.uint32(0),
                                maxNumber = cms.uint32(999999),
                                src       = cms.InputTag('selectedLayer1' + patLabel))
        # add modules to process
        setattr(process, 'allLayer1'      + patLabel, producer)
        setattr(process, 'selectedLayer1' + patLabel, filter)
        setattr(process, 'countLayer1'    + patLabel, counter)
        # insert into sequence
        process.allLayer1Objects.replace(process.allLayer1Summary, producer +  process.allLayer1Summary)
        process.selectedLayer1Objects.replace(process.selectedLayer1Summary, filter +  process.selectedLayer1Summary)
        process.countLayer1Objects    += counter
        # summary tables
        process.allLayer1Summary.candidates.append(cms.InputTag('allLayer1' + patLabel))
        process.selectedLayer1Summary.candidates.append(cms.InputTag('selectedLayer1' + patLabel))
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)
           

addPFCandidates=AddPFCandidates()

class SwitchToPFMET(ConfigToolBase):
    """ Tool to switch the input of the pat::MET collection from calo MET to particle flow MET.
        Type1MET and MuonMET corrections are removed from the patDefaultSequence.
    """
    _label='SwitchToPFMET'
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython = "\nswitchToPFMET(process, "
        dumpPython += str(self.getvalue('input'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,input=cms.InputTag('pfMET')):

        self.addParameter('process',process, 'the  process')
        self.addParameter('input',input, "input collection label to the pat::MET producer (default is 'pfMET')")
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(input,InputTag):
            raise TypeError(self.instanceError(input,'InputTag'))
        self.doCall()

    def doCall(self):        
        process=self._parameters['process'].value
        input=self._parameters['input'].value
        process.disableRecording()
                                                     
        print 'MET: using ', input
        oldMETSource = process.layer1METs.metSource
        process.layer1METs.metSource = input
        process.layer1METs.addMuonCorrections = False
        process.patDefaultSequence.remove(process.patMETCorrections)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)
       
switchToPFMET=SwitchToPFMET()

class SwitchToPFJets(ConfigToolBase):
    """ Tool to switch the input of the pat::Jet collection from calo jets to particle flow jets.
        The jet collection stays the same. No residual jet or MET corrections are applied
    """
    _label='SwitchToPFJets'

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython = "\nswitchToPFJets(process, "
        dumpPython += str(self.getvalue('input'))+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,input=cms.InputTag('pfNoTau')):
        self.addParameter('process',process, 'the process')
        self.addParameter('input',input, "input collection label to the pat::Jet producer as an edm::Module (default is 'pfNoTau')")
        print type(input)
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(input,InputTag):
            raise TypeError(self.instanceError(input,'InputTag'))
        self.doCall()

    def doCall(self):        
        process=self._parameters['process'].value
        input=self._parameters['input'].value
        process.disableRecording()
                         
        print 'Jets: using ', input
        switchJetCollection(process,
                            input,
                            doJTA=True,
                            doBTagging=True,
                            jetCorrLabel=None, 
                            doType1MET=False)  
        adaptPFJets(process, process.allLayer1Jets)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

switchToPFJets=SwitchToPFJets()

class  UsePF2PAT(ConfigToolBase):
    """ Switch PAT to use PF2PAT instead of AOD sources. if 'runPF2PAT' is true, we'll also add PF2PAT in front of the PAT sequence
    """
    _label='UsePF2PAT'

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython = "\nusePF2PAT(process, "
        dumpPython += str(self.getvalue('process'))+ ", "
        dumpPython += str(self.getvalue('runPF2PAT'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,runPF2PAT=True):

        self.addParameter('process',process, 'the  process')
        self.addParameter('runPF2PAT',runPF2PAT, 'Run the PF2PAT sequence before pat::Candidate production (default is True)')
        if not isinstance(process,Process):
            raise TypeError(self.instanceError(process,'Process'))
        if not isinstance(runPF2PAT,bool):
            raise TypeError(self.typeError(runPF2PAT,'bool'))
        self.doCall()

    def doCall(self):       
        process=self._parameters['process'].value
        runPF2PAT=self._parameters['runPF2PAT'].value
        process.disableRecording()                         
        # PLEASE DO NOT CLOBBER THIS FUNCTION WITH CODE SPECIFIC TO A GIVEN PHYSICS OBJECT.
        # CREATE ADDITIONAL FUNCTIONS IF NEEDED. 
        
        # -------- CORE ---------------
        if runPF2PAT:
            process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")
            
            #        process.dump = cms.EDAnalyzer("EventContentAnalyzer")
            process.patDefaultSequence.replace(process.allLayer1Objects,
                                               process.PF2PAT +
                                               process.allLayer1Objects
                                               )
            
        removeCleaning(process)
            
        # -------- OBJECTS ------------
        # Muons
        adaptPFMuons(process,process.allLayer1Muons)
            
        
        # Electrons
        adaptPFElectrons(process,process.allLayer1Electrons)
        
        # Photons
        print "Temporarily switching off photons completely"
        removeSpecificPATObjects(process,['Photons'])
        process.patDefaultSequence.remove(process.patPhotonIsolation)
        
        # Jets
        switchToPFJets( process, cms.InputTag('pfNoTau') )
        
        # Taus
        adaptPFTaus( process ) #default (i.e. fixedConePFTau)
        #adaptPFTaus( process, tauType='shrinkingConePFTau' )
    
        # MET
        switchToPFMET(process, cms.InputTag('pfMET'))
        
        # Unmasked PFCandidates
        addPFCandidates(process,cms.InputTag('pfNoJet'),patLabel='PFParticles',cut="")
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

usePF2PAT=UsePF2PAT()
