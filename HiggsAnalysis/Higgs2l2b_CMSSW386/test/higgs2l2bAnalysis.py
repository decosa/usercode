import FWCore.ParameterSet.Config as cms


process = cms.Process("TRIM")


process.load("HiggsAnalysis.Higgs2l2b.Higgs2l2bedmNtuples_cff")
#process.load("HiggsAnalysis.Higgs2l2b.zjjEdmNtuples_cff")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.TFileService = cms.Service("TFileService", fileName = cms.string('h2l2b300GF.root') )

process.source = cms.Source("PoolSource")

process.source.fileNames=cms.untracked.vstring('rfio:/castor/cern.ch/user/d/decosa/Higgs/h350/skim/h2l2b300GF_1_1_Ukh.root')
###
process.elChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
    higgsTag = cms.InputTag("hzzeejj:h"),
)
process.elChannelEvtCounter = cms.EDAnalyzer("EventCounter",
    higgsTag = cms.InputTag("hzzeejj:h"),
    metTag = cms.InputTag("hzzeejj:met")

)
process.muChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
    higgsTag = cms.InputTag("hzzmmjj:h"),
)

#process.muChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
#    higgsTag = cms.InputTag("hzzmmjj"),
#)


process.edmNtuplesOut.fileName = cms.untracked.string('H300GFEdmNtuples.root')

process.analysisPath = cms.Path(
    process.elChannelAnalysis+
    process.elChannelEvtCounter+
    process.muChannelAnalysis+
    process.Higgs2e2bEdmNtuple+
    process.Higgs2mu2bEdmNtuple#+
##    process.zjjEdmNtuple+
##    process.zeeEdmNtuple+
##    process.zmmEdmNtuple
    )

process.endPath = cms.EndPath(process.edmNtuplesOut)


process.schedule = cms.Schedule(
    process.analysisPath,
    process.endPath
    )
