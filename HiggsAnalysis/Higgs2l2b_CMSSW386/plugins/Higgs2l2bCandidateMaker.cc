#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <TTree.h>
#include <algorithm>
#include <iostream>
#include "HiggsAnalysis/Higgs2l2b/interface/sorters.h"
#include "HiggsAnalysis/Higgs2l2b/interface/Higgs2l2bCandidate.h"

class Higgs2l2bCandidateMaker : public edm::EDProducer {
    public:
        explicit Higgs2l2bCandidateMaker(const edm::ParameterSet&);
        ~Higgs2l2bCandidateMaker();
    
    private:
        virtual void beginJob();
        virtual void produce(edm::Event&, const edm::EventSetup&);
        virtual void endJob();

        edm::InputTag jetsTag;
        edm::InputTag zllTag;
        bool isMuonChannel;
};

Higgs2l2bCandidateMaker::Higgs2l2bCandidateMaker(const edm::ParameterSet& iConfig): 
    jetsTag(iConfig.getParameter<edm::InputTag>("jetsTag")),
    zllTag(iConfig.getParameter<edm::InputTag>("zllTag")),
    isMuonChannel(iConfig.getParameter<bool>("isMuonChannel"))
{
   produces<std::vector<Higgs2l2bCandidate> >();
}


Higgs2l2bCandidateMaker::~Higgs2l2bCandidateMaker() {
}

void Higgs2l2bCandidateMaker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    using namespace edm;
    using namespace reco;
    using namespace std;

    Handle<pat::JetCollection> jetsH;
    iEvent.getByLabel(jetsTag, jetsH);
    pat::JetCollection jets = *jetsH;

    Handle<CompositeCandidateCollection> zllH;
    iEvent.getByLabel(zllTag, zllH);
    CompositeCandidateCollection zll = *zllH;

    std::auto_ptr<std::vector<Higgs2l2bCandidate> > higgs(new std::vector<Higgs2l2bCandidate>);

    CompositeCandidateCollection zjj;

    for (size_t i = 0; i < jets.size(); i++) {
        for (size_t j = i+1; j < jets.size(); j++) {
            CompositeCandidate dijet;
            dijet.addDaughter(jets[i]);
            dijet.addDaughter(jets[j]);
            AddFourMomenta addjj;
            addjj.set(dijet);
            zjj.push_back(dijet);
        }
    }

    for (size_t i = 0; i < zll.size(); i++) {
        for (size_t j = 0; j < zjj.size(); j++) {
            CompositeCandidate h;
            h.addDaughter(zll[i]);
            h.addDaughter(zjj[j]);
            AddFourMomenta addzz;
            addzz.set(h);

            
            Higgs2l2bCandidate h2l2b;

            h2l2b.higgsmass = h.mass();            
            h2l2b.higgspt   = h.pt();            
            h2l2b.higgseta  = h.eta();            
            h2l2b.higgsphi  = h.phi();            

            h2l2b.zllmass = zll[i].mass();            
            h2l2b.zllpt   = zll[i].pt();            
            h2l2b.zlleta  = zll[i].eta();            
            h2l2b.zllphi  = zll[i].phi();            

            h2l2b.zjjmass = zjj[j].mass();            
            h2l2b.zjjpt   = zjj[j].pt();            
            h2l2b.zjjeta  = zjj[j].eta();            
            h2l2b.zjjphi  = zjj[j].phi();            

            if (zll[i].daughter(0)->pt() < zll[i].daughter(1)->pt()) {
                h2l2b.lminpt  = zll[i].daughter(0)->pt();
                if (isMuonChannel) h2l2b.lminet = zll[i].daughter(0)->pt();
                else {
                    float scenergy = (dynamic_cast<pat::Electron*>(zll[i].daughter(0)))->superCluster()->energy();
                    float sceta = (dynamic_cast<pat::Electron*>(zll[i].daughter(0)))->superCluster()->eta();
                    h2l2b.lminet = scenergy/cosh(sceta);
                }
                h2l2b.lmineta = zll[i].daughter(0)->eta();
                h2l2b.lminphi = zll[i].daughter(0)->phi();
                h2l2b.lmaxpt  = zll[i].daughter(1)->pt();
                if (isMuonChannel) h2l2b.lmaxet = zll[i].daughter(1)->pt();
                else {
                    float scenergy = (dynamic_cast<pat::Electron*>(zll[i].daughter(1)))->superCluster()->energy();
                    float sceta = (dynamic_cast<pat::Electron*>(zll[i].daughter(1)))->superCluster()->eta();
                    h2l2b.lmaxet = scenergy/cosh(sceta);
                }
                h2l2b.lmaxeta = zll[i].daughter(1)->eta();
                h2l2b.lmaxphi = zll[i].daughter(1)->phi();
                if (isMuonChannel) {
                    if ((dynamic_cast<pat::Muon*>(zll[i].daughter(0)))->triggerObjectMatchesByPath("HLT_Mu9").size() > 0) h2l2b.lminHLT = true; 
                    else h2l2b.lminHLT = false;
                    if ((dynamic_cast<pat::Muon*>(zll[i].daughter(1)))->triggerObjectMatchesByPath("HLT_Mu9").size() > 0) h2l2b.lmaxHLT = true;
                    else h2l2b.lmaxHLT = false;
                }
                else {
                    if ((dynamic_cast<pat::Electron*>(zll[i].daughter(0)))->triggerObjectMatchesByPath("HLT_Ele15_LW_L1R").size() > 0) h2l2b.lminHLT = true; 
                    else h2l2b.lminHLT = false;
                    if ((dynamic_cast<pat::Electron*>(zll[i].daughter(1)))->triggerObjectMatchesByPath("HLT_Ele15_LW_L1R").size() > 0) h2l2b.lmaxHLT = true;
                    else h2l2b.lmaxHLT = false;
                }
            }
            
            else {
                h2l2b.lminpt  = zll[i].daughter(1)->pt();
                if (isMuonChannel) h2l2b.lminet = zll[i].daughter(1)->pt();
                else {
                    float scenergy = (dynamic_cast<pat::Electron*>(zll[i].daughter(1)))->superCluster()->energy();
                    float sceta = (dynamic_cast<pat::Electron*>(zll[i].daughter(1)))->superCluster()->eta();
                    h2l2b.lminet = scenergy/cosh(sceta);
                }
                h2l2b.lmineta = zll[i].daughter(1)->eta();
                h2l2b.lminphi = zll[i].daughter(1)->phi();
                h2l2b.lmaxpt  = zll[i].daughter(0)->pt();
                if (isMuonChannel) h2l2b.lmaxet = zll[i].daughter(0)->pt();
                else {
                    float scenergy = (dynamic_cast<pat::Electron*>(zll[i].daughter(0)))->superCluster()->energy();
                    float sceta = (dynamic_cast<pat::Electron*>(zll[i].daughter(0)))->superCluster()->eta();
                    h2l2b.lmaxet = scenergy/cosh(sceta);
                }
                h2l2b.lmaxeta = zll[i].daughter(0)->eta();
                h2l2b.lmaxphi = zll[i].daughter(0)->phi();
                if (isMuonChannel) {
                    if ((dynamic_cast<pat::Muon*>(zll[i].daughter(1)))->triggerObjectMatchesByPath("HLT_Mu9").size() > 0) h2l2b.lminHLT = true;
                    else h2l2b.lminHLT = false;
                    if ((dynamic_cast<pat::Muon*>(zll[i].daughter(0)))->triggerObjectMatchesByPath("HLT_Mu9").size() > 0) h2l2b.lmaxHLT = true;
                    else h2l2b.lmaxHLT = false;
                }
                else {
                    if ((dynamic_cast<pat::Electron*>(zll[i].daughter(1)))->triggerObjectMatchesByPath("HLT_Ele15_LW_L1R").size() > 0) h2l2b.lminHLT = true;
                    else h2l2b.lminHLT = false;
                    if ((dynamic_cast<pat::Electron*>(zll[i].daughter(0)))->triggerObjectMatchesByPath("HLT_Ele15_LW_L1R").size() > 0) h2l2b.lmaxHLT = true;
                    else h2l2b.lmaxHLT = false;
                }
            }

            if (zjj[j].daughter(0)->pt() < zjj[j].daughter(1)->pt()) {
                h2l2b.jminpt  = zjj[j].daughter(0)->pt();
                h2l2b.jmineta = zjj[j].daughter(0)->eta();
                h2l2b.jminphi = zjj[j].daughter(0)->phi();
                h2l2b.jmaxpt  = zjj[j].daughter(1)->pt();
                h2l2b.jmaxeta = zjj[j].daughter(1)->eta();
                h2l2b.jmaxphi = zjj[j].daughter(1)->phi();
            }
            
            else {
                h2l2b.jminpt  = zjj[j].daughter(1)->pt();
                h2l2b.jmineta = zjj[j].daughter(1)->eta();
                h2l2b.jminphi = zjj[j].daughter(1)->phi();
                h2l2b.jmaxpt  = zjj[j].daughter(0)->pt();
                h2l2b.jmaxeta = zjj[j].daughter(0)->eta();
                h2l2b.jmaxphi = zjj[j].daughter(0)->phi();
            }

            if (zjj[j].daughter(0)->pt() < zjj[j].daughter(1)->pt()) {
                h2l2b.jmincsv    = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("combinedSecondaryVertexBJetTags");
                h2l2b.jmincsvmva = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
                h2l2b.jminjprob  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("jetBProbabilityBJetTags");
                h2l2b.jminjbprob = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("jetBProbabilityJetTags");
                h2l2b.jminssvhe  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
                h2l2b.jminssvhp  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
                h2l2b.jminelpt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softElectronByPtBJetTags");
                h2l2b.jminelip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softElectronByIP3BJetTags");
                h2l2b.jminmu     = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softMuonBJetTags");
                h2l2b.jminmupt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softMuonPtBJetTags");
                h2l2b.jminmuip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softMuonIP3BJetTags");
                h2l2b.jmintkhe   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("trackCountingHighEffBJetTags");
                h2l2b.jmintkhp   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("trackCountingHighPurBJetTags");
                
                h2l2b.jmaxcsv    = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("combinedSecondaryVertexBJetTags");
                h2l2b.jmaxcsvmva = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
                h2l2b.jmaxjprob  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("jetBProbabilityBJetTags");
                h2l2b.jmaxjbprob = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("jetBProbabilityJetTags");
                h2l2b.jmaxssvhe  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
                h2l2b.jmaxssvhp  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
                h2l2b.jmaxelpt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softElectronByPtBJetTags");
                h2l2b.jmaxelip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softElectronByIP3BJetTags");
                h2l2b.jmaxmu     = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softMuonBJetTags");
                h2l2b.jmaxmupt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softMuonPtBJetTags");
                h2l2b.jmaxmuip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softMuonIP3BJetTags");
                h2l2b.jmaxtkhe   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("trackCountingHighEffBJetTags");
                h2l2b.jmaxtkhp   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("trackCountingHighPurBJetTags");
            }

            else {
                h2l2b.jmincsv    = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("combinedSecondaryVertexBJetTags");
                h2l2b.jmincsvmva = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
                h2l2b.jminjprob  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("jetBProbabilityBJetTags");
                h2l2b.jminjbprob = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("jetBProbabilityJetTags");
                h2l2b.jminssvhe  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
                h2l2b.jminssvhp  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
                h2l2b.jminelpt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softElectronByPtBJetTags");
                h2l2b.jminelip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softElectronByIP3BJetTags");
                h2l2b.jminmu     = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softMuonBJetTags");
                h2l2b.jminmupt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softMuonPtBJetTags");
                h2l2b.jminmuip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("softMuonIP3BJetTags");
                h2l2b.jmintkhe   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("trackCountingHighEffBJetTags");
                h2l2b.jmintkhp   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(1)))->bDiscriminator("trackCountingHighPurBJetTags");
           
                h2l2b.jmaxcsv    = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("combinedSecondaryVertexBJetTags");
                h2l2b.jmaxcsvmva = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
                h2l2b.jmaxjprob  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("jetBProbabilityBJetTags");
                h2l2b.jmaxjbprob = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("jetBProbabilityJetTags");
                h2l2b.jmaxssvhe  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
                h2l2b.jmaxssvhp  = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
                h2l2b.jmaxelpt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softElectronByPtBJetTags");
                h2l2b.jmaxelip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softElectronByIP3BJetTags");
                h2l2b.jmaxmu     = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softMuonBJetTags");
                h2l2b.jmaxmupt   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softMuonPtBJetTags");
                h2l2b.jmaxmuip   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("softMuonIP3BJetTags");
                h2l2b.jmaxtkhe   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("trackCountingHighEffBJetTags");
                h2l2b.jmaxtkhp   = (dynamic_cast<pat::Jet*>(zjj[j].daughter(0)))->bDiscriminator("trackCountingHighPurBJetTags");
            }

            h2l2b.zzdphi = fabs(deltaPhi(zll[i].phi(), zjj[j].phi()));
            h2l2b.zzdeta = fabs(zll[i].eta() - zjj[j].eta());
            h2l2b.zzdr = deltaR(zll[i].eta(), zll[i].phi(), zjj[j].eta(), zjj[j].phi());
            
            h2l2b.lldphi = fabs(deltaPhi(zll[i].daughter(0)->phi(), zll[i].daughter(1)->phi()));
            h2l2b.lldeta = fabs(zll[i].daughter(0)->eta() - zll[i].daughter(1)->eta());
            h2l2b.lldr = deltaR(zll[i].daughter(0)->eta(),  zll[i].daughter(0)->phi(), zll[i].daughter(1)->eta(), zll[i].daughter(1)->phi());
            
            h2l2b.jjdphi = fabs(deltaPhi(zjj[j].daughter(0)->phi(), zjj[j].daughter(1)->phi()));
            h2l2b.jjdeta = fabs(zjj[j].daughter(0)->eta() - zjj[j].daughter(1)->eta());
            h2l2b.jjdr = deltaR(zjj[j].daughter(0)->eta(), zjj[j].daughter(0)->phi(), zjj[j].daughter(1)->eta(), zjj[j].daughter(1)->phi());

            h2l2b.isMuon = isMuonChannel;

            higgs->push_back(h2l2b);
        }
    }



    iEvent.put(higgs);
}

void Higgs2l2bCandidateMaker::beginJob() {
}

void Higgs2l2bCandidateMaker::endJob() {
}

DEFINE_FWK_MODULE(Higgs2l2bCandidateMaker);
