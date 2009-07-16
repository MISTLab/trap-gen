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
#include <fstream>
#include <iostream>

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
    typename template_map<issueWidth, ProfFunction> functions;
    std::vector<ProfFunction *> currentStack;
    sc_time oldFunTime;
    unsigned int oldFunInstructions;
    typename template_map<issueWidth, ProfFunction>::iterator functionsEnd;
    //names of the routines which should be ignored from
    //entry or exit
    std::set<std::string> ignored;

    issueWidth prevPC;

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
        unsigned int instrId = curInstr->getId();
        template_map<unsigned int, ProfInstruction>::iterator foundInstr = this->instructions.find(instrId);
        if(foundInstr != this->instructionsEnd){
            foundInstr->second.numCalls++;
            this->oldInstruction = &(foundInstr->second);
        }
        else{
            this->instructions[instrId].name = curInstr->getInstructionName();
            this->oldInstruction = &(this->instructions[instrId]);
            this->instructionsEnd = this->instructions.end();
        }
    }
    ///Based on the new instruction just issued, the statistics on the functions
    ///are updated
    inline void updateFunctionStats(const issueWidth &curPC, const InstructionBase *curInstr) throw(){
        std::vector<ProfFunction *>::iterator stackIterator, stackEnd;

        //First of all I have to check whether I am entering in a new
        //function. If we are not entering in a new function, I have
        //to check whether we are exiting from the current function;
        //if no of the two sitations happen, I do not perform anything
        if(this->processorInstance.isRoutineEntry(curInstr)){
            std::string funName = this->bfdInstance.symbolAt(curPC);
            if(this->ignored.find(funName) != this->ignored.end()){
                this->oldFunInstructions++;
                return;
            }
            ProfFunction::numTotalCalls++;
            ProfFunction * curFun = NULL;
            typename template_map<issueWidth, ProfFunction>::iterator curFunction = this->functions.find(curPC);
            if(curFunction != this->functionsEnd){
                curFun = &(curFunction->second);
                curFun->numCalls++;
            }
            else{
                curFun = &(this->functions[curPC]);
                this->functionsEnd = this->functions.end();
                curFun->name = funName;
                curFun->address = curPC;
            }
            curFun->exclNumInstr++;
            curFun->totalNumInstr++;

            std::cerr << "entering in " << curFun->name << " " << std::hex << std::showbase << curPC << std::endl;

            //Now I have to update the statistics on the number of instructions executed on the
            //instruction stack so far
            sc_time curTimeDelta = sc_time_stamp() - this->oldFunTime;

            if(this->currentStack.size() > 0){
                std::cerr << "from " << this->currentStack.back()->name << " " << std::hex << std::showbase << this->prevPC << std::endl;
                this->currentStack.back()->exclNumInstr += this->oldFunInstructions;
                this->currentStack.back()->exclTime += curTimeDelta;
            }

            for(stackIterator = this->currentStack.begin(), stackEnd = this->currentStack.end(); stackIterator != stackEnd; stackIterator++){
                if(!(*stackIterator)->alreadyExamined){
                    (*stackIterator)->totalNumInstr += this->oldFunInstructions;
                    (*stackIterator)->totalTime += curTimeDelta;
                    (*stackIterator)->alreadyExamined = true;
                }
            }
            // finally I can push the element on the stack
            this->currentStack.push_back(curFun);
            //..and record the call time of the function
            this->oldFunTime = sc_time_stamp();
            this->oldFunInstructions = 0;
            //and reset the aòready examined flag
            for(stackIterator = this->currentStack.begin(), stackEnd = this->currentStack.end(); stackIterator != stackEnd; stackIterator++){
                (*stackIterator)->alreadyExamined = false;
            }
        }
        else if(this->processorInstance.isRoutineExit(curInstr)){
            std::string funName = this->bfdInstance.symbolAt(curPC);
            if(this->ignored.find(funName) != this->ignored.end()){
                this->oldFunInstructions++;
                return;
            }
            //Here I have to update the timing statistics for the
            //function on the top of the stack and pop it from
            //the stack
            #ifndef NDEBUG
            if(this->currentStack.size() == 0){
                THROW_ERROR("We are exiting from a routine at address " << std::hex << std::showbase << curPC << " name: " << this->bfdInstance.symbolAt(curPC) << " but the stack is empty");
            }
            #endif
            //Lets update the statistics for the current instruction
            ProfFunction * curFun = this->currentStack.back();
            curFun->exclNumInstr += this->oldFunInstructions;
            sc_time curTimeDelta = sc_time_stamp() - this->oldFunTime;
            curFun->exclTime += curTimeDelta;

            std::cerr << "exiting from " << curFun->name << " " << std::hex << std::showbase << this->prevPC << std::endl;

            //Now I have to update the statistics on the number of instructions executed on the
            //instruction stack
            for(stackIterator = this->currentStack.begin(), stackEnd = this->currentStack.end(); stackIterator != stackEnd; stackIterator++){
                if(!(*stackIterator)->alreadyExamined){
                    (*stackIterator)->totalNumInstr += this->oldFunInstructions;
                    (*stackIterator)->totalTime += curTimeDelta;
                    (*stackIterator)->alreadyExamined = true;
                }
            }
            //I restore the already examined flag
            for(stackIterator = this->currentStack.begin(), stackEnd = this->currentStack.end(); stackIterator != stackEnd; stackIterator++){
                (*stackIterator)->alreadyExamined = false;
            }
            //Now I pop the instruction from the stack
            this->currentStack.pop_back();
            #ifndef NDEBUG
            if(this->currentStack.size() > 0){
                if(this->currentStack.back()->name != this->bfdInstance.symbolAt(curPC)){
                    THROW_ERROR("Error, we are into a function different from the one on our fake stack: " << this->currentStack.back()->name << " != " << this->bfdInstance.symbolAt(curPC));
                }
                std::cerr << "going into " << this->currentStack.back()->name << " " << std::hex << std::showbase << curPC << std::endl;
            }
            #endif
        }
        else{
            this->oldFunInstructions++;
        }
        this->prevPC = curPC;
    }
  public:
    Profiler(ABIIf<issueWidth> &processorInstance, std::string execName) : processorInstance(processorInstance),
                                                                    bfdInstance(BFDFrontend::getInstance(execName)){
        this->oldInstruction = NULL;
        this->oldInstrTime = SC_ZERO_TIME;
        this->instructionsEnd = this->instructions.end();
        this->oldFunTime = SC_ZERO_TIME;
        this->functionsEnd = this->functions.end();
        this->oldFunInstructions = 0;
    }

    ~Profiler(){
    }

    ///Prints the compuated statistics in the form of a csv file
    void printCsvStats(std::string fileName){
        //I simply have to iterate over the encountered functions and instructions
        //and print the relative statistics.
        //two files will be created: fileName_fun.csv and fileName_instr.csv
        std::ofstream instructionFile((fileName + "_instr.csv").c_str());
        instructionFile << ProfInstruction::printCsvHeader() << std::endl;
        template_map<unsigned int, ProfInstruction>::iterator instrIter, instrEnd;
        for(instrIter = this->instructions.begin(), instrEnd = this->instructions.end(); instrIter != instrEnd; instrIter++){
            instructionFile << instrIter->second.printCsv() << std::endl;
        }
        instructionFile.close();

        std::ofstream functionFile((fileName + "_fun.csv").c_str());
        functionFile << ProfFunction::printCsvHeader() << std::endl;
        typename template_map<issueWidth, ProfFunction>::iterator funIter, funEnd;
        for(funIter = this->functions.begin(), funEnd = this->functions.end(); funIter != funEnd; funIter++){
            functionFile << funIter->second.printCsv() << std::endl;
        }
        functionFile.close();
    }

    ///Function called by the processor at every new instruction issue.
    bool newIssue(const issueWidth &curPC, const InstructionBase *curInstr) throw(){
        this->updateInstructionStats(curPC, curInstr);
        this->updateFunctionStats(curPC, curInstr);

        return false;
    }

    void addIgnoredFunction(std::string &toIgnore){
        this->ignored.insert(toIgnore);
    }
    void addIgnoredFunctions(const std::set<std::string> &toIgnore){
        this->ignored.insert(toIgnore.begin(), toIgnore.end());
    }
};

}

#endif
