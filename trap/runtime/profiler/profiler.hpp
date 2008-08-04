#ifndef PROFILER_HPP
#define PROFILER_HPP

#include <map>
#include <string>
#include <vector>

#include "Graph.hpp"
#include "Interval.hpp"

class BFDFrontend;

namespace resp{

///Represents all the profiling data which can be
///associated with a single function
struct Function : VertexInfo{
   ///Name of the function
   std::string name;
   ///path of the file in which the function is declared
   std::string path;
   ///Number of times this function is called
   unsigned long numCalls;
   ///The number of assembly instructions executed in total (divide for numCalls to have the average)
   unsigned long long numInstr;
   ///Total time spent in the function (considering also the subfunctions called from it)
   long double totalTime;
   ///Time spent exclusively in the function (not considering also the subfunctions called from it)
   long double exclTime;
   ///dump these information to a string,  in the command separated values (CVS) format
   std::string dump(unsigned int threadId);
   ///Prints the description of the informations which describe a function,  in the command separated values (CVS) format
   static std::string printHeader();
};

///Represents all the profiling data which can be
///associated with a single assembly instruction
struct Instruction{
   ///Name of the assembly instruction (MOV, ADD ...)
   std::string name;
   ///Number of times this instruction is called
   unsigned long numCalls;
   ///Total time spent in executing the instruction
   long double time;
   ///dump these information to a string,  in the command separated values (CVS) format
   std::string dump();
   ///Prints the description of the informations which describe an instruction,  in the command separated values (CVS) format
   static std::string printHeader();
};

/**
 * Class representing the profiler, it contains all the data profiled so
 * far and all the methods necessary to perform the profiling
 */
class Profiler{
  private:
   std::string objFile;
   ///Keeps track statistics about function calls: the index of the map is the
   ///name of the function itself
   std::map<std::string, std::map<Interval *,  Function> > function;
   ///keep track of the stack of functions currently being called; for each function
   ///we have the corresponding stack pointer; note that for each thread (each
   ///thread is represented by its stack) we have a different stack
   std::map<Interval *,  std::list<std::pair<Function *,  unsigned int> > > functionStack;
   ///The current function
   Function *curFun;
   ///The current instruction
   Instruction *curInstr;
   ///Used to keep track of time
   double oldTime;
   ///Keeps the call graph
   std::map<Interval *,  Graph *> callGraph;
   ///Keeps track of statistics about single assembly instructions: the index of the
   ///map is the assembly instruction itself
   std::map<std::string, Instruction> instruction;
   ///Helper used to query and manage the symbols in the object files
   BFDFrontend *symbolManager;
   ///Specifies whether it is necessary to keep track of the call graph or not. Note
   ///that there are not problems if we use normal OS emulation; on the other hand
   ///there may be problems in case we use a real operating system,  since it is
   ///very difficult to keep track of context switches,  interrupts ...
   bool callGraphEnable;
   ///Specifies the average stack size: when there is a difference among two consecutive stacks
   ///bigger than stackSize we may assume that a context switch has happened
   unsigned int stackSize;
   ///used when adding vertices to the call graph,  it associates to each vertex a unique ID
   std::map<Interval *,  unsigned int> uniqueVertexId;
   ///Adds a new vertex to the graph (note that 1 to 1 correspondence among vertices and
   ///functions)
   vertex_t addGraphFun(Function * fun,  Interval * interval);
   ///Adds a new edge to the graph; if the edge already exists it adds a new label to it
   void addEdge(double curTime,  std::pair<Function *, Function *> vertices,  Interval * interval);
   ///Keeps track of the symbol helpers,  so that the symbol helper is not reloaded too many times if not needed
   static std::map<std::string,  BFDFrontend *> symbolManagers;
  public:
   ///Prepares to profile a given objFile using the objdump command with full path
   ///objdumpPath to extract symbols
   Profiler(std::string objFile,  bool callGraphEnable = false,  unsigned int stackSize = 2048);
   ~Profiler();
   ///Signals to the profiler that a new instruction at address is being executed
   void step(unsigned int address,  unsigned int stackPointer);
   ///Writes to file the collected statistics; they are written in a comma separated value format
   void dumpStats(std::string fileName,  std::string graphName = "");
};

}

#endif
