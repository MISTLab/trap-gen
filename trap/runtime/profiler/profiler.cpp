#include <sys/stat.h>
#include <map>
#include <iostream>
#include <string>
#include <ostream>
#include <fstream>
#include <sstream>
#include <vector>

#include "utils.hpp"

#include <systemc.h>
#include <boost/lexical_cast.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/algorithm/string.hpp>

#include "bfdFrontend.hpp"
#include "Graph.hpp"
#include "Interval.hpp"
#include "profiler.hpp"

using namespace resp;

namespace resp{
std::map<std::string,  BFDFrontend *> Profiler::symbolManagers;
}

std::string Function::printHeader(){
    std::ostringstream stream;
    stream << "Name" << ";" << "Path" << ";" << "Thread Stack" << ";" << "Number of Calls" << ";" << "Number Of Instructions" << ";" << "Total Time" << ";" << "Exclusive Time" << std::endl;
    return stream.str();
}

std::string Function::dump(unsigned int threadId){
    std::ostringstream stream;
    stream << this->name << ";" << this->path << ";" << threadId << ";" << this->numCalls << ";" << this->numInstr << ";";
    if(this->totalTime > 0)
        stream << this->totalTime;
    else
        stream << this->exclTime;
    stream << ";" << this->exclTime << std::endl;
    return stream.str();
}

std::string Instruction::printHeader(){
    std::ostringstream stream;
    stream << "Name" << ";" << "Number of Calls" << ";" << "Total Time" << std::endl;
    return stream.str();
}

std::string Instruction::dump(){
    std::ostringstream stream;
    stream << this->name << ";" << this->numCalls << ";" << this->time << std::endl;
    return stream.str();
}

///Prepares to profile a given objFile using the objdump command with full path
///objdumpPath to extract symbols
Profiler::Profiler(std::string objFile, bool callGraphEnable, unsigned int stackSize) : objFile(objFile), curFun(NULL), curInstr(NULL), 
                                                                                                         callGraphEnable(callGraphEnable),  stackSize(stackSize){
    struct stat buffer;
    if ( stat(objFile.c_str(), &buffer )  != 0){
        THROW_EXCEPTION("File " << objFile.c_str() << " not found");
    }
    if(Profiler::symbolManagers.find(this->objFile) == Profiler::symbolManagers.end()){
        Profiler::symbolManagers[this->objFile] = new BFDFrontend(objFile, true);
    }
    this->symbolManager = Profiler::symbolManagers[this->objFile];
}

Profiler::~Profiler(){
    if(Profiler::symbolManagers[this->objFile] != NULL){
        Profiler::symbolManagers[this->objFile] = NULL;
        delete this->symbolManager;
    }
}

///Signals to the profiler that a new instruction at address is being executed
void Profiler::step(unsigned int address,  unsigned int stackPointer){
    //First of all I get all the necessary information regarding the current
    //program counter
    //std::cerr << "Starting the statistics computations - " << this  << std::endl;
    std::string curFunction = this->symbolManager->symbolAt(address).front();
    boost:: replace_all(curFunction, "\t", " ");
    std::string assembly;
    assembly = this->symbolManager->getAssembly(address);
    std::size_t lastSemCol = assembly.rfind(';');
    if(lastSemCol != std::string::npos)
        assembly = assembly.substr(0, lastSemCol);
    std::size_t toTrim = assembly.find_last_not_of(" \t");
    #ifndef NDEBUG
    if(toTrim == std::string::npos)
        THROW_EXCEPTION("No character different from space or tab found " << assembly);
    #endif
    assembly = assembly.substr(0, toTrim + 1);
    boost:: replace_all(assembly, "\t", " ");
    if(assembly[assembly.size() - 1] == '\n')
        assembly = assembly.substr(0, assembly.size() - 1);
    double newTime = sc_time_stamp().to_double();
    bool newInstruction = false;
    
    //Now finally I can update the status of the profiler with the newly read data; 
    //Dealing with the instructions now
    if(this->curInstr != NULL){
        this->curInstr->time += (newTime - this->oldTime);
    }
    if(this->curInstr == NULL || this->curInstr->name != assembly){
        if(this->instruction.find(assembly) == this->instruction.end()){
            Instruction newInstr;
            newInstr.name = assembly;
            newInstr.numCalls = 0;
            newInstr.time = 0;
            this->instruction[assembly] = newInstr;
        }
        newInstruction = true;
        this->curInstr = &(this->instruction[assembly]);
        this->curInstr->numCalls++;
    }
    
    //Now we can deal with functions; the trick is a bit more complicated since if we want to draw the call
    //graph,  we need also to keep track of the order in which the various functions are called. To represent
    //a call graph we use a boost graph; each edge in the graph is annotate with the time at which
    //the call takes place. Note that at each time functionStack contains the current stack of
    //the calls; every time there is a new call,  if the value of SP is smaller than the last one on
    //the stack it goes on top of that,  otherwise it means that the call currently on top has
    //ended and it must be popped out. Note that we do all these operations only if we decidede to
    //keep track of the call graph
    if(this->callGraphEnable){
        std::string file;
        unsigned int line = 0;
        this->symbolManager->getSrcFile(address, file, line);
        boost:: replace_all(file, "\t", " ");

        Function * curPseudoFunction = NULL;
        //Creating the call graph and keeping track of the function calls
        if(this->functionStack.empty()){
            //std::cerr << "Beginning: creating new stack element " << stackPointer << "   " << Interval::dumpIntervals() << " - " << this  << std::endl;
            //ok,  I'm at the beginning of simulation: I have to add a new stack element
            //Lets create it
            Interval * newStackElem = Interval::getInterval(stackPointer,  this->stackSize).first;
            //std::cerr << "Acquired new stack elem   " << Interval::dumpIntervals() << " - " << this  << std::endl;
            //First of all I create the function; note that this means also adding a new
            //element to the graph
            Function fun;
            fun.name = curFunction;
            fun.path =  file + " line: " + boost::lexical_cast<std::string>(line);
            fun.numCalls = 1;
            fun.numInstr =0;
            fun.totalTime = 0;
            fun.exclTime = 0;
            this->function[curFunction][newStackElem] = fun;
            //Adding element to the graph
            Graph * g = new Graph();
            this->callGraph[newStackElem] = g;
            this->addGraphFun(&this->function[curFunction][newStackElem],  newStackElem);
            //Finally I add the element to the current stack
            std::pair<Function *,  unsigned int> stackElem(&this->function[curFunction][newStackElem],  stackPointer);
            this->functionStack[newStackElem].push_front(stackElem);
        }
        else{
             //First of all I have to determine which thread I'm in (for this I have to determine the
             //interval corresponding to the current stack pointer)
             //std::cerr << "Trying to get another interval " << stackPointer << "   " << Interval::dumpIntervals() << " - " << this  << std::endl;
             std::pair<Interval *,  bool> curInterval = Interval::getInterval(stackPointer,  this->stackSize);
             if(curInterval.second){
                  //Already existing interval: I simply update it with the new stack address
                  //std::cerr << "Updating existing interval " << stackPointer << "   " << Interval::dumpIntervals() << " - " << this  << std::endl;
                  curInterval.first->update(stackPointer);
                  //std::cerr << "Updated interval " << stackPointer << "   " << Interval::dumpIntervals() << " - " << this  << std::endl;
             }
             
             //Interval never seen before: this means that I'm in a new thread: I consequently
              //add a new stack and call graph
              if(this->callGraph.find(curInterval.first) == this->callGraph.end()){
                  Graph * g = new Graph();
                  this->callGraph[curInterval.first] = g;
                  std::list<std::pair<Function *,  unsigned int> > curList;
                  this->functionStack[curInterval.first] = curList;
                  //std::cerr << "new Interval " << stackPointer << "   " << Interval::dumpIntervals() << " - " << this  << std::endl;
              }

             //Now I have the current stack; I also get the string identifying the current function;
             //if it is a new function (not present in the function map for the current thread) I
             //have to add it and add it also to the corresponding call graph
             //Now I examine the current stack: if current stack pointer is smaller than the
             //one of the function on top I add this new function on top and I add an arrow among
             //the two functions (if it already exists I simply update the label): it means that the 
             //function was called from the one on top). Otherwise the current function replaces
             //the one on top and an arrow is added from the last two functions of the stack.
             //After i have rebuilt the stack I go over it and I update the counters for the functions
             if(this->function.find(curFunction) == this->function.end() || 
                this->function[curFunction].find(curInterval.first) == this->function[curFunction].end()){
                 //I have to add the new function
                 Function fun;
                 fun.name = curFunction;
                 fun.path =  file + " line: " + boost::lexical_cast<std::string>(line);
                 fun.numCalls = 1;
                 fun.numInstr =0;
                 fun.totalTime = 0;
                 fun.exclTime = 0;
                 this->function[curFunction][curInterval.first] = fun;
                 //Adding element to the graph
                 //Graph * g = new Graph();
                 //this->callGraph[curInterval.first] = g;
                 this->addGraphFun(&this->function[curFunction][curInterval.first],  curInterval.first);
             }
             //Now I'm going to examine and update the call stack and the statistics about the
             //function
             std::list<std::pair<Function *,  unsigned int> > & curStack = functionStack[curInterval.first];
             if(curStack.empty()){
                //There is nothing on the stack: I simply have to add this function
                std::pair<Function *,  unsigned int> curStackElem(&this->function[curFunction][curInterval.first],  stackPointer);
                curStack.push_front(curStackElem);
             }
             else{
                  //I have to check the stack and eventually update it; I also update the function statistics
                  //TODO: NOTE THAT SO FAR WE ARE NOT ABLE TO DEAL WITH DIRECT RECURSIVE FUNCTIONS: THE 
                  //PROBLEM IS THAT THE STACK POINTER IS NOT UPDATED AS SOON AS WE ENTER IN A FUNCTION, 
                  //BUT AFTER A COUPLE OF INSTRUCTIONS: SO,  SINCE THE STACK POINTER IS THE ONLY THING
                  //THAT CHANGES IN A RECURSIVE FUNCTION,  WE HAVE NO MEANS TO KNOW IF THE STACK POINTER
                  //IS CHANGING BECAUSE OF RECURSION OR SIMPLY BECAUSE WE ARE MOVING INSIDE THE FUNCTION
                  if(curStack.front().first->name != curFunction){
                     //I have to update the stack: either adding a new element (new function call) or returning
                     //from it
                     if(stackPointer < curStack.front().second){
                        //New function call
                        std::pair<Function *,  unsigned int> stackElem(&this->function[curFunction][curInterval.first],  stackPointer);
                        //std::cerr << "stack top: " << curStack.front().first->name << " - " << curStack.front().second << " - " << this << std::endl;
                        //std::cerr << " cur fun " << curFunction << " adding edge among " << curStack.front().first->name << " and " << this->function[curFunction][curInterval.first].name << " cur stack " << stackPointer << " address " << std::hex <<  address << std::dec << " - " << this << std::endl;
                        std::pair<Function *,  Function *> newCall(curStack.front().first,  &this->function[curFunction][curInterval.first]);
                        curStack.push_front(stackElem);
                        curStack.front().first->numCalls++;
                        //I also have to add the edge to the graph
                        this->addEdge(newTime,  newCall,  curInterval.first);
                     }
                     else if(stackPointer > curStack.front().second){
                          //Returning from the call
                          //std::cerr << "popping " << curStack.front().first->name  << " stack " << stackPointer << " old stack " << curStack.front().second  << " address " << std::hex <<  address << std::dec << " - " << this << std::endl;
                          curStack.pop_front();
                          #ifndef NDEBUG
                          if(!curStack.empty() && curStack.front().first->name != curFunction && stackPointer < curStack.front().second){
                             std::pair<Function *,  unsigned int> stackElem(&this->function[curFunction][curInterval.first],  stackPointer);
                             //std::cerr << "stack top: " << curStack.front().first->name << " - " << curStack.front().second << " - " << this << std::endl;
                             //std::cerr << " cur fun " << curFunction << " adding edge among " << curStack.front().first->name << " and " << this->function[curFunction][curInterval.first].name << " cur stack " << stackPointer << " address " << std::hex <<  address << std::dec << " - " << this << std::endl;
                             std::pair<Function *,  Function *> newCall(curStack.front().first,  &this->function[curFunction][curInterval.first]);
                             curStack.push_front(stackElem);
                             curStack.front().first->numCalls++;
                             //I also have to add the edge to the graph
                             this->addEdge(newTime,  newCall,  curInterval.first);
                          }
                          #endif
                     }
                     else{
                          //It is a kind of function call,  but the stack pointer wasn't modified for it; I put it in a temporary variable
                          //so that the statistics for this function can be separately updated
                          curPseudoFunction = &this->function[curFunction][curInterval.first];
                    }
                 }
                 else{ //if(stackPointer < curStack.front().second){
                      //I update the stack pointer with the new value
                      //std::cerr << "updating stack: " << curStack.front().first->name << " - " << curStack.front().second << " into " << stackPointer << " PC " << std::hex <<  address << std::dec << " - " << this <<std::endl;
                      curStack.front().second = stackPointer;
                }
             }
             //Finally now i can go over the stack and update the function statistics
             std::list<std::pair<Function *,  unsigned int> >::iterator curStackIter,  curStackIterEnd;
             for(curStackIter = curStack.begin(),  curStackIterEnd = curStack.end(); curStackIter != curStackIterEnd; curStackIter++){
                 Function * fun = curStackIter->first;
                 fun->totalTime += (newTime - this->oldTime);
             }
             //Note that the exclusive time and the number of instructions are updated only for the function on top of the stack
             if(!curStack.empty() && curPseudoFunction == NULL){
                 curStack.front().first->exclTime += (newTime - this->oldTime);
                 if(newInstruction)
                     curStack.front().first->numInstr++;
             }
             else if(curPseudoFunction != NULL){
                 curStack.front().first->exclTime += (newTime - this->oldTime);
                 if(newInstruction)
                     curStack.front().first->numInstr++;
             }
        }
    }
    else{
        //Keeping simple statistics on the functions
        if(this->curFun != NULL){
            this->curFun->exclTime += (newTime - this->oldTime);
        }
        if(this->curFun == NULL || this->curFun->name != curFunction){
            if(this->function.find(curFunction) == this->function.end()){
                std::string file;
                unsigned int line = 0;
                this->symbolManager->getSrcFile(address, file, line);
                boost:: replace_all(file, "\t", " ");

                Function newFun;
                newFun.name = curFunction;
                newFun.path = file + ":" + boost::lexical_cast<std::string>(line);
                newFun.numInstr = 0;
                newFun.numCalls = 0;
                newFun.totalTime = 0;
                newFun.exclTime = 0;
                this->function[curFunction][nullInterval] = newFun;
            }
            this->curFun = &(this->function[curFunction][nullInterval]);
        }
        if(newInstruction)
            this->curFun->numInstr++;
    }
    this->oldTime = newTime;
}

///Writes to file the collected statistics; they are written in a comma separated value format
void Profiler::dumpStats(std::string fileName,  std::string graphName){
    //Printing functions
    std::ofstream fileOut(std::string("funs_" + fileName).c_str(), std::ios::out);
    fileOut << Function::printHeader();
    std::map<std::string, std::map<Interval *,  Function> >::iterator funIter,  funIterEnd;
    for(funIter = this->function.begin(),  funIterEnd = this->function.end(); funIter !=  funIterEnd; funIter++){
        std::map<Interval *,  Function>::iterator funThIter,  funThIterEnd;
        for(funThIter = funIter->second.begin(),  funThIterEnd = funIter->second.end(); funThIter !=  funThIterEnd; funThIter++){
            if(funThIter->first != NULL)
                fileOut << funThIter->second.dump(funThIter->first->getId());
            else
                fileOut << funThIter->second.dump(0);
        }
    }
    fileOut.close();
        
    //printing instructions
    std::ofstream fileOut1(std::string("instr_" + fileName).c_str(), std::ios::out);
    std::map<std::string, Instruction>::iterator instrIter,  instrIterEnd;
    fileOut1 << Instruction::printHeader();
    for(instrIter = this->instruction.begin(),  instrIterEnd = this->instruction.end(); instrIter !=  instrIterEnd; instrIter++){
        fileOut1 << instrIter->second.dump();
    }
    fileOut1.close();
    //Creating instruction summary
    std::ofstream instr_sum(std::string("instr_summary_" + fileName).c_str(), std::ios::out);
    instr_sum << Instruction::printHeader();
    std::map<std::string, std::pair<unsigned long, long double> > instruSum;
    for(instrIter = this->instruction.begin(),  instrIterEnd = this->instruction.end(); instrIter !=  instrIterEnd; instrIter++){
        std::size_t nameEnd = instrIter->first.find(' ');
        std::string instrName;
        if(nameEnd != std::string::npos)
            instrName = instrIter->first.substr(0, nameEnd);
        else
            instrName = instrIter->first;
        std::map<std::string, std::pair<unsigned long, long double> >::iterator foundName = instruSum.find(instrName);
        if(foundName != instruSum.end()){
            foundName->second.first += instrIter->second.numCalls;
            foundName->second.second += instrIter->second.time;
        }
        else{
            instruSum.insert(std::pair<std::string, std::pair<unsigned long, long double> >(instrName, 
                std::pair<unsigned long, long double>(instrIter->second.numCalls, instrIter->second.time)));
        }
    }
    std::map<std::string, std::pair<unsigned long, long double> >::iterator sumBeg, sumEnd;
    for(sumBeg = instruSum.begin(), sumEnd = instruSum.end(); sumBeg != sumEnd; sumBeg++){
        instr_sum << sumBeg->first << ";" << sumBeg->second.first << ";" << sumBeg->second.second << std::endl;
    }
    instr_sum.close();
    
    //printing the call graph
    if(graphName != "" && this->callGraphEnable){
        std::map<Interval *,  Graph *>::iterator graphIter,  graphIterEnd;
        for(graphIter = this->callGraph.begin(),  graphIterEnd = this->callGraph.end(); graphIter !=  graphIterEnd; graphIter++){
            std::ofstream graphOut((boost::lexical_cast<std::string>(graphIter->first->getId()) + graphName).c_str());
            boost::write_graphviz(graphOut,  *graphIter->second,  NodeWriter(*graphIter->second),  EdgeWriter(*graphIter->second));
            graphOut.close();
        }
    }
    
    //printing the list of the stacks
    std::ofstream intervalOut(std::string("stack_" + fileName).c_str(), std::ios::out);
    intervalOut << Interval::dumpIntervals();
    intervalOut.close();
}

vertex_t Profiler::addGraphFun(Function * fun,  Interval * interval){
    #ifndef NDEBUG
    if(this->callGraph.find(interval) == this->callGraph.end())
        THROW_EXCEPTION("Graph not found for the particular interval during node addition");
    #endif
   //map associating an id to each node of the graph
   vertex_index_pmap_t tgIndexMap = boost::get(boost::vertex_index_t(), *this->callGraph[interval]);

   //Add the vertex
   vertex_t newVertex = boost::add_vertex(*this->callGraph[interval]);
   tgIndexMap[newVertex] = this->uniqueVertexId[interval];
   this->uniqueVertexId[interval]++;
   
   //Setting its properties
   boost::property_map<Graph, node_info_t>::type nodeInfo = boost::get(node_info_t(), *this->callGraph[interval]);
   nodeInfo[newVertex] = fun;
   //std::cerr << "adding vertex graph " << fun->name << " vertex " << newVertex << " Interval " << interval->dump() << " id " << this->uniqueVertexId[interval] << " num vert " << boost::num_vertices(*this->callGraph[interval]) << " - " << this << std::endl;
   
   return newVertex;
}

void Profiler::addEdge(double curTime,  std::pair<Function *, Function *> vertices,  Interval * interval){
    #ifndef NDEBUG
    if(this->callGraph.find(interval) == this->callGraph.end())
        THROW_EXCEPTION("Graph not found for the particular interval during edge addition");
    #endif
    //First of all I have to determine the vertices which correspond to the functions which I
    //want to connect
    boost::property_map<Graph, node_info_t>::type nodeInfo = boost::get(node_info_t(), *this->callGraph[interval]);
    vertex_t firstFun = 0,  secondFun = 0;
    vertex_iterator v, vIter;
    for(boost::tie(v, vIter) = boost::vertices(*this->callGraph[interval]); v != vIter; v++){
        if(nodeInfo[*v] == vertices.first)
            firstFun = *v;
        if(nodeInfo[*v] == vertices.second)
            secondFun = *v;
    }
    #ifndef NDEBUG
    if(firstFun == 0)
        THROW_EXCEPTION("First vertex not found in the graph");
    if(secondFun == 0)
        THROW_EXCEPTION("Second vertex not found in the graph");
    #endif
    
    //Now I look for the edge: in case it does not exist I create it,  otherwise I simply update its properties
    std::pair<edge_t, bool> foundEdge = boost::edge(firstFun, secondFun, *this->callGraph[interval]);
    edge_t curEdge = foundEdge.first;
   if(!foundEdge.second){
       //Finally I make the connection...
       edge_t e;
       bool inserted;
       std::vector<double> edgeProps;
       boost::tie(e, inserted) = boost::add_edge(firstFun, secondFun, edgeProps, *this->callGraph[interval]);
       curEdge = e;
   }
   //Now I can set the properties of the edge: this means pushing the current calling time
   //in the vector
   boost::property_map<Graph, edge_info_t>::type edgeInfo = boost::get(edge_info_t(), *this->callGraph[interval]);
   edgeInfo[curEdge].push_back(curTime);
}
