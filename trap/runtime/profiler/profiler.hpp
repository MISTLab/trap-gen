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

/// Profiler: it keeps track of many runtime statistics on:
/// - number and percentage of instructions executed of each type.
/// - call graph: time of each call.
/// - function stats: time and percentage in each function
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
