import FWCore.ParameterSet.Config as cms


process = cms.Process("TRIM")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.TFileService = cms.Service("TFileService", fileName = cms.string('tree_h2l2b300.root') )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:h2l2b300New.root',
    )
)



process.elChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
    higgsTag = cms.InputTag("hzzeejj"),
)


#process.muChannelAnalysis = cms.EDAnalyzer("Higgs2l2bAnalysis",
#    higgsTag = cms.InputTag("hzzmmjj"),
#)

process.analysisPath = cms.Path(process.elChannelAnalysis)#+process.muChannelAnalysis)
