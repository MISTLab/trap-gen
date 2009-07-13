#ifndef PROFILER_HPP
#define PROFILER_HPP

#ifdef __GNUC__
#ifdef __GNUC_MINOR__
#if (__GNUC__ >= 4 && __GNUC_MINOR__ >= 3)
#include <tr1/unordered_map>
#define template_map std::tr1::unordered_map
#else
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif
#else
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif
#else
#ifdef _WIN32
#include <hash_map>
#define  template_map stdext::hash_map
#else
#include <map>
#define  template_map std::map
#endif
#endif

#include <string>

#include <systemc.h>

#include "ToolsIf.hpp"
#include "ABIIf.hpp"
#include "instructionBase.hpp"
#include "bfdFrontend.hpp"
#include "profInfo.hpp"

namespace trap{

/// Profiler: it keeps track of many runtime statistics on:
/// - number and percentage of instructions executed of each type.
/// - function stats: time and percentage in each function
/// - call graph: time of each call.
template<class issueWidth> class Profiler : public ToolsIf<issueWidth>{
  private:
    //Interface with the processor
    ABIIf<issueWidth> &processorInstance;
    //instance of the BFD frontend containing information on the software
    //running on the processor
    BFDFrontend & bfdInstance;
    //name of the files on which the profiler should write the output
    std::string fileName;
    //Statistic on the instructions
    template_map<unsigned int, ProfInstruction> instructions;
    ProfInstruction *oldInstruction;
    sc_time oldInstrTime;
    template_map<unsigned int, ProfInstruction>::iterator instructionsEnd;
    //Statistic on the functions
    template_map<unsigned int, ProfFunction> functions;
    ProfFunction *oldFunction;
    sc_time oldFunTime;
    template_map<unsigned int, ProfFunction>::iterator functionsEnd;

    ///Based on the new instruction just issued, the statistics on the instructions
    ///are updated
    inline void updateInstructionStats(const issueWidth &curPC, const InstructionBase *curInstr) throw(){
        //Update the total number of instructions executed
        ProfInstruction::numTotalCalls++;
        //Update the old instruction elapsed time
        if(this->oldInstruction != NULL){
            this->oldInstruction->time += sc_time_stamp() - this->oldInstrTime;
            this->oldInstrTime = sc_time_stamp();
        }
        //Update the new instruction statistics
        template_map<unsigned int, ProfInstruction>::iterator foundInstr = this->instructions.find(curInstr->getId());
        if(foundInstr != this->instructionsEnd){
            foundInstr->second.numCalls++;
            this->oldInstruction = &(foundInstr->second);
        }
        else{
            this->instructions[curInstr->getId()].name = curInstr->getInstructionName();
            this->oldInstruction = &(this->instructions[curInstr->getId()]);
            this->instructionsEnd = this->instructions.end();
        }
    }
    ///Based on the new instruction just issued, the statistics on the functions
    ///are updated
    inline void updateFunctionStats(const issueWidth &curPC, const InstructionBase *curInstr) throw(){
    }
  public:
    Profiler(ABIIf<issueWidth> &processorInstance, std::string execName) : processorInstance(processorInstance),
                                                                    bfdInstance(BFDFrontend::getInstance(execName)){
        this->oldInstruction = NULL;
        this->oldInstrTime = SC_ZERO_TIME;
        this->instructionsEnd = this->instructions.end();
        this->oldFunction = NULL;
        this->oldFunTime = SC_ZERO_TIME;
        this->functionsEnd = this->functions.end();
    }
    ~Profiler(){
    }
    ///sets the file name on which the profiler should write the output
    void setOutputFile(std::string fileName){
        this->fileName = fileName;
    }

    ///Function called by the processor at every new instruction issue.
    bool newIssue(const issueWidth &curPC, const InstructionBase *curInstr) throw(){
        this->updateInstructionStats(curPC, curInstr);
        this->updateFunctionStats(curPC, curInstr);

        return false;
    }
};

}

#endif
