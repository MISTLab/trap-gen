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
#include <vector>

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
    //Statistic on the instructions
    template_map<unsigned int, ProfInstruction> instructions;
    ProfInstruction *oldInstruction;
    sc_time oldInstrTime;
    template_map<unsigned int, ProfInstruction>::iterator instructionsEnd;
    //Statistic on the functions
    template_map<issueWidth, ProfFunction> functions;
    std::vector<ProfFunction *> currentStack;
    sc_time oldFunTime;
    template_map<issueWidth, ProfFunction>::iterator functionsEnd;

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
        //First of all I have to check whether I am entering in a new
        //function. If we are not entering in a new function, I have
        //to check whether we are exiting from the current function;
        //if no of the two sitations happen, I do not perform anything
        if(this->processorInstance.isRoutineEntry(curInstr)){
            ProfFunction::numTotalCalls++;

            ProfFunction * curFun = NULL;
            template_map<issueWidth, ProfFunction>::iterator curFunction = this->functions.find(curPC);
            if(curFunction != this->functionsEnd){
                curFun = &(curFunction->second);
            }
            else{
                curFun = &(this->functions[curPC]);
                curFun->name = this->bfdFrontend.symbolAt(curPC).front();
            }
            currentStack.push_back(curFun);
        }
        else if(this->processorInstance.isRoutineExit(curInstr)){
            //Here I have to update the statistics for the
            //function on the top of the stack and pop it from
            //the stack
        }
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
    ///Prints the compuated statistics in the form of a csv file
    void printCsvStats(std::string fileName){

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
