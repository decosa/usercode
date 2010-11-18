import FWCore.ParameterSet.Config as cms


Higgs2e2bEdmNtuple = cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("hzzeejj"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string("eejj"),
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
    )
    )


edmNtuplesOut = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string('Higgs2l2bEdmNtuples.root'),
    outputCommands = cms.untracked.vstring(
    "drop *",
    "keep *_Higgs2e2bEdmNtuple_*_*",
    
    )
    )
