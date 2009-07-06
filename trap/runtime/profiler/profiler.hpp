#ifndef PROFILER_HPP
#define PROFILER_HPP

#include <map>
#include <string>
#include <vector>

#include "ToolsIf.hpp"
#include "ABIIf.hpp"
#include "instructionBase.hpp"
#include "bfdFrontend.hpp"

namespace trap{

template<class issueWidth> class Profiler : public ToolsIf<addressType>{
  private:
    ABIIf<issueWidth> &processorInstance;
    BFDFrontend & bfdInstance;
  public:
    Profiler(ABIIf<issueWidth> &processorInstance, std::string execName) : processorInstance(processorInstance), bfdInstance(BFDFrontend::getInstance(execName)){
    }
    bool newIssue(const issueWidth &curPC, const InstructionBase *curInstr) throw(){
    }
    ~Profiler(){
    }
};

}

#endif
