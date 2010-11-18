#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <TTree.h>
#include "HiggsAnalysis/Higgs2l2b/interface/Higgs2l2bCandidate.h"

class Higgs2l2bCandidateMaker : public edm::EDProducer {
    public:
        explicit Higgs2l2bCandidateMaker(const edm::ParameterSet&);
        ~Higgs2l2bCandidateMaker();
    
    private:
        virtual void beginJob();
        virtual void produce(edm::Event&, const edm::EventSetup&);
        virtual void endJob();

        edm::InputTag gensTag;
        edm::InputTag higgsTag;
        edm::InputTag metTag;
};

Higgs2l2bCandidateMaker::Higgs2l2bCandidateMaker(const edm::ParameterSet& iConfig): 
    gensTag(iConfig.getParameter<edm::InputTag>("gensTag")),
    higgsTag(iConfig.getParameter<edm::InputTag>("higgsTag")),
    metTag(iConfig.getParameter<edm::InputTag>("metTag"))
{
   produces<std::vector<Higgs2l2bCandidate> >();
}


Higgs2l2bCandidateMaker::~Higgs2l2bCandidateMaker() {
}

void Higgs2l2bCandidateMaker::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    using namespace edm;
    using namespace reco;
    using namespace std;

    Handle<GenParticleCollection> gensH;
    iEvent.getByLabel(gensTag, gensH);
    GenParticleCollection gens = *gensH;

    Handle<CompositeCandidateCollection> higgsH;
    iEvent.getByLabel(higgsTag, higgsH);
    CompositeCandidateCollection higgs = *higgsH;

    Handle<pat::METCollection> metH;
    iEvent.getByLabel(metTag, metH);
    pat::METCollection met = *metH;

    std::auto_ptr<std::vector<Higgs2l2bCandidate> > h2l2bCollection(new std::vector<Higgs2l2bCandidate>);

    for (size_t i = 0; i < higgs.size(); i++) {
        Higgs2l2bCandidate h2l2b;

        CompositeCandidate* zllptr = dynamic_cast<CompositeCandidate*>(higgs[i].daughter(0));
        CompositeCandidate* zjjptr = dynamic_cast<CompositeCandidate*>(higgs[i].daughter(1));

        CompositeCandidate  zll = *zllptr;
        CompositeCandidate  zjj = *zjjptr;

        h2l2b.higgsmass = higgs[i].mass();            
        h2l2b.higgspt   = higgs[i].pt();            
        h2l2b.higgseta  = higgs[i].eta();            
        h2l2b.higgsphi  = higgs[i].phi();            

        h2l2b.zllmass = zll.mass();            
        h2l2b.zllpt   = zll.pt();            
        h2l2b.zlleta  = zll.eta();            
        h2l2b.zllphi  = zll.phi();            

        h2l2b.zjjmass = zjj.mass();            
        h2l2b.zjjpt   = zjj.pt();            
        h2l2b.zjjeta  = zjj.eta();            
        h2l2b.zjjphi  = zjj.phi();            

        h2l2b.met    = met.front().et();
        h2l2b.metsig = met.front().mEtSig();
        h2l2b.metphi = met.front().phi();

        if (zll.daughter(0)->pt() < zll.daughter(1)->pt()) {
            h2l2b.lminpt  = zll.daughter(0)->pt();
            h2l2b.lmineta = zll.daughter(0)->eta();
            h2l2b.lminphi = zll.daughter(0)->phi();
            h2l2b.lmaxpt  = zll.daughter(1)->pt();
            h2l2b.lmaxeta = zll.daughter(1)->eta();
            h2l2b.lmaxphi = zll.daughter(1)->phi();
        }
        
        else {
            h2l2b.lminpt  = zll.daughter(1)->pt();
            h2l2b.lmineta = zll.daughter(1)->eta();
            h2l2b.lminphi = zll.daughter(1)->phi();
            h2l2b.lmaxpt  = zll.daughter(0)->pt();
            h2l2b.lmaxeta = zll.daughter(0)->eta();
            h2l2b.lmaxphi = zll.daughter(0)->phi();
        }

        if (zjj.daughter(0)->pt() < zjj.daughter(1)->pt()) {
            h2l2b.jminpt  = zjj.daughter(0)->pt();
            h2l2b.jmineta = zjj.daughter(0)->eta();
            h2l2b.jminphi = zjj.daughter(0)->phi();
            h2l2b.jmaxpt  = zjj.daughter(1)->pt();
            h2l2b.jmaxeta = zjj.daughter(1)->eta();
            h2l2b.jmaxphi = zjj.daughter(1)->phi();
        }
        
        else {
            h2l2b.jminpt  = zjj.daughter(1)->pt();
            h2l2b.jmineta = zjj.daughter(1)->eta();
            h2l2b.jminphi = zjj.daughter(1)->phi();
            h2l2b.jmaxpt  = zjj.daughter(0)->pt();
            h2l2b.jmaxeta = zjj.daughter(0)->eta();
            h2l2b.jmaxphi = zjj.daughter(0)->phi();
        }

        h2l2b.jminbmatch = false;
        h2l2b.jmincmatch = false;
        h2l2b.jmaxbmatch = false;
        h2l2b.jmaxcmatch = false;

        for (size_t k = 0; k < gens.size(); k++) {
            if (abs(gens[k].pdgId()) == 5 && gens[k].status() != 3 && deltaR(h2l2b.jmineta, h2l2b.jminphi, gens[k].eta(), gens[k].phi()) < 0.3) h2l2b.jminbmatch = true; 
            if (abs(gens[k].pdgId()) == 4 && gens[k].status() != 3 && deltaR(h2l2b.jmineta, h2l2b.jminphi, gens[k].eta(), gens[k].phi()) < 0.3) h2l2b.jmincmatch = true; 
            if (abs(gens[k].pdgId()) == 5 && gens[k].status() != 3 && deltaR(h2l2b.jmaxeta, h2l2b.jmaxphi, gens[k].eta(), gens[k].phi()) < 0.3) h2l2b.jmaxbmatch = true; 
            if (abs(gens[k].pdgId()) == 4 && gens[k].status() != 3 && deltaR(h2l2b.jmaxeta, h2l2b.jmaxphi, gens[k].eta(), gens[k].phi()) < 0.3) h2l2b.jmaxcmatch = true; 
        }

        if (zjj.daughter(0)->pt() < zjj.daughter(1)->pt()) {
            h2l2b.jmincsv    = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("combinedSecondaryVertexBJetTags");
            h2l2b.jmincsvmva = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
            h2l2b.jminjprob  = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("jetBProbabilityBJetTags");
            h2l2b.jminjbprob = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("jetBProbabilityJetTags");
            h2l2b.jminssvhe  = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
            h2l2b.jminssvhp  = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
            h2l2b.jminelpt   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softElectronByPtBJetTags");
            h2l2b.jminelip   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softElectronByIP3BJetTags");
            h2l2b.jminmu     = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softMuonBJetTags");
            h2l2b.jminmupt   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softMuonPtBJetTags");
            h2l2b.jminmuip   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softMuonIP3BJetTags");
            h2l2b.jmintkhe   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("trackCountingHighEffBJetTags");
            h2l2b.jmintkhp   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("trackCountingHighPurBJetTags");
            
            h2l2b.jmaxcsv    = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("combinedSecondaryVertexBJetTags");
            h2l2b.jmaxcsvmva = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
            h2l2b.jmaxjprob  = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("jetBProbabilityBJetTags");
            h2l2b.jmaxjbprob = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("jetBProbabilityJetTags");
            h2l2b.jmaxssvhe  = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
            h2l2b.jmaxssvhp  = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
            h2l2b.jmaxelpt   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softElectronByPtBJetTags");
            h2l2b.jmaxelip   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softElectronByIP3BJetTags");
            h2l2b.jmaxmu     = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softMuonBJetTags");
            h2l2b.jmaxmupt   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softMuonPtBJetTags");
            h2l2b.jmaxmuip   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softMuonIP3BJetTags");
            h2l2b.jmaxtkhe   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("trackCountingHighEffBJetTags");
            h2l2b.jmaxtkhp   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("trackCountingHighPurBJetTags");

            float neutralHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->neutralHadronEnergy();
            float HFHadronEnergy      = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->HFHadronEnergy();
            float neutralEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->neutralEmEnergy();
            float chargedEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->chargedEmEnergy();
            float chargedHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->chargedHadronEnergy();
            float energy              = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->energy();

            if (neutralEmEnergy/energy < 1.00 && chargedEmEnergy/energy < 1.00 && chargedHadronEnergy/energy > 0) h2l2b.jminid = true;
            else h2l2b.jminid = false;

            neutralHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->neutralHadronEnergy();
            HFHadronEnergy      = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->HFHadronEnergy();
            neutralEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->neutralEmEnergy();
            chargedEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->chargedEmEnergy();
            chargedHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->chargedHadronEnergy();
            energy              = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->energy();

            if (neutralEmEnergy/energy < 1.00 && chargedEmEnergy/energy < 1.00 && chargedHadronEnergy/energy > 0) h2l2b.jmaxid = true;
            else h2l2b.jmaxid = false;
        }

        else {
            h2l2b.jmincsv    = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("combinedSecondaryVertexBJetTags");
            h2l2b.jmincsvmva = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
            h2l2b.jminjprob  = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("jetProbabilityBJetTags");
            h2l2b.jminjbprob = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("jetBProbabilityBJetTags");
            h2l2b.jminssvhe  = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
            h2l2b.jminssvhp  = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
            h2l2b.jminelpt   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softElectronByPtBJetTags");
            h2l2b.jminelip   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softElectronByIP3BJetTags");
            h2l2b.jminmu     = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softMuonBJetTags");
            h2l2b.jminmupt   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softMuonPtBJetTags");
            h2l2b.jminmuip   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("softMuonIP3BJetTags");
            h2l2b.jmintkhe   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("trackCountingHighEffBJetTags");
            h2l2b.jmintkhp   = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->bDiscriminator("trackCountingHighPurBJetTags");
        
            h2l2b.jmaxcsv    = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("combinedSecondaryVertexBJetTags");
            h2l2b.jmaxcsvmva = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("combinedSecondaryVertexMVABJetTags");
            h2l2b.jmaxjprob  = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("jetProbabilityBJetTags");
            h2l2b.jmaxjbprob = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("jetBProbabilityBJetTags");
            h2l2b.jmaxssvhe  = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("simpleSecondaryVertexHighEffBJetTags");
            h2l2b.jmaxssvhp  = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("simpleSecondaryVertexHighPurBJetTags");
            h2l2b.jmaxelpt   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softElectronByPtBJetTags");
            h2l2b.jmaxelip   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softElectronByIP3BJetTags");
            h2l2b.jmaxmu     = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softMuonBJetTags");
            h2l2b.jmaxmupt   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softMuonPtBJetTags");
            h2l2b.jmaxmuip   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("softMuonIP3BJetTags");
            h2l2b.jmaxtkhe   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("trackCountingHighEffBJetTags");
            h2l2b.jmaxtkhp   = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->bDiscriminator("trackCountingHighPurBJetTags");

            float neutralHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->neutralHadronEnergy();
            float HFHadronEnergy      = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->HFHadronEnergy();
            float neutralEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->neutralEmEnergy();
            float chargedEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->chargedEmEnergy();
            float chargedHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->chargedHadronEnergy();
            float energy              = (dynamic_cast<pat::Jet*>(zjj.daughter(1)))->energy();

            if (neutralEmEnergy/energy < 1.00 && chargedEmEnergy/energy < 1.00 && chargedHadronEnergy/energy > 0) h2l2b.jminid = true;
            else h2l2b.jminid = false;

            neutralHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->neutralHadronEnergy();
            HFHadronEnergy      = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->HFHadronEnergy();
            neutralEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->neutralEmEnergy();
            chargedEmEnergy     = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->chargedEmEnergy();
            chargedHadronEnergy = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->chargedHadronEnergy();
            energy              = (dynamic_cast<pat::Jet*>(zjj.daughter(0)))->energy();

            if (neutralEmEnergy/energy < 1.00 && chargedEmEnergy/energy < 1.00 && chargedHadronEnergy/energy > 0) h2l2b.jmaxid = true;
            else h2l2b.jmaxid = false;
        }

        h2l2b.zzdphi = fabs(deltaPhi(zll.phi(), zjj.phi()));
        h2l2b.zzdeta = fabs(zll.eta() - zjj.eta());
        h2l2b.zzdr = deltaR(zll.eta(),  zll.phi(), zjj.eta(), zjj.phi());
        
        h2l2b.lldphi = fabs(deltaPhi(zll.daughter(0)->phi(), zll.daughter(1)->phi()));
        h2l2b.lldeta = fabs(zll.daughter(0)->eta() - zll.daughter(1)->eta());
        h2l2b.lldr = deltaR(zll.daughter(0)->eta(),  zll.daughter(0)->phi(), zll.daughter(1)->eta(), zll.daughter(1)->phi());
        
        h2l2b.jjdphi = fabs(deltaPhi(zjj.daughter(0)->phi(), zjj.daughter(1)->phi()));
        h2l2b.jjdeta = fabs(zjj.daughter(0)->eta() - zjj.daughter(1)->eta());
        h2l2b.jjdr = deltaR(zjj.daughter(0)->eta(),  zjj.daughter(0)->phi(), zjj.daughter(1)->eta(), zjj.daughter(1)->phi());

        h2l2bCollection->push_back(h2l2b);
    }



    iEvent.put(h2l2bCollection);
}

void Higgs2l2bCandidateMaker::beginJob() {
}

void Higgs2l2bCandidateMaker::endJob() {
}

DEFINE_FWK_MODULE(Higgs2l2bCandidateMaker);
