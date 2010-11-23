import FWCore.ParameterSet.Config as cms
import copy



baseKinematics = (
    cms.PSet(
    tag = cms.untracked.string("Mass"),
    quantity = cms.untracked.string("mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    )
    )


zllEdmNtuple = cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("zll"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string("zll"),
    eventInfo=cms.untracked.bool(True),
    variables = cms.VPSet(

    ### z daughters variables
    
    ## pt
    cms.PSet(
    tag = cms.untracked.string("DauMinPt"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.pt : daughter(1).masterClone.pt ")
    ),
    cms.PSet(
    tag = cms.untracked.string("DauMaxPt"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt > daughter(1).masterClone.pt ? daughter(0).masterClone.pt : daughter(1).masterClone.pt ")
    ),
    ## eta
    cms.PSet(
    tag = cms.untracked.string("DauMinEta"),
    quantity = cms.untracked.string("? daughter(0).masterClone.eta < daughter(1).masterClone.eta ? daughter(0).masterClone.eta : daughter(1).masterClone.eta ")
    ),
    cms.PSet(
    tag = cms.untracked.string("DauMaxEta"),
    quantity = cms.untracked.string("? daughter(0).masterClone.eta > daughter(1).masterClone.eta ? daughter(0).masterClone.eta : daughter(1).masterClone.eta ")
    ),
    ## phi
    cms.PSet(
    tag = cms.untracked.string("DauMinPhi"),
    quantity = cms.untracked.string("? daughter(0).masterClone.phi < daughter(1).masterClone.phi ? daughter(0).masterClone.phi :daughter(1).masterClone.phi ")
    ),
    cms.PSet(
    tag = cms.untracked.string("DauMaxPhi"),
    quantity = cms.untracked.string("? daughter(0).masterClone.phi > daughter(1).masterClone.phi ? daughter(0).masterClone.phi :daughter(1).masterClone.phi ")
    ),
    )
    )


higgs = (
    cms.PSet(
    tag = cms.untracked.string("AzimuthalAngle"),
    quantity = cms.untracked.string("userFloat('azimuthalAngle')")
    ),
    cms.PSet(
    tag = cms.untracked.string("jminbmatch"),
    quantity = cms.untracked.string("userFloat('jminbmatch')")
    ),
    cms.PSet(
    tag = cms.untracked.string("jmincmatch"),
    quantity = cms.untracked.string("userFloat('jmincmatch')")
    ),
    cms.PSet(
    tag = cms.untracked.string("jmaxbmatch"),
    quantity = cms.untracked.string("userFloat('jmaxbmatch')")
    ),
    cms.PSet(
    tag = cms.untracked.string("jmaxcmatch"),
    quantity = cms.untracked.string("userFloat('jmaxcmatch')")
    ),
    cms.PSet(
    tag = cms.untracked.string("zzdPhi"),
    quantity = cms.untracked.string("userFloat('zzdPhi')")
    ),
    cms.PSet(
    tag = cms.untracked.string("zzdEta"),
    quantity = cms.untracked.string("userFloat('zzdEta')")
    ),
    cms.PSet(
    tag = cms.untracked.string("zzdr"),
    quantity = cms.untracked.string("userFloat('zzdr')")
    ),
    cms.PSet(
    tag = cms.untracked.string("lldPhi"),
    quantity = cms.untracked.string("userFloat('lldPhi')")
    ),
    cms.PSet(
    tag = cms.untracked.string("lldEta"),
    quantity = cms.untracked.string("userFloat('lldEta')")
    ),
    cms.PSet(
    tag = cms.untracked.string("lldr"),
    quantity = cms.untracked.string("userFloat('lldr')")
    ),
    )

###  zjj bDiscriminator variables

zjj = (
    cms.PSet(
    tag = cms.untracked.string("JetMinCSV"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") :daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxCSV"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") :daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinCSVMVA"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") :daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxCSVMVA"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") :daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinJProb"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") :daughter(1).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxJProb"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") :daughter(0).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinJbProb"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") :daughter(1).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxJbProb"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") :daughter(0).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinSSVHE"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") :daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxSSVHE"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") :daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinSSVHP"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") :daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxSSVHP"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") :daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinElPt"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") :daughter(1).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxElPt"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") :daughter(0).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") ")
    ),
        cms.PSet(
    tag = cms.untracked.string("JetMinElIp"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") :daughter(1).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxElIp"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") :daughter(0).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") ")
    ),
        cms.PSet(
    tag = cms.untracked.string("JetMinMu"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"softMuonBJetTags\") :daughter(1).masterClone.bDiscriminator(\"softMuonBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxMu"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"softMuonBJetTags\") :daughter(0).masterClone.bDiscriminator(\"softMuonBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinMuPt"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"softMuonPtBJetTags\") :daughter(1).masterClone.bDiscriminator(\"softMuonPtBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxMuPt"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"softMuonPtBJetTags\") :daughter(0).masterClone.bDiscriminator(\"softMuonPtBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinMuIp"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") :daughter(1).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxMuIp"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") :daughter(0).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinTKHE"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") :daughter(1).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxTKHE"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") :daughter(0).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinTKHP"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(0).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") :daughter(1).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxTKHP"),
    quantity = cms.untracked.string("? daughter(0).masterClone.pt < daughter(1).masterClone.pt ? daughter(1).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") :daughter(0).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") ")
    ),


##     ## jET ID
    
##     cms.PSet(
##     tag = cms.untracked.string("JetMinID"),
##     quantity = cms.untracked.string("? (daughter(0).masterClone.pt < daughter(1).masterClone.pt) && ((daughter(0).masterClone.neutralEmEnergy/daughter(0).masterClone.energy ) < 1.00) && ((daughter(0).masterClone.chargedEmEnergy/daughter(0).masterClone.energy)<1.00) && ((daughter(0).masterClone.chargedHadronEnergy/daughter(0).masterClone.energy)>0) ? true : false")
##     ),
##     cms.PSet(
##     tag = cms.untracked.string("JetMaxID"),
##     quantity = cms.untracked.string("? (daughter(0).masterClone.pt < daughter(1).masterClone.pt) && ? daughter(1).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") :daughter(0).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") ")
##     ),


    )


zllEdmNtuple.variables += baseKinematics

Higgs2e2bEdmNtuple = copy.deepcopy(zllEdmNtuple)
Higgs2e2bEdmNtuple.variables += higgs
Higgs2e2bEdmNtuple.src = cms.InputTag("hzzeejj:h")
Higgs2e2bEdmNtuple.prefix = cms.untracked.string("elHiggs")

Higgs2mu2bEdmNtuple = copy.deepcopy(Higgs2e2bEdmNtuple)
Higgs2mu2bEdmNtuple.src = cms.InputTag("hzzmmjj:h")
Higgs2mu2bEdmNtuple.prefix = cms.untracked.string("muHiggs")


zeeEdmNtuple = copy.deepcopy(zllEdmNtuple)
zeeEdmNtuple.src = cms.InputTag("zee")
zeeEdmNtuple.prefix = cms.untracked.string("zee")

zmmEdmNtuple = copy.deepcopy(zllEdmNtuple)
zmmEdmNtuple.src = cms.InputTag("zmm")
zmmEdmNtuple.prefix = cms.untracked.string("zmm")

zjjEdmNtuple = copy.deepcopy(zllEdmNtuple)
zjjEdmNtuple.src = cms.InputTag("zjj")
zjjEdmNtuple.prefix = cms.untracked.string("zjj")
zjjEdmNtuple.variables += zjj




edmNtuplesOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('Higgs2l2bEdmNtuples.root'),
    outputCommands = cms.untracked.vstring(
    "drop *",
    "keep *_Higgs2e2bEdmNtuple_*_*",
    "keep *_Higgs2mu2bEdmNtuple_*_*",
    "keep *_zmmEdmNtuple_*_*",
    "keep *_zeeEdmNtuple_*_*",
    "keep *_zjjEdmNtuple_*_*",
    "keep *_hzzeejj_met_*",
    "keep *_hzzeejj_metSig_*",
    "keep *_hzzeejj_metPhi_*"
    
    )
    )
