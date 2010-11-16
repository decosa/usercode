#ifndef SORTERS_H
#define SORTERS_H

#include <string>
#include "HiggsAnalysis/Higgs2l2b/interface/Higgs2l2bCandidate.h"

namespace sorters {

    struct PTBasedPatJetSorter {
        bool operator() (const pat::Jet& j1, const pat::Jet& j2) {
            return (j1.pt() > j2.pt());
        }
    };

    struct ZMassBasedCompositeCandidateSorter {
        bool operator() (const reco::CompositeCandidate& c1, const reco::CompositeCandidate& c2) {
            return (fabs(c1.mass() - 91.187) < fabs(c2.mass() - 91.187));
        }
    };

    struct BTagBasedJetSorter {
        std::string tagname;
        BTagBasedJetSorter(std::string tn):
            tagname(tn) {}
        bool operator() (const pat::Jet& j1, const pat::Jet& j2) {
            return (j1.bDiscriminator(tagname) < j2.bDiscriminator(tagname));
        }
    };


}

#endif
