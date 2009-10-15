#import FWCore.ParameterSet.Config as cms


import copy

from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from PhysicsTools.PatAlgos.tools.coreTools import *
from FWCore.ParameterSet.Types  import InputTag 
from FWCore.ParameterSet.Config  import Process

class RedoPFTauDiscriminators(ConfigToolBase):
    """
    """
    _label='RedoPFTauDiscriminators'
    
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython = "\nredoPFTauDiscriminators(process, "
        dumpPython += str(self.getvalue('oldPFTauLabel'))+ ", "
        dumpPython += str(self.getvalue('newPFTauLabel'))+", "
        dumpPython += str(self.getvalue('tauType'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,
                 oldPFTauLabel = cms.InputTag('pfRecoTauProducer'),
                 newPFTauLabel = cms.InputTag('pfRecoTauProducer'),
                 tauType='fixedConePFTau'):
        
        self.addParameter('process',process, 'the process')
        self.addParameter('oldPFTauLabel',oldPFTauLabel, '')
        self.addParameter('newPFTauLabel',newPFTauLabel, '')
        self.addParameter('tauType',tauType, 'description: label')
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(oldPFTauLabel,InputTag),self.instanceError(oldPFTauLabel,'InputTag')
        assert isinstance(newPFTauLabel,InputTag), self.instanceError(newPFTauLabel,'InputTag')
        assert isinstance(tauType,str), self.typeError(tauType,'string')
        self.doCall() 
        
    def doCall(self):  
        process=self._parameters['process'].value
        oldPFTauLabel =self._parameters['oldPFTauLabel'].value
        newPFTauLabel =self._parameters['newPFTauLabel'].value
        tauType=self._parameters['tauType'].value
        process.disableRecording()
                
        print 'Tau discriminators: ', oldPFTauLabel, '->', newPFTauLabel
        print 'Tau type: ', tauType
        tauSrc = 'PFTauProducer'
        tauDiscriminationSequence = process.patFixedConePFTauDiscrimination
        if tauType == 'fixedConeHighEffPFTau':
            tauDiscriminationSequence = process.patFixedConeHighEffPFTauDiscrimination
        elif tauType == 'shrinkingConePFTau':
            tauDiscriminationSequence = process.patShrinkingConePFTauDiscrimination
        elif tauType == 'caloTau':
            tauDiscriminationSequence = process.patCaloTauDiscrimination
            tauSrc = 'CaloTauProducer'
            process.patDefaultSequence.replace(process.allLayer1Objects,
                                               tauDiscriminationSequence +
                                               process.allLayer1Objects
                                               )
        massSearchReplaceParam(tauDiscriminationSequence, tauSrc, oldPFTauLabel, newPFTauLabel)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

redoPFTauDiscriminators=RedoPFTauDiscriminators()

# switch to CaloTau collection

class SwitchToCaloTau(ConfigToolBase):
    """ Tool to switch from particle flow taus to calo taus as input to the production of the pat::Tau collection
    """
    _label='SwitchToCaloTau'
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython = "\nswitchToCaloTau(process, "
        dumpPython += str(self.getvalue('pfTauLabel'))+ ", "
        dumpPython += str(self.getvalue('caloTauLabel'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,
                 pfTauLabel = cms.InputTag('fixedConePFTauProducer'),
                 caloTauLabel = cms.InputTag('caloRecoTauProducer')):


        self.addParameter('process',process, 'the process')
        self.addParameter('pfTauLabel',pfTauLabel, "label of the (original) particle flow tau collection as a string (default is 'fixedConePFTauProducer')")
        self.addParameter('caloTauLabel',caloTauLabel, "label of the (new) calo tau collection as a string (default is 'caloRecoTauProducer')")
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(pfTauLabel,InputTag), self.instanceError(pfTauLabel,'InputTag')
        assert isinstance(caloTauLabel,InputTag), self.instanceError(caloTauLabel,'InputTag')
        self.doCall() 
        
    def doCall(self):          
        process=self._parameters['process'].value
        pfTauLabel=self._parameters['pfTauLabel'].value
        caloTauLabel=self._parameters['caloTauLabel'].value
        process.disableRecording()
                
        process.tauMatch.src       = caloTauLabel
        process.tauGenJetMatch.src = caloTauLabel
        process.allLayer1Taus.tauSource = caloTauLabel
        process.allLayer1Taus.tauIDSources = cms.PSet(
            leadingTrackFinding = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackFinding"),
            leadingTrackPtCut   = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackPtCut"),
            byIsolation         = cms.InputTag("caloRecoTauDiscriminationByIsolation"),
            againstElectron     = cms.InputTag("caloRecoTauDiscriminationAgainstElectron"),  
            )
        process.allLayer1Taus.addDecayMode = False
    ## Isolation is somewhat an issue, so we start just by turning it off
        print "NO PF Isolation will be computed for CaloTau (this could be improved later)"
        process.allLayer1Taus.isolation   = cms.PSet()
        process.allLayer1Taus.isoDeposits = cms.PSet()
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)
switchToCaloTau=SwitchToCaloTau()


 
# internal auxiliary function to switch to **any** PFTau collection
def _switchToPFTau(process, pfTauLabelOld, pfTauLabelNew, pfTauType):

    print ' Taus: ', pfTauLabelOld, '->', pfTauLabelNew

    process.tauMatch.src       = pfTauLabelNew
    process.tauGenJetMatch.src = pfTauLabelNew
    process.tauIsoDepositPFCandidates.src = pfTauLabelNew
    process.tauIsoDepositPFCandidates.ExtractorPSet.tauSource = pfTauLabelNew
    process.tauIsoDepositPFChargedHadrons.src = pfTauLabelNew
    process.tauIsoDepositPFChargedHadrons.ExtractorPSet.tauSource = pfTauLabelNew
    process.tauIsoDepositPFNeutralHadrons.src = pfTauLabelNew
    process.tauIsoDepositPFNeutralHadrons.ExtractorPSet.tauSource = pfTauLabelNew
    process.tauIsoDepositPFGammas.src = pfTauLabelNew
    process.tauIsoDepositPFGammas.ExtractorPSet.tauSource = pfTauLabelNew
    process.allLayer1Taus.tauSource = pfTauLabelNew
    process.allLayer1Taus.tauIDSources = cms.PSet(
        leadingTrackFinding = cms.InputTag(pfTauType + "DiscriminationByLeadingTrackFinding"),
        leadingTrackPtCut = cms.InputTag(pfTauType + "DiscriminationByLeadingTrackPtCut"),
        trackIsolation = cms.InputTag(pfTauType + "DiscriminationByTrackIsolation"),
        ecalIsolation = cms.InputTag(pfTauType + "DiscriminationByECALIsolation"),
        byIsolation = cms.InputTag(pfTauType + "DiscriminationByIsolation"),
        againstElectron = cms.InputTag(pfTauType + "DiscriminationAgainstElectron"),
        againstMuon = cms.InputTag(pfTauType + "DiscriminationAgainstMuon")
        #
        # CV: TaNC only trained for shrinkingCone PFTaus up to now,
        #     so cannot implement switch of TaNC based discriminators
        #     generically for all kinds of PFTaus yet...
        #
        #byTaNC = cms.InputTag(pfTauType + "DiscriminationByTaNC"),
        #byTaNCfrOnePercent = cms.InputTag(pfTauType + "DiscriminationByTaNCfrOnePercent"),
        #byTaNCfrHalfPercent = cms.InputTag(pfTauType + "DiscriminationByTaNCfrHalfPercent"),
        #byTaNCfrQuarterPercent = cms.InputTag(pfTauType + "DiscriminationByTaNCfrQuarterPercent"),
        #byTaNCfrTenthPercent = cms.InputTag(pfTauType + "DiscriminationByTaNCfrTenthPercent")
    )
    process.allLayer1Taus.decayModeSrc = cms.InputTag(pfTauType + "DecayModeProducer")


class SwitchToPFTauFixedCone(ConfigToolBase):
    # switch to PFTau collection produced for fixed dR = 0.07 signal cone size
    """ Tool to switch from the standard particle flow taus to the fixed cone particle flow taus as input to the production of the pat::Tau collection
    """
    _label='SwitchToPFTauFixedCone'
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython = "\nswitchToPFTauFixedCone(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,
                 pfTauLabelOld = cms.InputTag('pfRecoTauProducer'),
                 pfTauLabelNew = cms.InputTag('fixedConePFTauProducer')):

        self.addParameter('process',process, 'the process')
        self.addParameter('pfTauLabelOld',pfTauLabelOld, "label of the original particle flow tau collection as a string (default is 'pfRecoTauProducer')")
        self.addParameter('pfTauLabelNew',pfTauLabelNew, "label of the new particle flow tau collection as a string (default is 'fixedConePFTauProducer')")
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(pfTauLabelOld,InputTag),self.istanceError(pfTauLabelOld,'InputTag')
        assert isinstance(pfTauLabelNew,InputTag), self.istanceError(pfTauLabelNew,'InputTag')
        self.doCall() 
        
    def doCall(self):  
        
        process=self._parameters['process'].value
        pfTauLabelOld=self._parameters['pfTauLabelOld'].value
        pfTauLabelNew=self._parameters['pfTauLabelNew'].value
        process.disableRecording()
                
        _switchToPFTau(process, pfTauLabelOld, pfTauLabelNew, 'fixedConePFTau')
        #
        # CV: PFTauDecayMode objects produced only for shrinking cone reco::PFTaus in
        #     RecoTauTag/Configuration global_PFTau_22X_V00-02-01 and CMSSW_3_1_x tags,
        #     so need to disable embedding of PFTauDecayMode information into pat::Tau for now...
        #
        process.allLayer1Taus.addDecayMode = cms.bool(False)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

switchToPFTauFixedCone=SwitchToPFTauFixedCone()

class SwitchToPFTauFixedConeHighEff(ConfigToolBase):
    """ Tool to switch from the standard particle flow taus to the fixed cone particle flow taus as input to the production of the pat::Tau collection
    """
    _label='SwitchToPFTauFixedConeHighEff'
    
    # switch to PFTau collection produced for fixed dR = 0.15 signal cone size
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython = "\nswitchToPFTauFixedConeHighEff(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
     
    def __call__(self,process,
                 pfTauLabelOld = cms.InputTag('pfRecoTauProducer'),
                 pfTauLabelNew = cms.InputTag('fixedConeHighEffPFTauProducer')):
        
        self.addParameter('process',process, 'the process')
        self.addParameter('pfTauLabelOld',pfTauLabelOld, "label of the original particle flow tau collection as a string (default is 'pfRecoTauProducer')")
        self.addParameter('pfTauLabelNew',pfTauLabelNew, "label of the new particle flow tau collection as a string (default is 'fixedConeHighEffPFTauProducer')")
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(pfTauLabelOld,InputTag),self.instanceError(pfTauLabelOld,'InputTag')
        assert isinstance(pfTauLabelNew,InputTag), self.instanceError(pfTauLabelNew,'InputTag')
        self.doCall() 
        
    def doCall(self):          
        process=self._parameters['process'].value
        pfTauLabelOld=self._parameters['pfTauLabelOld'].value
        pfTauLabelNew=self._parameters['pfTauLabelNew'].value
        process.disableRecording()
               
        _switchToPFTau(process, pfTauLabelOld, pfTauLabelNew, 'fixedConeHighEffPFTau')
        #
        # CV: PFTauDecayMode objects produced only for shrinking cone reco::PFTaus in
        #     RecoTauTag/Configuration global_PFTau_22X_V00-02-01 and CMSSW_3_1_x tags,
        #     so need to disable embedding of PFTauDecayMode information into pat::Tau for now...
        #
        process.allLayer1Taus.addDecayMode = cms.bool(False)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)
        
switchToPFTauFixedConeHighEff=SwitchToPFTauFixedConeHighEff()


class SwitchToPFTauShrinkingCone(ConfigToolBase):
    """ Tool to switch from the standard particle flow taus to the fixed cone particle flow taus as input to the production of the pat::Tau collection
    """
    _label='SwitchToPFTauShrinkingCone'
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython = "\nswitchToPFTauShrinkingCone(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
 
    # switch to PFTau collection produced for shrinking signal cone of size dR = 5.0/Et(PFTau)
    def __call__(self,process,
                 pfTauLabelOld = cms.InputTag('pfRecoTauProducer'),
                 pfTauLabelNew = cms.InputTag('shrinkingConePFTauProducer')):
        self.addParameter('process',process, 'the process')
        self.addParameter('pfTauLabelOld',pfTauLabelOld, "label of the original particle flow tau collection as a string (default is 'pfRecoTauProducer')")
        self.addParameter('pfTauLabelNew',pfTauLabelNew, "label of the new particle flow tau collection as a string (default is 'shrinkingConePFTauProducer')")
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(pfTauLabelOld,InputTag),self.instanceError(pfTauLabelOld,'InputTag')
        assert isinstance(pfTauLabelNew,InputTag), self.instanceError(pfTauLabelNew,'InputTag')
        self.doCall() 
        
    def doCall(self):          
        process=self._parameters['process'].value
        pfTauLabelOld=self._parameters['pfTauLabelOld'].value
        pfTauLabelNew=self._parameters['pfTauLabelNew'].value
        process.disableRecording()
               
        _switchToPFTau(process, pfTauLabelOld, pfTauLabelNew, 'shrinkingConePFTau')
        #
        # CV: TaNC only trained for shrinkingCone PFTaus up to now,
        #     so need to add TaNC based discriminators
        #     specifically for that case here...
        #
        process.allLayer1Taus.tauIDSources = cms.PSet(
            leadingTrackFinding = cms.InputTag("shrinkingConePFTauDiscriminationByLeadingTrackFinding"),
            leadingTrackPtCut = cms.InputTag("shrinkingConePFTauDiscriminationByLeadingTrackPtCut"),
            trackIsolation = cms.InputTag("shrinkingConePFTauDiscriminationByTrackIsolation"),
            ecalIsolation = cms.InputTag("shrinkingConePFTauDiscriminationByECALIsolation"),
            byIsolation = cms.InputTag("shrinkingConePFTauDiscriminationByIsolation"),
            againstElectron = cms.InputTag("shrinkingConePFTauDiscriminationAgainstElectron"),
            againstMuon = cms.InputTag("shrinkingConePFTauDiscriminationAgainstMuon"),
            byTaNC = cms.InputTag("shrinkingConePFTauDiscriminationByTaNC"),
            byTaNCfrOnePercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrOnePercent"),
            byTaNCfrHalfPercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrHalfPercent"),
            byTaNCfrQuarterPercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrQuarterPercent"),
            byTaNCfrTenthPercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrTenthPercent")
            )
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)

switchToPFTauShrinkingCone=SwitchToPFTauShrinkingCone()



# function to switch to **any** PFTau collection
# It is just to make internal function accessible externally
class SwitchToAnyPFTau(ConfigToolBase):
    """
    """
    _label='SwitchToAnyPFTau'
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython = "\nswitchToAnyPFTau(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+ ", "
        dumpPython += str(self.getvalue('pfTauType'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
 
    def __call__(self,process,
                 pfTauLabelOld = cms.InputTag('pfRecoTauProducer'),
                 pfTauLabelNew = cms.InputTag('fixedConePFTauProducer'),
                 pfTauType='fixedConePFTau'):

        self.addParameter('process',process, 'the process')
        self.addParameter('pfTauLabelOld',pfTauLabelOld, "label of the original particle flow tau collection as a string (default is 'pfRecoTauProducer')")
        self.addParameter('pfTauLabelNew',pfTauLabelNew, "label of the new particle flow tau collection as a string (default is 'fixedConePFTauProducer')")
        self.addParameter('pfTauType',pfTauType, "")
        assert isinstance(process,Process),self.instanceError(process,'Process')
        assert isinstance(pfTauLabelOld,InputTag),self.instanceError(pfTauLabelOld,'InputTag')
        assert isinstance(pfTauLabelNew,InputTag), self.instanceError(pfTauLabelNew,'InputTag')
        assert isinstance(pfTauType,str), self.typeError(pfTauType,'string')
        self.doCall() 
        
    def doCall(self):           
        process=self._parameters['process'].value
        pfTauLabelOld=self._parameters['pfTauLabelOld'].value
        pfTauLabelNew=self._parameters['pfTauLabelNew'].value
        pfTauType=self._parameters['pfTauType'].value
        
        process.disableRecording()
        _switchToPFTau(process, pfTauLabelOld, pfTauLabelNew, pfTauType)
        process.enableRecording()
        action = Action(self._label,copy.copy(self._parameters),self)
        process.addAction(action)
        
switchToAnyPFTau=SwitchToAnyPFTau()
