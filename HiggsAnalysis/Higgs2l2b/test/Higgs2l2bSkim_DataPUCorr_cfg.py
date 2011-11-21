# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *


## global tag for data
process.GlobalTag.globaltag = 'GR_R_42_V19::All'


# Triggers for the /Jet PD are from:
# http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HLTrigger/Configuration/python/HLT_FULL_data_cff.py?revision=1.63&view=markup
# The list is here, let's take all of them :
## Jet = cms.vstring( 'HLT_DiJetAve100U_v4',
##   'HLT_DiJetAve140U_v4',
##   'HLT_DiJetAve15U_v4',
##   'HLT_DiJetAve180U_v4',
##   'HLT_DiJetAve300U_v4',
##   'HLT_DiJetAve30U_v4',
##   'HLT_DiJetAve50U_v4',
##   'HLT_DiJetAve70U_v4',
##   'HLT_Jet110_v1',
##   'HLT_Jet150_v1',
##   'HLT_Jet190_v1',
##   'HLT_Jet240_v1',
##   'HLT_Jet30_v1',
##   'HLT_Jet370_NoJetID_v1',
##   'HLT_Jet370_v1',
##   'HLT_Jet60_v1',
##   'HLT_Jet80_v1' ),
# mytrigs = ['*']

# Jet energy corrections to use: 
#inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
# no residual correction in 4_2_X: 
#inputJetCorrLabel = ('AK5PF', ['L1FastJet', 'L2Relative', 'L3Absolute'])
# now residual correction in 4_2_X are available
inputJetCorrLabel = ('AK5PF', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])

# add pf met
#from PhysicsTools.PatAlgos.tools.metTools import *
#addPfMET(process, 'PF')

removeMCMatching(process, ['All'])

# Switch to using PFMET 
from PhysicsTools.PatAlgos.tools.pfTools import *
switchToPFMET(
    process, 
    cms.InputTag('pfMet'), 
    ""
)

# Add PF jets
from PhysicsTools.PatAlgos.tools.jetTools import *

process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load('RecoJets.Configuration.RecoPFJets_cff')

process.kt6PFJets.doRhoFastjet = True
#process.kt6PFJets.Rho_EtaMax = cms.double(5.0)
#process.kt6PFJets.Ghost_EtaMax = cms.double(5.0)
process.ak5PFJets.doAreaFastjet = True
#process.ak5PFJets.Rho_EtaMax = cms.double(2.5)

process.patJetCorrFactors.rho = cms.InputTag('kt6PFJets','rho')

addJetCollection(process,cms.InputTag('ak5PFJets'),
                 'AK5','PFOffset',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('AK5PF', cms.vstring(['L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual'])),
                 doType1MET   = False,
                 doL1Cleaning   = False,
                 doL1Counters   = True,
                 genJetCollection=cms.InputTag(""),
                 doJetID      = True,
                 jetIdLabel   = "ak5"
                 )

switchJetCollection(process,cms.InputTag('ak5PFJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = inputJetCorrLabel,
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True
                 )
process.patJets.addTagInfos = True
process.patJets.tagInfoSources  = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD"),
    )

# Apply loose PF jet ID
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJets = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                   filterParams = pfJetIDSelector.clone(),
                                   src = cms.InputTag("selectedPatJets"),
                                   filter = cms.bool(True)
                                   )

# require physics declared
#process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
#process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

# require scraping filter
#process.scrapingVeto = cms.EDFilter("FilterOutScraping",
#                                    applyfilter = cms.untracked.bool(True),
#                                    debugOn = cms.untracked.bool(False),
#                                    numtrack = cms.untracked.uint32(10),
#                                    thresh = cms.untracked.double(0.2)
#                                    )
# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

# ECAL noise filtering
process.load('JetMETAnalysis.ecalDeadCellTools.EcalDeadCellEventFilter_cfi')

#
#from HLTrigger.HLTfilters.hltHighLevel_cfi import *
#if mytrigs is not None :
#    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
#    process.hltSelection.throw = False
#
#
#process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
#                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
#                                           minimumNDOF = cms.uint32(4) ,
#                                           maxAbsZ = cms.double(24), 
#                                           maxd0 = cms.double(2) 
#                                           )


# Select jets
process.selectedPatJets.cut = cms.string('pt > 30.0 && abs(eta) < 2.4')

# Add the files
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()



# Modules for the Cut-based Electron ID in the VBTF prescription
#import ElectroWeakAnalysis.WENu.simpleCutBasedElectronIDSpring10_cfi as vbtfid
# Switch to the official Electron VBTF Selection for 2011 Data (relax H/E cut in the Endcap):
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/VbtfEleID2011
import HiggsAnalysis.Higgs2l2b.simpleCutBasedElectronIDSummer11_cfi as vbtfid
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

process.patElectrons.electronIDSources = cms.PSet(
        eidVBTFRel95 = cms.InputTag("eidVBTFRel95"),
        eidVBTFRel80 = cms.InputTag("eidVBTFRel80"),
        eidVBTFCom95 = cms.InputTag("eidVBTFCom95"),
        eidVBTFCom80 = cms.InputTag("eidVBTFCom80")
)

# Muon Selection
process.selectedPatMuons.cut = (
            "pt > 10 && isGlobalMuon && isTrackerMuon && globalTrack().normalizedChi2 < 10 &&" +
            "innerTrack().hitPattern().numberOfValidTrackerHits > 10 && "                      +
            "innerTrack().hitPattern().numberOfValidPixelHits > 0 && "                         +
            "globalTrack().hitPattern().numberOfValidMuonHits > 0 && "                         +
            "dB < 0.2 && "                                                                     +
#            "trackIso + caloIso < 0.15 * pt && "                                               +
            "numberOfMatches > 1 && abs(eta) < 2.4"
        )

# Electron Selection (only ID and conversion)
process.selectedPatElectrons.cut = (
            "pt > 10.0 && abs(eta) < 2.5 &&"                               +
            "(isEE || isEB) && !isEBEEGap &&"                              +
            "( (electronID('eidVBTFCom95') == 7) ||"                       +
            " (electronID('eidVBTFCom95') == 5) )"
        )

# Muon with UserData
process.userDataSelectedMuons = cms.EDProducer(
    "Higgs2l2bMuonUserData",
    src = cms.InputTag("selectedPatMuons"),
    rho = cms.InputTag("kt6PFJets:rho")
)

# Electron with UserData
process.userDataSelectedElectrons = cms.EDProducer(
    "Higgs2l2bElectronUserData",
    src = cms.InputTag("selectedPatElectrons"),
    rho = cms.InputTag("kt6PFJets:rho")
)

# Isolated Muons
process.selectedIsoMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("userDataSelectedMuons"),
    cut = cms.string('userFloat("absCombIsoPUCorrected") < 0.15*pt')
)

# Isolated Electrons -> isolation is different for Barrel/Endcap
process.selectedIsoElectrons = cms.EDFilter(
    "PATElectronSelector",
    src = cms.InputTag("userDataSelectedElectrons"),
    cut = cms.string('( isEB && (userFloat("absCombIsoPUCorrected") < 0.15*pt) ) || '      +
                     '( !isEB && isEE && (userFloat("absCombIsoPUCorrected") < 0.1*pt) ) ' 
                     )
)

# Jet cleaning postponed after pat sequence
process.cleanPatJetsPURobust = cms.EDProducer("PATJetCleaner",
                           src = cms.InputTag("selectedPatJets"),
                           preselection = cms.string('pt > 30.0 && abs(eta) < 2.4'),
                           checkOverlaps = cms.PSet(
                              muons = cms.PSet(
                                          src = cms.InputTag("selectedIsoMuons"),
                                          algorithm = cms.string("byDeltaR"),
                                          preselection = cms.string(""),
                                          deltaR = cms.double(0.5),
                                          checkRecoComponents = cms.bool(False),
                                          pairCut = cms.string(""),
                                          requireNoOverlaps = cms.bool(True),
                              ),
                              electrons = cms.PSet(
                                              src = cms.InputTag("selectedIsoElectrons"),
                                              algorithm = cms.string("byDeltaR"),
                                              preselection = cms.string(""),
                                              deltaR = cms.double(0.5),
                                              checkRecoComponents = cms.bool(False),
                                              pairCut = cms.string(""),
                                              requireNoOverlaps = cms.bool(True),
                             )
                           ),
                           finalCut = cms.string('')
)

process.cleanPatJetsAK5PFOffset = cms.EDProducer("PATJetCleaner",
                           src = cms.InputTag("patJetsAK5PFOffset"),
                           preselection = cms.string('pt > 30.0 && abs(eta) < 2.4'),
                           checkOverlaps = cms.PSet(
                              muons = cms.PSet(
                                          src = cms.InputTag("selectedIsoMuons"),
                                          algorithm = cms.string("byDeltaR"),
                                          preselection = cms.string(""),
                                          deltaR = cms.double(0.5),
                                          checkRecoComponents = cms.bool(False),
                                          pairCut = cms.string(""),
                                          requireNoOverlaps = cms.bool(True),
                              ),
                              electrons = cms.PSet(
                                              src = cms.InputTag("selectedIsoElectrons"),
                                              algorithm = cms.string("byDeltaR"),
                                              preselection = cms.string(""),
                                              deltaR = cms.double(0.5),
                                              checkRecoComponents = cms.bool(False),
                                              pairCut = cms.string(""),
                                              requireNoOverlaps = cms.bool(True),
                             )
                           ),
                           finalCut = cms.string('')
)


# Z Candidates and Higgs Candidates
process.zee = cms.EDProducer("CandViewShallowCloneCombiner",
                                 checkCharge = cms.bool(True),
                                 cut = cms.string('mass >50 '),
                                 decay = cms.string("selectedIsoElectrons@+ selectedIsoElectrons@-")
                             )

process.zmm = cms.EDProducer("CandViewShallowCloneCombiner",
                                 checkCharge = cms.bool(True),
                                 cut = cms.string('mass > 50 '),
                                 decay = cms.string("selectedIsoMuons@+ selectedIsoMuons@-")
                             )

process.zem = cms.EDProducer("CandViewShallowCloneCombiner",
                                 checkCharge = cms.bool(True),
                                 cut = cms.string('mass > 50 '),
                                 decay = cms.string("selectedIsoElectrons@+ selectedIsoMuons@-")
                             )

process.zjj = cms.EDProducer("CandViewShallowCloneCombiner",
                                 checkCharge = cms.bool(False),
                                 cut = cms.string(''),
                                 decay = cms.string("cleanPatJetsPURobust cleanPatJetsPURobust")
                             )

process.hzzeejjBaseColl = cms.EDProducer("CandViewCombiner",
                                             checkCharge = cms.bool(False),
                                             cut = cms.string(''),
                                             decay = cms.string("zee zjj")
                                         )

process.hzzmmjjBaseColl = cms.EDProducer("CandViewCombiner",
                                             checkCharge = cms.bool(False),
                                             cut = cms.string(''),
                                             decay = cms.string("zmm zjj")
                                         )

process.hzzemjjBaseColl = cms.EDProducer("CandViewCombiner",
                                             checkCharge = cms.bool(False),
                                             cut = cms.string(''),
                                             decay = cms.string("zem zjj")
                                         )


process.hzzeejj = cms.EDProducer("Higgs2l2bUserDataNoMC",
                                     higgs = cms.InputTag("hzzeejjBaseColl"),
                                     #gensTag = cms.InputTag("genParticles"),
                                     metTag = cms.InputTag("patMETs")
                                     )

process.hzzmmjj = cms.EDProducer("Higgs2l2bUserDataNoMC",
                                     higgs = cms.InputTag("hzzmmjjBaseColl"),
                                     #gensTag = cms.InputTag("genParticles"),
                                     metTag = cms.InputTag("patMETs")
                                     )

process.hzzemjj = cms.EDProducer("Higgs2l2bUserDataNoMC",
                                     higgs = cms.InputTag("hzzemjjBaseColl"),
                                     #gensTag = cms.InputTag("genParticles"),
                                     metTag = cms.InputTag("patMETs")
                                     )


# Met variables producer
process.metInfoProducer = cms.EDProducer("MetVariablesProducer",
                                    metTag = cms.InputTag("patMETs")
                                    )

readFiles.extend( [
'file:/data3/scratch/cms/data/Run2011A/DoubleMu/May10ReReco-v1/161311/FC8C48F7-CE7B-E011-954A-001A92810AA4.root',
 ] )

process.source.fileNames = readFiles

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")

# select lumis interactively from a json
#import PhysicsTools.PythonAnalysis.LumiList as LumiList
#import FWCore.ParameterSet.Types as CfgTypes
#myLumis = LumiList.LumiList(filename = 'Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON.txt').getCMSSWString().split(',')
#process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
#process.source.lumisToProcess.extend(myLumis)

# let it run

process.p = cms.Path(
#    process.hltSelection*
#    process.scrapingVeto*
#    process.primaryVertexFilter*
    process.HBHENoiseFilter*
    process.EcalDeadCellEventFilter*
    process.recoPFJets *
    process.eidSequence *
    process.patDefaultSequence*
    process.userDataSelectedMuons *
    process.userDataSelectedElectrons *
    process.selectedIsoMuons *
    process.selectedIsoElectrons *
    process.cleanPatJetsPURobust *
    process.cleanPatJetsAK5PFOffset *
    process.zee +
    process.zmm +
    process.zem +
    process.zjj +
    process.hzzeejjBaseColl +
    process.hzzmmjjBaseColl +
    process.hzzemjjBaseColl +
    process.hzzeejj +
    process.hzzmmjj +
    process.hzzemjj +
    process.metInfoProducer
    )


# Setup for a basic filtering
process.zll = cms.EDProducer("CandViewMerger",
                             src = cms.VInputTag("zee", "zmm", "zem")
)

process.zllFilter = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("zll"),
                                 minNumber = cms.uint32(1),
)

process.jetFilter = cms.EDFilter("CandViewCountFilter",
                                 src = cms.InputTag("cleanPatJetsPURobust"),
                                 minNumber = cms.uint32(2),
)


process.filterPath = cms.Path(
#    process.hltSelection *
#    process.scrapingVeto *
#    process.primaryVertexFilter *
    process.HBHENoiseFilter *
    process.EcalDeadCellEventFilter *
    process.zll *
    process.zllFilter *
    process.jetFilter
)

# Output Module : Hopefully we keep all we need
process.out = cms.OutputModule("PoolOutputModule",
                 fileName = cms.untracked.string('h2l2bData_New.root'),
                 SelectEvents = cms.untracked.PSet(
                    SelectEvents = cms.vstring("filterPath")
                 ),
                 outputCommands =  cms.untracked.vstring(
                  'drop *_*_*_*',
                  'keep *_userDataSelectedElectrons_*_PAT',
                  'keep *_selectedIsoElectrons_*_PAT',
                  'keep *_userDataSelectedMuons_*_PAT',
                  'keep *_selectedIsoMuons_*_PAT',
#                  'keep *_cleanPatJets_*_PAT',
                  'keep *_cleanPatJetsPURobust_*_PAT',
                  'keep *_cleanPatJetsAK5PFOffset_*_PAT',
                  'keep *_kt6PFJets_rho_PAT',
                  'keep *_zee_*_PAT',
                  'keep *_zmm_*_PAT',
                  'keep *_zem_*_PAT',
                  'keep *_zjj_*_PAT',
                  'keep *_hzzeejj_*_PAT',
                  'keep *_hzzmmjj_*_PAT',
                  'keep *_hzzemjj_*_PAT',
                #'keep *_TriggerResults*_*_HLT',
                #'keep *_hltTriggerSummaryAOD_*_HLT',
                #'keep *_TriggerResults*_*_REDIGI*',
                #'keep *_hltTriggerSummaryAOD_*_REDIGI*',
                  'keep *_offlinePrimaryVertices_*_*',
                  'keep *_secondaryVertexTagInfos*_*_*',
                  'keep *_*_*tagInfo*_*',
                  'keep *_generalTracks_*_*',
                  'keep *_metInfoProducer_*_*',
                  ),
)

process.out.SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring("filterPath",
                                       )
)


# switch on PAT trigger
from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process, sequence = 'p', hltProcess = '*' )

process.outPath = cms.EndPath(process.out)

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 10000
process.options.wantSummary = True
