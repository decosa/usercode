
import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
        

def switchJECParameters(jetCorrFactors,newalgo,newtype="Calo",oldalgo="IC5",oldtype="Calo"):
   """Replace input tags in the JetCorrFactorsProducer -- L5Flavor is taken out as it is said not to be dependend on the specific jet algorithm"""
   for k in ['L1Offset', 'L2Relative', 'L3Absolute', 'L4EMF', 'L6UE', 'L7Parton']:
      vv = getattr(jetCorrFactors, k).value();
      if (vv != "none"):
         setattr(jetCorrFactors, k, vv.replace(oldalgo+oldtype,newalgo+newtype).replace(oldalgo,newalgo) )
         #the first replace is good for L2, L3; the last for L7 (which don't have type dependency, at least not in the name) 
        


class RunBTagging(ConfigToolBase):

   """Define a sequence to run BTagging on AOD on top of jet collection 'jetCollection', appending 'label' to module labels.
      The sequence will be called "btaggingAOD" + 'label', and will already be added to the process (but not to any Path)
      The sequence will include a JetTracksAssociatorAtVertex with name "jetTracksAssociatorAtVertex" + 'label'
      The method will return a pair (sequence, labels) where 'sequence' is the cms.Sequence object, and 'labels' contains
      labels["jta"]      = the name of the JetTrackAssociator module
      labels["tagInfos"] = list of names of TagInfo modules
      labels["jetTags "] = list of names of JetTag modules
      these labels are meant to be used for PAT BTagging tools
      NOTE: 'label' MUST NOT BE EMPTY
   """
   _label='RunBTagging'                                           
    
    
   def dumpPython(self):

      dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.RunBTagging import *\n\nrunBTagging(process, "
      dumpPython += str(self.getvalue('jetCollection'))+ ", "
      dumpPython += str(self.getvalue('label'))+'\n'
      return dumpPython     
                                                                                                      
   def __call__(self, process, jetCollection,label):
     
      self.addParameter('process',process, 'description: process')
      self.addParameter('jetCollection',jetCollection, 'description: InputTag')
      self.addParameter('label',label, 'description: label')
      
      process=self._parameters['process'].value
      
      
      
      
      if (label == ''):
         raise ValueError, "Label for re-running BTagging can't be empty, it will crash CRAB."
      process.load("RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi")
      process.load("RecoBTag.Configuration.RecoBTag_cff")
      from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import ic5JetTracksAssociatorAtVertex
      import RecoBTag.Configuration.RecoBTag_cff as btag
      # quickly make VInputTag from strings
      def vit(*args) : return cms.VInputTag( *[ cms.InputTag(x) for x in args ] )
      
      # define labels
      jtaLabel =  'jetTracksAssociatorAtVertex' + label
      ipTILabel = 'impactParameterTagInfos'     + label
      svTILabel = 'secondaryVertexTagInfos'     + label
      seTILabel = 'softElectronTagInfos'        + label
      smTILabel = 'softMuonTagInfos'            + label
      
      # make JTA and TagInfos
      setattr( process, jtaLabel,  ic5JetTracksAssociatorAtVertex.clone(jets = self.getvalue('jetCollection')))
      setattr( process, ipTILabel, btag.impactParameterTagInfos.clone(jetTracks = cms.InputTag(jtaLabel)) )
      setattr( process, svTILabel, btag.secondaryVertexTagInfos.clone(trackIPTagInfos = cms.InputTag(ipTILabel)) )
      setattr( process, seTILabel, btag.softElectronTagInfos.clone(jets = self.getvalue('jetCollection')) )
      setattr( process, smTILabel, btag.softMuonTagInfos.clone(jets = self.getvalue('jetCollection')) )
      setattr( process, 'jetBProbabilityBJetTags'+label, btag.jetBProbabilityBJetTags.clone(tagInfos = vit(ipTILabel)) )
      setattr( process, 'jetProbabilityBJetTags' +label,  btag.jetProbabilityBJetTags.clone(tagInfos = vit(ipTILabel)) )
      setattr( process, 'trackCountingHighPurBJetTags'+label, btag.trackCountingHighPurBJetTags.clone(tagInfos = vit(ipTILabel)) )
      setattr( process, 'trackCountingHighEffBJetTags'+label, btag.trackCountingHighEffBJetTags.clone(tagInfos = vit(ipTILabel)) )
      setattr( process, 'simpleSecondaryVertexBJetTags'+label, btag.simpleSecondaryVertexBJetTags.clone(tagInfos = vit(svTILabel)) )
      setattr( process, 'combinedSecondaryVertexBJetTags'+label, btag.combinedSecondaryVertexBJetTags.clone(tagInfos = vit(ipTILabel, svTILabel)) )
      setattr( process, 'combinedSecondaryVertexMVABJetTags'+label, btag.combinedSecondaryVertexMVABJetTags.clone(tagInfos = vit(ipTILabel, svTILabel)) )
      setattr( process, 'softMuonBJetTags'+label, btag.softMuonBJetTags.clone(tagInfos = vit(smTILabel)) )
      setattr( process, 'softMuonByPtBJetTags'+label, btag.softMuonByPtBJetTags.clone(tagInfos = vit(smTILabel)) )
      setattr( process, 'softMuonByIP3dBJetTags'+label, btag.softMuonByIP3dBJetTags.clone(tagInfos = vit(smTILabel)) )
      setattr( process, 'softElectronByPtBJetTags'+label, btag.softElectronByPtBJetTags.clone(tagInfos = vit(smTILabel)) )
      setattr( process, 'softElectronByIP3dBJetTags'+label, btag.softElectronByIP3dBJetTags.clone(tagInfos = vit(smTILabel)) )
      
      def mkseq(process, firstlabel, *otherlabels):
         seq = getattr(process, firstlabel)
         for x in otherlabels: seq += getattr(process, x)
         return cms.Sequence(seq)
        
      labels = { 'jta' : jtaLabel,
                 'tagInfos' : (ipTILabel,svTILabel,seTILabel,smTILabel),
                 'jetTags'  : [ (x + label) for x in ('jetBProbabilityBJetTags',
                                                      'jetProbabilityBJetTags',
                                                      'trackCountingHighPurBJetTags',
                                                      'trackCountingHighEffBJetTags',
                                                      'simpleSecondaryVertexBJetTags',
                                                      'combinedSecondaryVertexBJetTags',
                                                      'combinedSecondaryVertexMVABJetTags',
                                                      'softElectronByPtBJetTags',
                                                      'softElectronByIP3dBJetTags',
                                                      'softMuonBJetTags',
                                                      'softMuonByPtBJetTags',
                                                      'softMuonByIP3dBJetTags') ]
                 }
      
      setattr( process, 'btaggingTagInfos' + label, mkseq(process, *(labels['tagInfos']) ) )
      setattr( process, 'btaggingJetTags' + label,  mkseq(process, *(labels['jetTags'])  ) )
      seq = mkseq(process, jtaLabel, 'btaggingTagInfos' + label, 'btaggingJetTags' + label)
      setattr( process, 'btagging' + label, seq )
      return (seq, labels)
   


runBTagging=RunBTagging()
