#include <vector>
#include "controller.hpp"
#include "GDBStub.hpp"


namespace resp {
std::vector<GDBStubBase *> stubs;
unsigned int numStopped = 0;
boost::mutex stop_mutex;
boost::mutex cont_mutex;
double curSimTime = 0;
double timeToGo = 0;
double timeToJump = 0;
double simStartTime = 0;
#ifdef ENABLE_MYSQL
bool realtime = true;
#endif
GDBStubBase::DirectionType direction = GDBStubBase::FORWARD;
}

using namespace resp;

///Callback called by SystemC to signal to all stubs that the simulation
///has ended
void GDBSimEndCallback::operator()(){
    #ifndef NDEBUG
    std::cerr << __PRETTY_FUNCTION__ << " GDB EOS callback" << std::endl;
    #endif
    #ifdef ENABLE_MYSQL 
    if(!realtime)
        return;
    #endif
    std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
    for(stubsIter = stubs.begin(), stubsEnd = stubs.end(); 
                            stubsIter != stubsEnd; stubsIter++){
        (*stubsIter)->signalProgramEnd();
    }
}

///Callback called by the controller to signal that the simulation
///ha been paused
void GDBPauseCallback::operator()(){
    #ifdef ENABLE_MYSQL 
    if(!realtime)
        return;
    #endif
    #ifndef NDEBUG
    std::cerr << __PRETTY_FUNCTION__ << " Calling GDB pause callback" << std::endl;
    #endif
    if(stubs.size() > 0)
        stubs[0]->setStopped(GDBStubBase::PAUSED);
}

///Callback called by the controller to signal that the simulation
///timeout has expired
void GDBTimeoutCallback::operator()(){
    #ifdef ENABLE_MYSQL 
    if(!realtime)
        return;
    #endif
    #ifndef NDEBUG
    std::cerr << __PRETTY_FUNCTION__ << " Calling GDB timeout callback" << std::endl;
    #endif
    if(stubs.size() > 0)
        stubs[0]->setStopped(GDBStubBase::TIMEOUT);
}

///Callback called by SystemC to signal to all stubs that the simulation
///has ended
void GDBErrorCallback::operator()(){
    #ifndef NDEBUG
    std::cerr << __PRETTY_FUNCTION__ << " GDB Error callback" << std::endl;
    #endif
    std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
    for(stubsIter = stubs.begin(), stubsEnd = stubs.end(); 
                            stubsIter != stubsEnd; stubsIter++){
        (*stubsIter)->signalProgramEnd(true);
    }
}
