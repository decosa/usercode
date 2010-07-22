import FWCore.ParameterSet.Config as cms

process = cms.Process("CMGTOPMICROTUPLE")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger = cms.Service(
    "MessageLogger",
    destinations   = cms.untracked.vstring(
#    'detailedInfo'
    'critical'
#    ,'debugAll'
    ,'cout'
    )
    ,critical       = cms.untracked.PSet(
    threshold = cms.untracked.string('ERROR')
    )
#    ,detailedInfo   = cms.untracked.PSet(
#    threshold = cms.untracked.string('INFO')
#    )
#    ,debugAll       = cms.untracked.PSet(
#    threshold = cms.untracked.string('DEBUG')
#    )
#    ,debugModules = cms.untracked.vstring('*')
#    ,suppressDebug = cms.untracked.vstring('RFIOFileDebug')
    ,messageSummaryToJobReport = cms.untracked.bool(True)
    )

    

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring
    (
    #"file:TTbar_TopPAT.root"
    "rfio:/castor/cern.ch/user/r/rovere/cmst3/TTbarJets-madgraph__Spring10-START3X_V26_S09-v1__GEN-SIM-RECO_3/CMGPAT/TTbar_TopPAT_12_1.root"
    )
    )

# Load input files from external python

# process.load("CMGEDMMicroTuple.CMGEDMMicroTuple.inputFiles")

# process.source = cms.Source("EmptySource")

# Run Filter on top of FlavorHistory Product
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")
#make sure we do not filter!!!
process.flavorHistoryFilter.pathToSelect = cms.int32(-1) # do not select any path, always return true

#############################################
### **** labels have to be changed!! **** ###
#############################################



## process.CMGMicroTuple = cms.EDProducer(
##     'CMGEDMMicroTuple'
##     ,electronSrc = cms.untracked.InputTag("selectedLayer1Electrons")
##     ,muonSrc = cms.untracked.InputTag("selectedLayer1Muons")
##     ,calojetSrc  = cms.untracked.InputTag("selectedLayer1Jets")
##     ,calometSrc  = cms.untracked.InputTag("layer1METs")
##     ,TQAFGenSrc  = cms.untracked.InputTag("genEvt")
##     ,pfjetSrc    = cms.untracked.InputTag("sisCone5PFJets")
##     ,pfmetSrc    = cms.untracked.InputTag("pfMet")
##     ,genjetSrc    = cms.untracked.InputTag("antikt5GenJets")
##     ,genmetSrc    = cms.untracked.InputTag("genMetCalo")
##     )


### **** MUONS **** ###


process.CMGMicroTupleMuons = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("selectedPatMuons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("Mu"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("charge"),
    quantity = cms.untracked.string("charge")
    ),
    cms.PSet(
    tag = cms.untracked.string("eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("IsIsoValid"),
    quantity = cms.untracked.string("isIsolationValid")
    ),
    cms.PSet(
    tag = cms.untracked.string("ecaliso"),
    quantity = cms.untracked.string("ecalIso")
    ),
    cms.PSet(
    tag = cms.untracked.string("hcaliso"),
    quantity = cms.untracked.string("hcalIso")
    ),
    cms.PSet(
    tag = cms.untracked.string("trackiso"),
    quantity = cms.untracked.string("trackIso")
    ),
    cms.PSet(
    tag = cms.untracked.string("type"),
    quantity = cms.untracked.string("type")
    ),
    cms.PSet(
    tag = cms.untracked.string("isGlobalMuon"),
    quantity = cms.untracked.string("isGlobalMuon")
    ),
    cms.PSet(
    tag = cms.untracked.string("isTrackerMuon"),
    quantity = cms.untracked.string("isTrackerMuon")
    ),
    cms.PSet(
    tag = cms.untracked.string("isStandAloneMuon"),
    quantity = cms.untracked.string("isStandAloneMuon")
    ),
    cms.PSet(
    tag = cms.untracked.string("isGlobalMuonPromptTight"),
    quantity = cms.untracked.string("muonID(\"GlobalMuonPromptTight\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalIsoCandEnergy"),
    quantity = cms.untracked.string("isolationR03.emVetoEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("hcalIsoCandEnergy"),
    quantity = cms.untracked.string("isolationR03.hadVetoEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("dB"),
    quantity = cms.untracked.string("dB")
    ),
    cms.PSet(
    tag = cms.untracked.string("globalTrackValidMuonHits"),
    quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.hitPattern.numberOfValidMuonHits:-1")
    ),
    cms.PSet(
    tag = cms.untracked.string("globalTrackChi2"),
    quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.chi2:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("globalTrackNdof"),
    quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.ndof:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("globalTrackDxy"),
    quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.dxy:100000")
    ),

### need producer for this variable  ###
##     cms.PSet(
##     tag = cms.untracked.string("globalTrackDxyPV"),
##     quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.dxy(pvs.op):-1")
##     ),
##     cms.PSet(
##     tag = cms.untracked.string("globalTrackDxyBS"),
##     quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.hitPattern.numberOfValidMuonHits:-1")
##     ),
    
    cms.PSet(
    tag = cms.untracked.string("globalTrackDxyError"),
    quantity = cms.untracked.string("?globalTrack.isAvailable?globalTrack.dxyError:-1")
    ),
    
    cms.PSet(
    tag = cms.untracked.string("innerTrackValidNumHits"),
    quantity = cms.untracked.string("?innerTrack.isAvailable?innerTrack.hitPattern.numberOfValidMuonHits:-1")
    ),
    cms.PSet(
    tag = cms.untracked.string("innerTrackChi2"),
    quantity = cms.untracked.string("?innerTrack.isAvailable?innerTrack.chi2:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("innerTrackNdof"),
    quantity = cms.untracked.string("?innerTrack.isAvailable?innerTrack.ndof:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("innerTrackDxy"),
    quantity = cms.untracked.string("?innerTrack.isAvailable?innerTrack.dxy:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("innerTrackDxyError"),
    quantity = cms.untracked.string("?innerTrack.isAvailable?innerTrack.dxyError:-1")
    ),

   
    cms.PSet(
    tag = cms.untracked.string("outerTrackValidNumHits"),
    quantity = cms.untracked.string("?outerTrack.isAvailable?outerTrack.hitPattern.numberOfValidMuonHits:-1")
    ),
    cms.PSet(
    tag = cms.untracked.string("outerTrackChi2"),
    quantity = cms.untracked.string("?outerTrack.isAvailable?outerTrack.chi2:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("outerTrackNdof"),
    quantity = cms.untracked.string("?outerTrack.isAvailable?outerTrack.ndof:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("outerTrackDxy"),
    quantity = cms.untracked.string("?outerTrack.isAvailable?outerTrack.dxy:100000")
    ),
    cms.PSet(
    tag = cms.untracked.string("outerTrackDxyError"),
    quantity = cms.untracked.string("?outerTrack.isAvailable?outerTrack.dxyError:-1")
    ),
   
   
    )
    )


### **** ELECTRONS **** ###

process.CMGMicroTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("selectedPatElectrons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("E"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("charge"),
    quantity = cms.untracked.string("charge")
    ),
    cms.PSet(
    tag = cms.untracked.string("eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("isEB"),
    quantity = cms.untracked.string("isEB")
    ),
    cms.PSet(
    tag = cms.untracked.string("isEE"),
    quantity = cms.untracked.string("isEE")
    ),
    cms.PSet(
    tag = cms.untracked.string("ecaliso"),
    quantity = cms.untracked.string("dr03EcalRecHitSumEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("hcaliso"),
    quantity = cms.untracked.string("dr03HcalTowerSumEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("trackiso"),
    quantity = cms.untracked.string("dr03TkSumPt")
    ),
    cms.PSet(
    tag = cms.untracked.string("classification"),
    quantity = cms.untracked.string("classification")
    ),
    cms.PSet(
    tag = cms.untracked.string("eidRobustTight"),
    quantity = cms.untracked.string("?isElectronIDAvailable(\"eidRobustTight\")?electronID(\"eidRobustTight\"):-1")
    ),
    cms.PSet(
    tag = cms.untracked.string("sihih"),
    quantity = cms.untracked.string("sigmaIetaIeta")
    ),
    cms.PSet(
    tag = cms.untracked.string("dfi"),
    quantity = cms.untracked.string("deltaPhiSuperClusterTrackAtVtx")
    ),
    cms.PSet(
    tag = cms.untracked.string("dhi"),
    quantity = cms.untracked.string("deltaEtaSuperClusterTrackAtVtx")
    ),
    cms.PSet(
    tag = cms.untracked.string("hoe"),
    quantity = cms.untracked.string("hcalOverEcal")
    ),
    )
    )


### **** CALOJETS **** ###


process.CMGMicroTupleCaloJets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("selectedPatJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("CaloJet"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("mass"),
    quantity = cms.untracked.string("charge")
    ),
    cms.PSet(
    tag = cms.untracked.string("eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("EMF"),
    quantity = cms.untracked.string("?isCaloJet?emEnergyFraction:-1.")
    ),
    cms.PSet(
    tag = cms.untracked.string("HadF"),
    quantity = cms.untracked.string("?isCaloJet?energyFractionHadronic:-1.")
    ),
    cms.PSet(
    tag = cms.untracked.string("n90"),
    quantity = cms.untracked.string("jetID.n90Hits")
    ),
    cms.PSet(
    tag = cms.untracked.string("fhpd"),
    quantity = cms.untracked.string("jetID.fHPD")
    ),
    cms.PSet(
    tag = cms.untracked.string("origpt"),
    quantity = cms.untracked.string("originalObject.pt")
    ),
##     cms.PSet(
##     tag = cms.untracked.string("genmass"),
##     quantity = cms.untracked.string("?1?genJet.mass:-10000")
##     ),
##     cms.PSet(
##     tag = cms.untracked.string("geneta"),
##     quantity = cms.untracked.string("?genJet?genJet.eta:-10000")
##     ),
##     cms.PSet(
##     tag = cms.untracked.string("genphi"),
##     quantity = cms.untracked.string("?genJet?genJet.phi:-10000")
##     ),
##     cms.PSet(
##     tag = cms.untracked.string("genpt"),
##     quantity = cms.untracked.string("?genJet?genJet.pt:-10000")
##     ),
    cms.PSet(
    tag = cms.untracked.string("softElectronBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"softElectronBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("softMuonBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"softMuonBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("softMuonNoIPBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"softMuonNOIPBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("jetProbabilityBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"jetProbablityBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("jetBProbabilityBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"jetBProbabilitBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("ttrackCountingHighPurBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"trackCountingHighPurBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("ttrackCountingHighEffBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"trackCountingHighEffBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("impactParameterMVABJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"impactParameterMVABJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("simpleSecondaryVertexBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"simpleSecondaryVertexBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("combinedSecondaryVertexBJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"combinedSecondaryVertexBJetTags\")")
    ),
    cms.PSet(
    tag = cms.untracked.string("combinedSecondaryVertexMVABJetTag"),
    quantity = cms.untracked.string("bDiscriminator(\"combinedSecondaryVertexMVABJetTags\")")
    ),    
    
    )
    )



### **** PFJETS **** ###


process.CMGMicroTuplePFJets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("ak5PFJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("PFJet"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("mass"),
    quantity = cms.untracked.string("mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("CEMF"),
    quantity = cms.untracked.string("chargedEmEnergyFraction")
    ),
    cms.PSet(
    tag = cms.untracked.string("NEMF"),
    quantity = cms.untracked.string("neutralEmEnergyFraction")
    ),
    cms.PSet(
    tag = cms.untracked.string("NHadF"),
    quantity = cms.untracked.string("neutralHadronEnergyFraction")
    ),
    cms.PSet(
    tag = cms.untracked.string("CHadF"),
    quantity = cms.untracked.string("chargedHadronEnergyFraction")
    ),
    cms.PSet(
    tag = cms.untracked.string("ChargedMu1"),
    quantity = cms.untracked.string("chargedMultiplicity")
    ),
    cms.PSet(
    tag = cms.untracked.string("NeutralMu1"),
    quantity = cms.untracked.string("neutralMultiplicity")
    ),
    cms.PSet(
    tag = cms.untracked.string("MuonMu1"),
    quantity = cms.untracked.string("muonMultiplicity")
    ),
    cms.PSet(
    tag = cms.untracked.string("NumObj"),
    quantity = cms.untracked.string("getPFConstituents.size")
    ),
    )
    )


### **** CALOMET **** ###


process.CMGMicroTupleCaloMets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("patMETs"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("CaloMet"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("ptUnCorr"),
    quantity = cms.untracked.string("uncorrectedPt")
    ),
    
    )
    )


### **** TQAF **** ###


process.CMGMicroTupleTQAF = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("genEvt"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("TQAFGen"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("isFullHadronic"),
    quantity = cms.untracked.string("isFullHadronic")
    ),
    cms.PSet(
    tag = cms.untracked.string("isFullLeptonic"),
    quantity = cms.untracked.string("isFullLeptonic")
    ),
    cms.PSet(
    tag = cms.untracked.string("isSemiLeptonic"),
    quantity = cms.untracked.string("isSemiLeptonic")
    ),
    cms.PSet(
    tag = cms.untracked.string("semiLeptonicChannel"),
    quantity = cms.untracked.string("semiLeptonicChannel")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonEta"),
    quantity = cms.untracked.string("?isSemiLeptonic?singleLepton.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonPhi"),
    quantity = cms.untracked.string("?isSemiLeptonic?singleLepton.phi:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonPt"),
    quantity = cms.untracked.string("?isSemiLeptonic?singleLepton.pt:-10000")
    ),

### hadronically decaying top ###
    
    cms.PSet(
    tag = cms.untracked.string("hadronicTopEta"),
    quantity = cms.untracked.string("?isSemiLeptonic?hadronicDecayTop.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("hadronicTopPhi"),
    quantity = cms.untracked.string("?isSemiLeptonic?hadronicDecayTop.phi:-10000")
    ),    cms.PSet(
    tag = cms.untracked.string("hadronicTopPt"),
    quantity = cms.untracked.string("?isSemiLeptonic?hadronicDecayTop.pt:-10000")
    ),

### leptonically decaying top ###
    
    cms.PSet(
    tag = cms.untracked.string("leptonicTopEta"),
    quantity = cms.untracked.string("?isSemiLeptonic?leptonicDecayTop.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonicTopPhi"),
    quantity = cms.untracked.string("?isSemiLeptonic?leptonicDecayTop.phi:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonicTopPt"),
    quantity = cms.untracked.string("?isSemiLeptonic?leptonicDecayTop.pt:-10000")
    ),

### hadronically decaying W ###
    
    cms.PSet(
    tag = cms.untracked.string("hadronicWEta"),
    quantity = cms.untracked.string("?isSemiLeptonic?hadronicDecayW.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("hadronicWPhi"),
    quantity = cms.untracked.string("?isSemiLeptonic?hadronicDecayW.phi:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("hadronicWPt"),
    quantity = cms.untracked.string("?isSemiLeptonic?hadronicDecayW.pt:-10000")
    ),

### leptonically decaying W ###
    
    cms.PSet(
    tag = cms.untracked.string("leptonicWEta"),
    quantity = cms.untracked.string("?isSemiLeptonic?leptonicDecayW.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonicWPhi"),
    quantity = cms.untracked.string("?isSemiLeptonic?leptonicDecayW.phi:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonicWPt"),
    quantity = cms.untracked.string("?isSemiLeptonic?leptonicDecayW.pt:-10000")
    ),

### b on the hadron side ###
    
    cms.PSet(
    tag = cms.untracked.string("hadronicBEta"),
    quantity = cms.untracked.string("?hadronicDecayB?hadronicDecayB.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("hadronicBPhi"),
    quantity = cms.untracked.string("?hadronicDecayB?hadronicDecayB.phi:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("hadronicBPt"),
    quantity = cms.untracked.string("?hadronicDecayB?hadronicDecayB.pt:-10000")
    ),
    
 ### b on the lepton side ###
    
    cms.PSet(
    tag = cms.untracked.string("leptonicBEta"),
    quantity = cms.untracked.string("?leptonicDecayB?leptonicDecayB.eta:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonicBPhi"),
    quantity = cms.untracked.string("?leptonicDecayB?leptonicDecayB.phi:-10000")
    ),
    cms.PSet(
    tag = cms.untracked.string("leptonicBPt"),
    quantity = cms.untracked.string("?leptonicDecayB?leptonicDecayB.pt:-10000")
    ),
    )
    )

### **** TCMET **** ###



process.CMGMicroTupleTCMets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("patMETsTC"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("TCMet"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    )
    )


### **** GENJET **** ###


process.CMGMicroTupleGENJets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("ak5GenJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("GENJet"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("mass"),
    quantity = cms.untracked.string("mass")
    ),
    cms.PSet(
    tag = cms.untracked.string("eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    )
    )

### **** GENMET **** ###


process.CMGMicroTupleGENMets = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("genMetCalo"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("GENMet"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    )
    )

### **** TRIGGERINFO **** ###


process.CMGMicroTupleTriggerInfo = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("patTriggerEvent"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("HLTMu"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("pt"),
    quantity = cms.untracked.string("pt")
    ),
    )
    )


### **** PV **** ###

process.CMGMicroTuplePrimaryVertices = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("offlinePrimaryVertices"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("PV"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("x"),
    quantity = cms.untracked.string("x")
    ),
    cms.PSet(
    tag = cms.untracked.string("y"),
    quantity = cms.untracked.string("y")
    ),
    cms.PSet(
    tag = cms.untracked.string("z"),
    quantity = cms.untracked.string("z")
    ),
    cms.PSet(
    tag = cms.untracked.string("xError"),
    quantity = cms.untracked.string("xError")
    ),
    cms.PSet(
    tag = cms.untracked.string("yError"),
    quantity = cms.untracked.string("yError")
    ),
    cms.PSet(
    tag = cms.untracked.string("zError"),
    quantity = cms.untracked.string("zError")
    ),
    cms.PSet(
    tag = cms.untracked.string("Chi2"),
    quantity = cms.untracked.string("chi2")
    ),
    cms.PSet(
    tag = cms.untracked.string("ndof"),
    quantity = cms.untracked.string("ndof")
    ),
    cms.PSet(
    tag = cms.untracked.string("isFake"),
    quantity = cms.untracked.string("isFake")
    ),
    )
    )


### **** BS **** ###


process.CMGMicroTupleBeamSpot = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("offlineBeamSpot"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("BS"),
    eventInfo = cms.untracked.bool(True),
    variables = cms.VPSet(
    cms.PSet(
    tag = cms.untracked.string("x"),
    quantity = cms.untracked.string("x0")
    ),
    cms.PSet(
    tag = cms.untracked.string("y"),
    quantity = cms.untracked.string("y0")
    ),
    cms.PSet(
    tag = cms.untracked.string("z"),
    quantity = cms.untracked.string("z0")
    ),
    cms.PSet(
    tag = cms.untracked.string("xError"),
    quantity = cms.untracked.string("x0Error")
    ),
    cms.PSet(
    tag = cms.untracked.string("yError"),
    quantity = cms.untracked.string("y0Error")
    ),
    cms.PSet(
    tag = cms.untracked.string("zError"),
    quantity = cms.untracked.string("z0Error")
    ),
    cms.PSet(
    tag = cms.untracked.string("type"),
    quantity = cms.untracked.string("type")
    ),
    )
    )







process.out = cms.OutputModule(
    "PoolOutputModule"
    ,fileName = cms.untracked.string('CMGEDMMicroTupla.root')
     ,outputCommands = cms.untracked.vstring("drop *"
                                             ,"keep *_CMGMicroTupleMuons_*_*"
                                             ,"keep *_CMGMicroTupleElectrons_*_*"
                                             ,"keep *_CMGMicroTupleCaloJets_*_*"
#                                            ,"keep *_Eeta_*_*"
#                                            ,"keep *_Ephi_*_*"
#                                            ,"keep *_Eecaliso_*_*"
                                             )
)

  
#process.outp = cms.EndPath(process.out)
process.p = cms.Path(process.flavorHistoryFilter*
                     process.CMGMicroTupleMuons*
                     process.CMGMicroTupleElectrons*
                     process.CMGMicroTupleCaloJets*
                     process.CMGMicroTuplePFJets*
                     process.CMGMicroTupleCaloMets*
                     process.CMGMicroTupleTQAF*
                     process.CMGMicroTupleTCMets*
                     process.CMGMicroTupleGENJets*
                     process.CMGMicroTupleGENMets*
                     process.CMGMicroTupleTriggerInfo*
                     process.CMGMicroTuplePrimaryVertices*
                     process.CMGMicroTupleBeamSpot*
                     process.out)
