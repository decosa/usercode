#include <vector>
#include <map>
#include <string>
#include "HiggsAnalysis/Higgs2l2b/interface/Higgs2l2bCandidate.h"
#include "DataFormats/Common/interface/Wrapper.h"

namespace
{
     namespace
     {
         edm::Wrapper<Higgs2l2bCandidate> Higgs2l2bCandidateWrapper;
         edm::Wrapper< std::vector<Higgs2l2bCandidate> > Higgs2l2bCandidateVectorWrapper;
    }
}

