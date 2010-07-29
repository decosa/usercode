import FWCore.ParameterSet.Config as cms

thisIsData = True
goCombined = True

if goCombined:
    process = cms.Process("CMG")
else:
    process = cms.Process("CMGPAT")


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )


# configure process options ----------------------------------------------------
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

# configure message logger -----------------------------------------------------

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
                                  

# conditions -------------------------------------------------------------------

process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.GeometryExtended_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.GlobalTag.globaltag = cms.string('GR10_P_V7::All') 


# source -----------------------------------------------------------------------

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
    "/store/relval/CMSSW_3_6_3/RelValTTbar/GEN-SIM-RECO/START36_V10-v1/0005/1E87EE3F-1478-DF11-B3F3-00304867902E.root"
    
    #'rfio:///castor/cern.ch/user/r/rovere/cmst3/localSkim/Sample_1_1.root',
    # '/store/relval/CMSSW_3_5_0_pre1/RelValTTbar/GEN-SIM-RECO/STARTUP3X_V14-v1/0006/14920B0A-0DE8-DE11-B138-002618943926.root'
    # '/store/relval/CMSSW_3_6_0_pre4/RelValProdMinBias/GEN-SIM-RECO/MC_36Y_V3-v1/0002/2A655C2D-E737-DF11-87C2-0030487C8CBE.root'
    )
    )

# CMGEDMMicroTuple Stuff -------------------------------------------------------

#####process.load('CMGEDMMicroTuple.CMGEDMMicroTuple.cmgedmmicrotuple_cfi')
process.load('CMGEDMMicroTuple.CMGEDMMicroTuple.cmgNtuples_cff')
# - Tune output filename
process.out.fileName = cms.untracked.string('data.root')


# Generator Information from TQAF ----------------------------------------------

process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")
from TopQuarkAnalysis.TopEventProducers.tqafEventContent_cff import tqafEventContent


# TT_SemileptonicJetPartonMatch ------------------------------------------------

process.load("TopQuarkAnalysis.TopTools.TtSemiLepJetPartonMatch_cfi")


# HCal Noise Cleaning ----------------------------------------------------------

process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')


# Ecal Endcap Alignment --------------------------------------------------------

process.load("RecoEgamma.ElectronIdentification.electronIdSequence_cff")
process.load("RecoEgamma.EgammaTools.correctedElectronsProducer_cfi")

# Standard PAT Configuration File ----------------------------------------------

process.load("PhysicsTools.PatAlgos.patSequences_cff")
# - Remove MC matching, photons, taus and cleaning from PAT default sequence
from PhysicsTools.PatAlgos.tools.coreTools import *
removeMCMatching(process, ['All'])

from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput
if not thisIsData:
    run36xOn35xInput(process)

# - Use the correct jet energy corrections
process.patJetCorrFactors.corrSample = "Spring10"

# - Compute dB w.r.t. beamspot!!
process.patMuons.usePV = False

# - Add pf met
from PhysicsTools.PatAlgos.tools.metTools import *
#addPfMET(process, 'PF')
addTcMET(process, 'TC')

# - Switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
switchOnTrigger( process )

# - Use recomputed Electrons with proper Endcap Alignment
if goCombined:
    process.patElectrons.electronSource = cms.InputTag("gsfElectrons","","CMG")
else:
    process.patElectrons.electronSource = cms.InputTag("gsfElectrons","","CMGPAT")

# DATA Filters ------------------------------------------------------------------

if thisIsData:
# - Require physics declared
    process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
    process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

# - Require scraping filter
    process.noscraping = cms.EDFilter("FilterOutScraping",
                                      applyfilter = cms.untracked.bool(True),
                                      debugOn = cms.untracked.bool(True),
                                      numtrack = cms.untracked.uint32(10),
                                      thresh = cms.untracked.double(0.25)
                                      )
    
# - Require PV Filter
    process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                               vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                               minimumNDOF = cms.uint32(4) ,
                                               maxAbsZ = cms.double(15), 
                                               maxd0 = cms.double(2) 
                                               )    
# - Configure HLT
    process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
    process.load('HLTrigger/HLTfilters/hltLevel1GTSeed_cfi')
    process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
#    process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0 AND (40 OR 41) AND NOT (36 OR 37 OR 38 OR 39)')
    process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('0')
        

# HLT single muon filter -------------------------------------------------------
import HLTrigger.HLTfilters.hltHighLevel_cfi
# - See also e.g. Alignment/CommonAlignmentProducer/python/ALCARECOMuAlCalIsolatedMu_cff.py
process.muon_filter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = [
    'HLT_Mu9',
    ],
#    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT8E29"),
    TriggerResultsTag = cms.InputTag("TriggerResults","","HLT"),
    andOr = cms.bool(True), # apply or
    )


#  HLT summary -----------------------------------------------------------------
import HLTrigger.HLTanalyzers.hlTrigReport_cfi
process.hltReport = HLTrigger.HLTanalyzers.hlTrigReport_cfi.hlTrigReport.clone()


# Rebuild GenJetParticles ------------------------------------------------------
process.load('Configuration.StandardSequences.Generator_cff')


# Add FlavorHistory, see https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideFlavorHistory 
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryProducer_cfi")
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryFilter_cfi")

# Output module configuration --------------------------------------------------
if not goCombined:
    process.out = cms.OutputModule("PoolOutputModule",
                                   fileName = cms.untracked.string('data.root'),
                                   # - Save only events passing the full path
                                   # SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
                                   outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_generalTracks_*_*',
        # - These seem to be needed for TtGenEvent...
        "keep recoGenParticles_decaySubset_*_*",
        "keep recoGenParticles_initSubset_*_*",
        # - Jet to parton associations
        "keep *_ttSemiLepJetPartonMatch_*_*",
        # - Keep the 'new' Trigger Result
        "keep *_TriggerResult_*_*",
        # - Keep all the Jet stuff
        "keep recoGenJets_*_*_*",
        "keep recoGenMETs_genMetCalo_*_*",
        "keep recoCaloJets_ak5CaloJets_*_*",
	#    "keep recoCaloMETs_*_*_*",
        "keep recoPFJets_ak5PFJets_*_*",
        "keep recoPFMETs_*_*_*",
        # - Keep PF STUFF
        "keep *_ak5PFJets_*_*",
        "keep *_pfMet_*_*",
        # - Keep Generator Stuff
        "keep genMetCalo_*_*_*",
        # - Keep Flavor history stuff
        "keep *_cFlavorHistoryProducer_*_*",
        "keep *_bFlavorHistoryProducer_*_*",
        "keep *_flavorHistoryFilter_*_*",
        )
                                   )

# - Save PAT Layer 0/1 output -- put in what you want to keep in the out.root file
from PhysicsTools.PatAlgos.patEventContent_cff import *
if not goCombined:
	process.out.outputCommands += patEventContentNoCleaning
	process.out.outputCommands += patEventContent
	process.out.outputCommands += patExtraAodEventContent
	process.out.outputCommands += patTriggerEventContent
if not thisIsData:
    process.out.outputCommands += tqafEventContent
if goCombined:
    process.out = cms.OutputModule(
	"PoolOutputModule"
	,fileName = cms.untracked.string('data.root')
	# - Save only events passing the full path
	#SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
	,outputCommands = cms.untracked.vstring("drop *"
						,"keep *_CMGMicroTuple_*_*"
						)
	)

# path and outpath ------------------------------------------------------------

# the output path
if thisIsData:
    if not goCombined:
        process.p = cms.Path(
            # - FILTERS COME FIRST
            process.muon_filter *
            #process.hltLevel1GTSeed *
            process.noscraping *
            process.primaryVertexFilter *
            # - Filter HCal Noise
            process.HBHENoiseFilter *
            process.gsfElectrons *
            process.eIdSequence *
            process.patDefaultSequence
            )
    else:
        process.p = cms.Path(
            # - Filter Come First
            process.muon_filter *
            #process.hltLevel1GTSeed *
            process.noscraping *
            process.primaryVertexFilter *
            # - Filter HCal Noise
            process.HBHENoiseFilter *
            process.gsfElectrons *
            process.eIdSequence *
            process.patDefaultSequence *
            process.CMGMicroTuple
            )
else:
    # the output path
    process.p = cms.Path(
        #FILTERS COME FIRST
        process.muon_filter *
        # Rebuild Gen Particle for Jet and MET
        process.genJetMET *
        # TQAF stuff
        process.makeGenEvt *
#        * process.genJetParticles
#        * process.ak5GenJets
#        * process.flavorHistorySeq
#        * process.recoGenJets
#        * process.simpleSecondaryVertexHighPurBJetTags
#        * process.simpleSecondaryVertexHighEffBJetTags
        process.patDefaultSequence *
        # Flavor History
        process.cFlavorHistoryProducer *
        process.bFlavorHistoryProducer *
        process.flavorHistoryFilter
#        * process.patTriggerSequence
#        process.CMGMicroTuple
        )
    
process.outpath = cms.EndPath(
    # note that it looks like we have to apply the HLT muon
    # filter here again, otherwise we get ALL input events
    # but with missing products...

    process.muon_filter *
    #process.hltLevel1GTSeed *
    process.noscraping *
    process.primaryVertexFilter *
    # - Filter HCal Noise
    process.HBHENoiseFilter *
    process.hltReport *
    process.out
    )


