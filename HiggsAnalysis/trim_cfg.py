import FWCore.ParameterSet.Config as cms

# Setup PAT
from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.pfTools import *


# Load some generic cffs  
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.EventContent.EventContent_cff')

# Specify the Global Tag
process.GlobalTag.globaltag = 'START3X_V26::All'

# Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# Source file : To be run on a Full RECO sample
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
    'file:/scratch2/users/fabozzi/higgs/zz2l2c/ZZ2l2c_6.root'
        
    )
)

# Output Module : Hopefully we keep all we need
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('zz2l2c.root'),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring("filterPath")
    ),
    outputCommands =  cms.untracked.vstring(
        'drop *_*_*_*',
        'keep *_*higgs_*_PAT',
        'keep *_selectedPatElectronsTriggerMatch_*_PAT',
        'keep *_selectedPatMuonsTriggerMatch_*_PAT',
        'keep *_cleanPatJets_*_PAT',
        'keep *_patMETs_*_PAT',
        'keep *_flavorHistoryFilter_*_PAT',
    ),
    verbose = cms.untracked.bool(True)
)

# Modules to run the SSV Tagger - Required for 35X
process.load("RecoBTag.Configuration.RecoBTag_cff")
process.load("RecoBTag.SecondaryVertex.simpleSecondaryVertexHighEffBJetTags_cfi")
process.load("RecoBTag.SecondaryVertex.simpleSecondaryVertexHighPurBJetTags_cfi")
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

# Modules for the Cut-based Electron ID in the VBTF prescription
import ElectroWeakAnalysis.WENu.simpleCutBasedElectronIDSpring10_cfi as vbtfid
process.eidVBTFRel95 = vbtfid.simpleCutBasedElectronID.clone( electronQuality = '95relIso' )
process.eidVBTFRel80 = vbtfid.simpleCutBasedElectronID.clone( electronQuality = '80relIso' )
process.eidVBTFCom95 = vbtfid.simpleCutBasedElectronID.clone( electronQuality = '95cIso'   )
process.eidVBTFCom80 = vbtfid.simpleCutBasedElectronID.clone( electronQuality = '80cIso'   )

process.eidSequence = cms.Sequence(
    process.eidVBTFRel95 +
    process.eidVBTFRel80 +
    process.eidVBTFCom95 +
    process.eidVBTFCom80 
)

# Keep a pruned collection of GenParticles to save space
process.prunedGen = cms.EDProducer( "GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        "drop  *  ",
        "keep++ pdgId = {Z0}",
        "++keep pdgId = {Z0}",
        "keep++ pdgId = {W+}",
        "++keep pdgId = {W+}",
        "keep++ pdgId = {W-}",
        "++keep pdgId = {W-}",
        "keep++ pdgId = {h0}",
        "++keep pdgId = {h0}",
        "keep++ pdgId = {e+}",
        "++keep pdgId = {e+}",
        "keep++ pdgId = {e-}",
        "++keep pdgId = {e-}",
        "keep++ pdgId = {mu+}",
        "++keep pdgId = {mu+}",
        "keep++ pdgId = {mu-}",
        "++keep pdgId = {mu-}",
        "keep++ pdgId = {tau+}",
        "++keep pdgId = {tau+}",
        "keep++ pdgId = {tau-}",
        "++keep pdgId = {tau-}",
        "keep++ pdgId = 4",
        "++keep pdgId = 4",
        "keep++ pdgId = -4",
        "++keep pdgId = -4",
        "keep++ pdgId = 5",
        "++keep pdgId = 5",
        "keep++ pdgId = -5",
        "++keep pdgId = -5"
    )
)

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryProducer_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")

# Muon Selection
process.selectedPatMuons.cut = ( "pt > 10 && isGlobalMuon && isTrackerMuon && globalTrack().normalizedChi2 < 10 &&" +
                                 "innerTrack().hitPattern().numberOfValidTrackerHits > 10 && "                      +
                                 "innerTrack().hitPattern().numberOfValidPixelHits > 0 && "                         +
                                 "globalTrack().hitPattern().numberOfValidMuonHits > 0 && "                         +
                                 "dB < 0.2 && "                                                                     +
                                 "trackIso + caloIso < 0.15 * pt && "                                               +
                                 "numberOfMatches > 1 && abs(eta) < 2.4" )

# Electron Selection
process.patElectrons.electronIDSources = cms.PSet(
    eidRobustLoose = cms.InputTag("eidRobustLoose"),
    eidLoose = cms.InputTag("eidLoose"),
    eidVBTFRel95 = cms.InputTag("eidVBTFRel95"),
    eidVBTFRel80 = cms.InputTag("eidVBTFRel80"),
    eidVBTFCom95 = cms.InputTag("eidVBTFCom95"),
    eidVBTFCom80 = cms.InputTag("eidVBTFCom80")
)

process.selectedPatElectrons.cut = ( "pt > 10.0 && abs(eta) < 2.5 &&"                               +
                                     "superCluster().energy / cosh(superCluster().eta) > 10.0 && "  +
                                     "(isEE || isEB) && !isEBEEGap &&"                                           +
                                     "electronID('eidVBTFCom95') == 7" )


# Switch to using PFJets 
switchJetCollection(
    process,
    cms.InputTag('ak5PFJets'),
    doJTA        = True,
    doBTagging   = True,
    jetCorrLabel = ('AK5', 'PF'),
    doType1MET   = True,
    genJetCollection=cms.InputTag("ak5GenJets"),
    doJetID      = True
)

process.patJetCorrFactors.corrLevels.L5Flavor = cms.string('none')
process.patJetCorrFactors.corrLevels.L7Parton = cms.string('none')

# Switch to using PFMET 
switchToPFMET(
    process, 
    cms.InputTag('pfMet'), 
    ""
)

# Clean the Jets from the seleted leptons
process.cleanPatJets = cms.EDProducer("PATJetCleaner",
    src = cms.InputTag("patJets"), 
    preselection = cms.string('pt > 30.0 && abs(eta) < 2.4'),
    checkOverlaps = cms.PSet(
        muons = cms.PSet(
           src       = cms.InputTag("selectedPatMuons"),
           algorithm = cms.string("byDeltaR"),
           preselection        = cms.string(""),
           deltaR              = cms.double(0.5),
           checkRecoComponents = cms.bool(False), 
           pairCut             = cms.string(""),
           requireNoOverlaps   = cms.bool(True), 
        ),
        electrons = cms.PSet(
           src       = cms.InputTag("selectedPatElectrons"),
           algorithm = cms.string("byDeltaR"),
           preselection        = cms.string(""),
           deltaR              = cms.double(0.5),
           checkRecoComponents = cms.bool(False), 
           pairCut             = cms.string(""),
           requireNoOverlaps   = cms.bool(True), 
        )
    ),
    finalCut = cms.string('')
)

# Remove MC Matching
removeMCMatching(process, ['Electrons', 'Muons', 'Jets', 'METs'])

# Trigger Matching Setup
process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")

process.electronsTriggerMatch = process.cleanElectronTriggerMatchHLTEle20SWL1R.clone()
#process.electronsTriggerMatch = process.electronTriggerMatchHLTEle15LWL1R.clone()
process.electronsTriggerMatch.src = "selectedPatElectrons"
process.electronsTriggerMatch.pathNames = cms.vstring('HLT_Ele15_LW_L1R')
process.electronsTriggerMatch.maxDeltaR = 0.2

process.muonsTriggerMatch = process.cleanMuonTriggerMatchHLTMu9.clone()
#process.muonsTriggerMatch = process.muonTriggerMatchHLTMu3.clone()
process.muonsTriggerMatch.src = "selectedPatMuons"
process.muonsTriggerMatch.pathNames = cms.vstring('HLT_Mu9')
process.muonsTriggerMatch.maxDeltaR = 0.2


process.selectedPatElectronsTriggerMatch = cms.EDProducer("PATTriggerMatchElectronEmbedder",
    src = cms.InputTag("selectedPatElectrons"),
    matches = cms.VInputTag(['electronsTriggerMatch'])
)

process.selectedPatMuonsTriggerMatch = cms.EDProducer("PATTriggerMatchMuonEmbedder",
    src = cms.InputTag("selectedPatMuons"),
    matches = cms.VInputTag(['muonsTriggerMatch'])
)


# Z Candidates : Z->emu can be used as a control sample for ttbar
process.zee = cms.EDProducer("CandViewCombiner",
    checkCharge = cms.bool(True),
    cut = cms.string('mass > 70 && mass < 110'),
    decay = cms.string("selectedPatElectronsTriggerMatch@+ selectedPatElectronsTriggerMatch@-")
)

process.zmm = cms.EDProducer("CandViewCombiner",
    checkCharge = cms.bool(True),
    cut = cms.string('mass > 70 && mass < 110 && min(abs(daughter(0).eta), abs(daughter(1).eta)) < 2.1'),
    decay = cms.string("selectedPatMuonsTriggerMatch@+ selectedPatMuonsTriggerMatch@-")
)

process.elhiggs = cms.EDProducer("Higgs2l2bCandidateMaker",
    zllTag = cms.InputTag("zee"),
    jetsTag = cms.InputTag("cleanPatJets"),
    metTag = cms.InputTag("patMETs"),
    isMuonChannel = cms.bool(False),
)

process.muhiggs = cms.EDProducer("Higgs2l2bCandidateMaker",
    zllTag = cms.InputTag("zmm"),
    jetsTag = cms.InputTag("cleanPatJets"),
    metTag = cms.InputTag("patMETs"),
    isMuonChannel = cms.bool(True),
)


# Define the relevant paths and schedule them
process.analysisPath = cms.Path(
    process.simpleSecondaryVertexHighEffBJetTags + 
    process.simpleSecondaryVertexHighPurBJetTags + 
    process.eidSequence +
    process.prunedGen + 
    process.genParticlesForJets +
    process.ak5GenJets +
    process.cFlavorHistoryProducer +
    process.bFlavorHistoryProducer +
    process.flavorHistoryFilter +
    process.makePatElectrons +
    process.makePatMuons +
    process.makePatJets +
    process.makePatMETs +
    process.selectedPatElectrons + 
    process.selectedPatMuons + 
    process.cleanPatJets +
    process.patTrigger +
    process.electronsTriggerMatch +
    process.muonsTriggerMatch +
    process.selectedPatElectronsTriggerMatch +
    process.selectedPatMuonsTriggerMatch +
    process.zee +
    process.zmm + 
    process.elhiggs + 
    process.muhiggs 
)

# Setup for a basic filtering  - 2 leptons with PT > 20 GeV/c
process.zll = cms.EDProducer("CandViewMerger",
    src = cms.VInputTag("zee", "zmm")
) 

process.zllFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("zll"),
    minNumber = cms.uint32(1),
)

process.jetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("cleanPatJets"),
    minNumber = cms.uint32(2),
)

process.filterPath = cms.Path(process.zll+process.zllFilter+process.jetFilter)

process.outPath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.analysisPath,
    process.filterPath,
    process.outPath
)
