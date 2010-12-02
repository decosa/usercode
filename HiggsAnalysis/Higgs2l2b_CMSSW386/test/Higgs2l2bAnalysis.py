import FWCore.ParameterSet.Config as cms


process = cms.Process("TRIM")


process.load("HiggsAnalysis.Higgs2l2b.Higgs2l2bedmNtuples_cff")
#process.load("HiggsAnalysis.Higgs2l2b.zjjEdmNtuples_cff")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service("TFileService", fileName = cms.string('h2l2b300Analysis.root') )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:h2l2b300.root',
    )
)



process.elChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
    higgsTag = cms.InputTag("hzzeejj:h"),
)

process.muChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
    higgsTag = cms.InputTag("hzzmmjj:h"),
)

#process.muChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
#    higgsTag = cms.InputTag("hzzmmjj"),
#)


process.edmNtuplesOut.fileName = cms.untracked.string('H300EdmNtuples.root')

process.analysisPath = cms.Path(
    process.elChannelAnalysis+
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
