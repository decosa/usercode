from FWCore.GuiBrowsers.ConfigToolBase import *
#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.coreTools import *

class RedoPFTauDiscriminators(ConfigToolBase):
    """
    """
    _label='RedoPFTauDiscriminators'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'oldPFTauLabel',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'newPFTauLabel',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'tauType','shrinkingConePFTau', ' ')
        self.addParameter(self._defaultParameters,'l0tauCollection',cms.InputTag('allLayer0Taus'), ' ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
        
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nredoPFTauDiscriminators(process, "
        dumpPython += str(self.getvalue('oldPFTauLabel'))+ ", "
        dumpPython += str(self.getvalue('newPFTauLabel'))+", "
        dumpPython += '"'+str(self.getvalue('tauType'))+'"'+", "
        dumpPython += str(self.getvalue('l0tauCollection'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
   
    def __call__(self,process,oldPFTauLabel=None,newPFTauLabel=None,tauType=None) :
        if  oldPFTauLabel is None:
            oldPFTauLabel=self._defaultParameters['oldPFTauLabel'].value
        if  newPFTauLabel is None:
            newPFTauLabel=self._defaultParameters['newPFTauLabel'].value
        if  tauType is None:
            tauType=self._defaultParameters['tauType'].value
        if  l0tauCollection is None:
            l0tauCollection=self._defaultParameters['l0tauCollection'].value     
            
        self.setParameter('oldPFTauLabel',oldPFTauLabel)
        self.setParameter('newPFTauLabel',newPFTauLabel)
        self.setParameter('tauType',tauType)
        self.setParameter('l0tauCollection',l0tauCollection)
        self.apply(process) 
        
    def toolCode(self, process):
                
        oldPFTauLabel =self._parameters['oldPFTauLabel'].value
        newPFTauLabel =self._parameters['newPFTauLabel'].value
        tauType =self._parameters['tauType'].value
        l0tauCollection =self._parameters['l0tauCollection'].value
       
        print 'Tau discriminators: ', oldPFTauLabel, '->', newPFTauLabel
        print 'Tau type: ', tauType
        tauSrc = 'PFTauProducer'

        tauDiscriminationSequence = process.patShrinkingConePFTauDiscrimination
        if tauType == 'fixedConeHighEffPFTau':
            tauDiscriminationSequence = process.patFixedConeHighEffPFTauDiscrimination
        elif tauType == 'fixedConePFTau':
            tauDiscriminationSequence = process.patFixedConePFTauDiscrimination
        elif tauType == 'shrinkingConePFTau':
            tauDiscriminationSequence = process.patShrinkingConePFTauDiscrimination
        elif tauType == 'caloTau':
            tauDiscriminationSequence = process.patCaloTauDiscrimination
            tauSrc = 'CaloTauProducer'

        moduleL0 =  getattr(process,l0tauCollection.moduleLabel)
        if (l0tauCollection.moduleLabel=="allLayer0Taus"):
            process.patDefaultSequence.replace(process.patCandidates, tauDiscriminationSequence + process.patCandidates)
        if (l0tauCollection.moduleLabel=='pfLayer0Taus'):         
            process.PF2PAT.replace(moduleL0, moduleL0+tauDiscriminationSequence)

        massSearchReplaceParam(tauDiscriminationSequence, tauSrc, oldPFTauLabel, newPFTauLabel)
      

redoPFTauDiscriminators= RedoPFTauDiscriminators()

class SwitchToCaloTau(ConfigToolBase):
    """ Switch to CaloTau collection
    """
    _label='SwitchToCaloTau'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'pfTauLabel',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'caloTauLabel',cms.InputTag('caloRecoTauProducer'), ' ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToCaloTau(process, "
        dumpPython += str(self.getvalue('pfTauLabel'))+ ", "
        dumpPython += str(self.getvalue('caloTauLabel'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,pfTauLabel=None,caloTauLabel=None) :
        if  pfTauLabel is None:
            pfTauLabel=self._defaultParameters['pfTauLabel'].value
        if  caloTauLabel is None:
            caloTauLabel=self._defaultParameters['caloTauLabel'].value
        self.setParameter('pfTauLabel',pfTauLabel)
        self.setParameter('caloTauLabel',caloTauLabel)
        self.apply(process) 
        
    def toolCode(self, process):
                
         pfTauLabel=self._parameters['pfTauLabel'].value
         caloTauLabel=self._parameters['caloTauLabel'].value
        
         process.tauMatch.src       = caloTauLabel
         process.tauGenJetMatch.src = caloTauLabel
         process.patTaus.tauSource = caloTauLabel
         process.patTaus.tauIDSources = cms.PSet(
             leadingTrackFinding = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackFinding"),
             leadingTrackPtCut   = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackPtCut"),
             byIsolation         = cms.InputTag("caloRecoTauDiscriminationByIsolation"),
             againstElectron     = cms.InputTag("caloRecoTauDiscriminationAgainstElectron"),  
             )
         process.patTaus.addDecayMode = False
         ## Isolation is somewhat an issue, so we start just by turning it off
         print "NO PF Isolation will be computed for CaloTau (this could be improved later)"
         process.patTaus.isolation   = cms.PSet()
         process.patTaus.isoDeposits = cms.PSet()
         process.patTaus.userIsolation = cms.PSet()
         ## adapt cleanPatTaus
         process.cleanPatTaus.preselection = 'tauID("leadingTrackFinding") > 0.5 & tauID("leadingTrackPtCut") > 0.5 & tauID("byIsolation") > 0.5 & tauID("againstElectron") > 0.5'

switchToCaloTau=SwitchToCaloTau()

# internal auxiliary function to switch to **any** PFTau collection
def _switchToPFTau(process,module, pfTauLabelOld, pfTauLabelNew, pfTauType):

    print ' Taus: ', pfTauLabelOld, '->', pfTauLabelNew
    mctaumatch      = getattr(process,module.genParticleMatch.moduleLabel)  
    mctaujetmatch   = getattr(process,module.genJetMatch.moduleLabel)
    tauisocand      = getattr(process,module.isoDeposits.pfAllParticles.moduleLabel)
    tauisopfch      = getattr(process,module.isoDeposits.pfChargedHadron.moduleLabel)
    tauisopfne      = getattr(process,module.isoDeposits.pfNeutralHadron.moduleLabel)
    tauisopfgam     = getattr(process,module.isoDeposits.pfGamma.moduleLabel)

    mctaumatch.src                      = pfTauLabelNew
    mctaujetmatch.src                   = pfTauLabelNew
    tauisocand.src                      = pfTauLabelNew
    tauisocand.ExtractorPSet.tauSource  = pfTauLabelNew
    tauisopfch.src                      = pfTauLabelNew
    tauisopfch.ExtractorPSet.tauSource  = pfTauLabelNew
    tauisopfne.src                      = pfTauLabelNew
    tauisopfne.ExtractorPSet.tauSource  = pfTauLabelNew
    tauisopfgam.src                     = pfTauLabelNew
    tauisopfgam.ExtractorPSet.tauSource = pfTauLabelNew
    module.tauSource = pfTauLabelNew

    module.tauIDSources = cms.PSet(
        leadingTrackFinding = cms.InputTag(pfTauType + "DiscriminationByLeadingTrackFinding"),
        leadingTrackPtCut = cms.InputTag(pfTauType + "DiscriminationByLeadingTrackPtCut"),
        leadingPionPtCut = cms.InputTag(pfTauType + "DiscriminationByLeadingPionPtCut"),
        trackIsolation = cms.InputTag(pfTauType + "DiscriminationByTrackIsolation"),
        trackIsolationUsingLeadingPion = cms.InputTag(pfTauType + "DiscriminationByTrackIsolationUsingLeadingPion"),
        ecalIsolation = cms.InputTag(pfTauType + "DiscriminationByECALIsolation"),
        ecalIsolationUsingLeadingPion = cms.InputTag(pfTauType + "DiscriminationByECALIsolationUsingLeadingPion"),
        byIsolation = cms.InputTag(pfTauType + "DiscriminationByIsolation"),
        byIsolationUsingLeadingPion = cms.InputTag(pfTauType + "DiscriminationByIsolationUsingLeadingPion"),
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
    module.decayModeSrc = cms.InputTag(pfTauType + "DecayModeProducer")


class SwitchToPFTauFixedCone(ConfigToolBase):
# switch to PFTau collection produced for fixed dR = 0.07 signal cone size
    """
    """
    _label='SwitchToPFTauFixedCone'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'pfTauLabelOld',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'pfTauLabelNew',cms.InputTag('fixedConePFTauProducer'), ' ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToPFTauFixedCone(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
       
    def __call__(self,process,pfTauLabelOld=None,pfTauLabelNew=None) :
        if  pfTauLabelOld is None:
            pfTauLabelOld=self._defaultParameters['pfTauLabelOld'].value
        if  pfTauLabelNew is None:
            pfTauLabelNew=self._defaultParameters['pfTauLabelNew'].value
        self.setParameter('pfTauLabelOld',pfTauLabel)
        self.setParameter('pfTauLabelNew',pfTauLabelNew)
        self.apply(process) 
        
    def toolCode(self, process):
                
         pfTauLabelOld=self._parameters['pfTauLabelOld'].value
         pfTauLabelNew=self._parameters['pfTauLabelNew'].value
            
         _switchToPFTau(process,module, pfTauLabelOld, pfTauLabelNew, 'fixedConePFTau')
         #
         # CV: PFTauDecayMode objects produced only for shrinking cone reco::PFTaus in
         #     RecoTauTag/Configuration global_PFTau_22X_V00-02-01 and CMSSW_3_1_x tags,
         #     so need to disable embedding of PFTauDecayMode information into pat::Tau for now...
         #
         module.addDecayMode = cms.bool(False)
    
switchToPFTauFixedCone=SwitchToPFTauFixedCone()       

class SwitchToPFTauFixedConeHighEff(ConfigToolBase):
    # switch to PFTau collection produced for fixed dR = 0.15 signal cone size
    """
    """
    _label='SwitchToPFTauFixedConeHighEff'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'pfTauLabelOld',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'pfTauLabelNew',cms.InputTag('fixedConeHighEffPFTauProducer'), ' ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""  
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToPFTauFixedConeHighEff(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
           
    def __call__(self,process,pfTauLabelOld=None,pfTauLabelNew=None) :
        if  pfTauLabelOld is None:
            pfTauLabelOld=self._defaultParameters['pfTauLabelOld'].value
        if  pfTauLabelNew is None:
            pfTauLabelNew=self._defaultParameters['pfTauLabelNew'].value
        self.setParameter('pfTauLabelOld',pfTauLabel)
        self.setParameter('pfTauLabelNew',pfTauLabelNew)
        self.apply(process) 
        
    def toolCode(self, process):
                
         pfTauLabelOld=self._parameters['pfTauLabelOld'].value
         pfTauLabelNew=self._parameters['pfTauLabelNew'].value

         _switchToPFTau(process, module,pfTauLabelOld, pfTauLabelNew, 'fixedConeHighEffPFTau')
         #
         # CV: PFTauDecayMode objects produced only for shrinking cone reco::PFTaus in
         #     RecoTauTag/Configuration global_PFTau_22X_V00-02-01 and CMSSW_3_1_x tags,
         #     so need to disable embedding of PFTauDecayMode information into pat::Tau for now...
         #
         module.addDecayMode = cms.bool(False)
       

switchToPFTauFixedConeHighEff=SwitchToPFTauFixedConeHighEff()

class SwitchToPFTauShrinkingCone(ConfigToolBase):
# switch to PFTau collection produced for shrinking signal cone of size dR = 5.0/Et(PFTau)
    """
    """
    _label='SwitchToPFTauShrinkingCone'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'pfTauLabelOld',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'pfTauLabelNew',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToPFTauShrinkingCone(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
           
    def __call__(self,process,pfTauLabelOld=None,pfTauLabelNew=None) :
        if  pfTauLabelOld is None:
            pfTauLabelOld=self._defaultParameters['pfTauLabelOld'].value
        if  pfTauLabelNew is None:
            pfTauLabelNew=self._defaultParameters['pfTauLabelNew'].value
        self.setParameter('pfTauLabelOld',pfTauLabel)
        self.setParameter('pfTauLabelNew',pfTauLabelNew)
        self.apply(process) 
        
    def toolCode(self, process):
                
         pfTauLabelOld=self._parameters['pfTauLabelOld'].value
         pfTauLabelNew=self._parameters['pfTauLabelNew'].value

         _switchToPFTau(process,module, pfTauLabelOld, pfTauLabelNew, 'shrinkingConePFTau')
         #
         # CV: TaNC only trained for shrinkingCone PFTaus up to now,
         #     so need to add TaNC based discriminators
         #     specifically for that case here...
         #
         module.tauIDSources = cms.PSet(
             leadingTrackFinding = cms.InputTag("shrinkingConePFTauDiscriminationByLeadingTrackFinding"),
             leadingTrackPtCut = cms.InputTag("shrinkingConePFTauDiscriminationByLeadingTrackPtCut"),
             leadingPionPtCut = cms.InputTag("shrinkingConePFTauDiscriminationByLeadingPionPtCut"),
             trackIsolation = cms.InputTag("shrinkingConePFTauDiscriminationByTrackIsolation"),
             trackIsolationUsingLeadingPion = cms.InputTag("shrinkingConePFTauDiscriminationByTrackIsolationUsingLeadingPion"),
             ecalIsolation = cms.InputTag("shrinkingConePFTauDiscriminationByECALIsolation"),
             ecalIsolationUsingLeadingPion = cms.InputTag("shrinkingConePFTauDiscriminationByECALIsolationUsingLeadingPion"),
             byIsolation = cms.InputTag("shrinkingConePFTauDiscriminationByIsolation"),
             byIsolationUsingLeadingPion = cms.InputTag("shrinkingConePFTauDiscriminationByIsolationUsingLeadingPion"),
             againstElectron = cms.InputTag("shrinkingConePFTauDiscriminationAgainstElectron"),
             againstMuon = cms.InputTag("shrinkingConePFTauDiscriminationAgainstMuon"),
             byTaNC = cms.InputTag("shrinkingConePFTauDiscriminationByTaNC"),
             byTaNCfrOnePercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrOnePercent"),
             byTaNCfrHalfPercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrHalfPercent"),
             byTaNCfrQuarterPercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrQuarterPercent"),
             byTaNCfrTenthPercent = cms.InputTag("shrinkingConePFTauDiscriminationByTaNCfrTenthPercent")
             )
         
switchToPFTauShrinkingCone=SwitchToPFTauShrinkingCone()

class SwitchToAnyPFTau(ConfigToolBase):    
# function to switch to **any** PFTau collection
# It is just to make internal function accessible externally

    """
    """
    _label='SwitchToAnyPFTau'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'pfTauLabelOld',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'pfTauLabelNew',cms.InputTag('shrinkingConePFTauProducer'), ' ')
        self.addParameter(self._defaultParameters,'pfTauType','shrinkingConePFTau', ' ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):  
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.jetTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToAnyPFTau(process, "
        dumpPython += str(self.getvalue('pfTauLabelOld'))+ ", "
        dumpPython += str(self.getvalue('pfTauLabelNew'))+ ", "
        dumpPython += '"'+str(self.getvalue('pfTauType'))+ '"'+')'+'\n'
        return (dumpPythonImport,dumpPython)
            
    def __call__(self,process,pfTauLabelOld=None,pfTauLabelNew=None,pfTauType=None) :
        if  pfTauLabelOld is None:
            pfTauLabelOld=self._defaultParameters['pfTauLabelOld'].value
        if  pfTauLabelNew is None:
            pfTauLabelNew=self._defaultParameters['pfTauLabelNew'].value
        if  pfTauType  is None:
            pfTauType=self._defaultParameters['pfTauType'].value

        self.setParameter('pfTauLabelOld',pfTauLabelOld)
        self.setParameter('pfTauLabelNew',pfTauLabelNew)
        self.setParameter('pfTauType',pfTauType)
        self.apply(process) 
        
    def toolCode(self, process):
                
         pfTauLabelOld=self._parameters['pfTauLabelOld'].value
         pfTauLabelNew=self._parameters['pfTauLabelNew'].value
         pfTauType =self._parameters['pfTauType'].value

         _switchToPFTau(process,module, pfTauLabelOld, pfTauLabelNew, pfTauType)
            

switchToAnyPFTau=SwitchToAnyPFTau()
