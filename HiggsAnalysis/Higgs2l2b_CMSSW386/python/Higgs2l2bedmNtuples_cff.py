import FWCore.ParameterSet.Config as cms
import copy

### HIGGS variables


higgs =  cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("h2l2b"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string("H"),
    eventInfo=cms.untracked.bool(True),
    variables = cms.VPSet(
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
    ),
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
    )

### Zll variables

zll = (

    cms.PSet(
    tag = cms.untracked.string("zllMass"),
    quantity = cms.untracked.string("daughter(0).mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("zllPt"),
    quantity = cms.untracked.string("daughter(0).pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("zllEta"),
    quantity = cms.untracked.string("daughter(0).eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("zllPhi"),
    quantity = cms.untracked.string("daughter(0).phi")
    ),
    ## pt
    cms.PSet(
    tag = cms.untracked.string("LeptDauMinPt"),
    quantity = cms.untracked.string("?daughter(0).daughter(0).pt <daughter(0).daughter(1).pt ?daughter(0).daughter(0).pt :daughter(0).daughter(1).pt ")
    ),
    cms.PSet(
    tag = cms.untracked.string("LeptDauMaxPt"),
    quantity = cms.untracked.string("?daughter(0).daughter(0).pt >daughter(0).daughter(1).pt ?daughter(0).daughter(0).pt :daughter(0).daughter(1).pt ")
    ),
    ## eta
    cms.PSet(
    tag = cms.untracked.string("LeptDauMinEta"),
    quantity = cms.untracked.string("?daughter(0).daughter(0).eta <daughter(0).daughter(1).eta ?daughter(0).daughter(0).eta :daughter(0).daughter(1).eta ")
    ),
    cms.PSet(
    tag = cms.untracked.string("LeptDauMaxEta"),
    quantity = cms.untracked.string("?daughter(0).daughter(0).eta >daughter(0).daughter(1).eta ?daughter(0).daughter(0).eta :daughter(0).daughter(1).eta ")
    ),
    ## phi
    cms.PSet(
    tag = cms.untracked.string("LeptDauMinPhi"),
    quantity = cms.untracked.string("?daughter(0).daughter(0).phi <daughter(0).daughter(1).phi ?daughter(0).daughter(0).phi :daughter(1).phi ")
    ),
    cms.PSet(
    tag = cms.untracked.string("LeptDauMaxPhi"),
    quantity = cms.untracked.string("?daughter(0).daughter(0).phi >daughter(0).daughter(1).phi ?daughter(0).daughter(0).phi :daughter(1).phi ")
    )
    )


###  zjj standard and bDiscriminator variables

zjj = (
    
    cms.PSet(
    tag = cms.untracked.string("zjjMass"),
    quantity = cms.untracked.string("daughter(1).mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("zjjPt"),
    quantity = cms.untracked.string("daughter(1).pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("zjjEta"),
    quantity = cms.untracked.string("daughter(1).eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("zjjPhi"),
    quantity = cms.untracked.string("daughter(1).phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinCSV"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxCSV"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinCSVMVA"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxCSVMVA"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"combinedSecondaryVertexMVABJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinJProb"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxJProb"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"jetBProbabilityBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinJbProb"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxJbProb"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"jetBProbabilityJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinSSVHE"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxSSVHE"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinSSVHP"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxSSVHP"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"simpleSecondaryVertexHighPurBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinElPt"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxElPt"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"softElectronByPtBJetTags\") ")
    ),
        cms.PSet(
    tag = cms.untracked.string("JetMinElIp"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxElIp"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"softElectronByIP3BJetTags\") ")
    ),
        cms.PSet(
    tag = cms.untracked.string("JetMinMu"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"softMuonBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"softMuonBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxMu"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"softMuonBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"softMuonBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinMuPt"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"softMuonPtBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"softMuonPtBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxMuPt"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"softMuonPtBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"softMuonPtBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinMuIp"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxMuIp"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"softMuonIP3BJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinTKHE"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxTKHE"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"trackCountingHighEffBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMinTKHP"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(0).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") :daughter(1).daughter(1).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") ")
    ),
    cms.PSet(
    tag = cms.untracked.string("JetMaxTKHP"),
    quantity = cms.untracked.string("? daughter(1).daughter(0).masterClone.pt < daughter(1).daughter(1).masterClone.pt ? daughter(1).daughter(1).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") :daughter(1).daughter(0).masterClone.bDiscriminator(\"trackCountingHighPurBJetTags\") ")
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


## zll.variables += baseKinematics

Higgs2e2bEdmNtuple = copy.deepcopy(higgs)
Higgs2e2bEdmNtuple.variables += zll
Higgs2e2bEdmNtuple.variables += zjj
Higgs2e2bEdmNtuple.src = cms.InputTag("hzzeejj:h")
Higgs2e2bEdmNtuple.prefix = cms.untracked.string("elHiggs")


Higgs2mu2bEdmNtuple = copy.deepcopy(Higgs2e2bEdmNtuple)
Higgs2mu2bEdmNtuple.src = cms.InputTag("hzzmmjj:h")
Higgs2mu2bEdmNtuple.prefix = cms.untracked.string("muHiggs")


edmNtuplesOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('Higgs2l2bEdmNtuples.root'),
    outputCommands = cms.untracked.vstring(
    "drop *",
    "keep *_Higgs2e2bEdmNtuple_*_*",
    "keep *_Higgs2mu2bEdmNtuple_*_*",
    "keep *_hzzeejj_met_*",
    "keep *_hzzeejj_metSig_*",
    "keep *_hzzeejj_metPhi_*"
    
    )
    )
