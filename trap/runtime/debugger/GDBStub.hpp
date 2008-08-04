/**
* This file contains the methods necessary to communicate with GDB in
* order to debug software running on simulators. Source code takes inspiration
* from the linux kernel (sparc-stub.c) and from ac_gdb.H in the ArchC sources
*/

#ifndef GDBSTUB_HPP
#define GDBSTUB_HPP

#include <vector>
#include <cassert>
#include <cmath>
#include <signal.h>
#include <boost/thread/thread.hpp>
#include <boost/thread/xtime.hpp>
#include <boost/thread/condition.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/lexical_cast.hpp>

#include "utils.hpp"

#include "controller.hpp"
#include "callback.hpp"

#include "BreakpointManager.hpp"
#include "GDBConnectionManager.hpp"
#include "processorInterface.hpp"

#include "MySQL.hpp"

/**
 * Base class for the GDB stub; it is used only to enable the
 * insertion of instances in the vector below.
 */

namespace resp {

class GDBStubBase{
  public:
   ///Manages connection among the GDB target stub (this class) and
   ///the GDB debugger
   GDBConnectionManager connManager;
   ///Enumeration type, describes the reasons why simulation stopped;
   enum stopType {BREAK=0, STEP, SEG, TIMEOUT, PAUSED, UNK};
   ///Current debugging direction
   enum DirectionType {FORWARD=0, BACKWARD};
   GDBStubBase(bool endianess, unsigned int verbosityLevel) : connManager(endianess,  verbosityLevel){}
   virtual ~GDBStubBase(){}
   virtual void signalProgramEnd(bool error = false){}
   virtual void setStopped(stopType stopReason = UNK){}
};

///Callback called by SystemC to signal to all stubs that the simulation
///has ended
class GDBSimEndCallback : public EOScallback{
  public:
   void operator()();
};

///Callback called by SystemC to signal to all stubs that the simulation
///has ended
class GDBErrorCallback : public ErrorCallback{
  public:
   void operator()();
};

///Callback called by the controller to signal that the simulation
///has been paused
class GDBPauseCallback : public PauseCallback{
  public:
   void operator()();
};

///Callback called by the controller to signal that the simulation
///timeout has expired
class GDBTimeoutCallback : public TimeoutCallback{
  public:
   void operator()();
};

extern std::vector<GDBStubBase *> stubs;
extern unsigned int numStopped;
///Contains the current simulation time; when the GDB stub stops,  it might be that
///we want simulation to go on (this just if MYSQL is enabled): this way simulation
///continues (faster) but we might debug a given simulation time
extern double curSimTime;
///In case we decided to run the simulation only for a limited ammount of time
///this variable contains that time
extern double timeToGo;
///In case we decided to jump onwards or backwards for a specified ammount of time,
///this variable contains that time
extern double timeToJump;
///In case the simulation is run only for a specified ammount of time,  this variable
///contains the simulation time at that start time
extern double simStartTime;
///Specifies the direction of the current simulation; the default direction is, of course, forward.
extern GDBStubBase::DirectionType direction;
#ifdef ENABLE_MYSQL
///Specifies if the debugging is happening in realtime (we are debugging the simulation at the last
///simulation time) or if we are using the history (we are debugging in the past)
extern bool realtime;
#endif
///Mutex which controls the access to the setStopped method
extern boost::mutex stop_mutex;
///Mutex which controls the access to the continue method
extern boost::mutex cont_mutex;

#ifdef ENABLE_MYSQL
template <class T> bool sortEventsAsc(const std::pair<double,  Breakpoint<T> *> & a, const std::pair<double,  Breakpoint<T> *> &b) {
    return a.first < b.first;
}

template <class T> bool sortEventsDesc(const std::pair<double,  Breakpoint<T> *> & a, const std::pair<double,  Breakpoint<T> *> &b) {
    return a.first > b.first;
}
#endif

/**
 * GDB stub: it provides responsed to the commands issued by GDB debugger
 */
template <class AddressType> class GDBStub : public GDBStubBase{
  private:
  struct ConnectionThread{
    GDBStub<AddressType> *mystub;
    ConnectionThread(GDBStub<AddressType> *mystub) : mystub(mystub){}
    void operator()(){
        mystub->connManager.initialize(mystub->port);
        //Now I have to listen for incoming GDB messages; this will
        //be done in a new thread, so that the console remains responsive;
        //I also have to signal that the current processor is
        //stopped (obviously, since SystemC hasn't been started yet)
        numStopped++;
        mystub->isGDBConnected = true;
        mystub->startThread();
    }
  };
  
  
   /// Sets the stub to test mode
   bool test;

   bool endianess;
   ///Instance of the interface to access the processor linked to
   ///this stub
   processorInterface<AddressType> &proc;
   ///Handles the breakpoints which have been set in the system
   BreakpointManager<AddressType> breakManager;
   ///Instance of the controller of SystemC simulation
   sc_controller & simController;
   ///The port on which the communication will take place
   unsigned int port;
   ///Determines whether the processor has to halt as a consequence of a
   ///step command
   unsigned int step;
   ///Keeps track of the last breakpoint encountered by this processor
   Breakpoint<AddressType> * breakReached;
   ///Specifies whether the watchpoints and breakpoints are enabled or not
   bool breakEnabled;
   ///Specifies whether GDB server side killed the simulation
   bool isKilled;
   ///Specifies whether GDB server side is waiting for input from the user
   bool isWaiting;
   ///Level of verbosity of the debug messages
   unsigned int verbosityLevel;
   ///True if GDB is connected to this stub
   bool isGDBConnected;
   bool stepCalled;
   #ifdef ENABLE_MYSQL
   ///The breakpoints already examined
   std::vector<AddressType> seenBreaks;
   MySQL mySQLinstance;
   #endif

   /**
    * Thread used to send and receive responses with the GDB debugger
    */
   struct GDBThread{
      GDBStub<AddressType> &stub;

      GDBThread(GDBStub<AddressType> &stub) : stub(stub){}

      /**
       * Main body of the thread: it simply waits for GDB requests
       * and takes the appropriate actions once the requests are decoded
       */
      void operator()(){
         while(stub.waitForRequest())
            ;
      }
   };

  public:
   GDBStub(processorInterface<AddressType> &proc, unsigned int port = 1500, unsigned int verbosityLevel = 1, bool test=false) :
                                         GDBStubBase(proc.get_ac_tgt_endian(), verbosityLevel),   endianess(proc.get_ac_tgt_endian()), proc(proc), simController(*controllerInstance), port(port),
                                         step(0), breakReached(NULL), breakEnabled(true), isKilled(false), isWaiting(true), verbosityLevel(verbosityLevel), stepCalled(false){
      stubs.push_back(this);
      this->test=test;
      GDBEnabled = true;
   }

   ///Checks if a breakpoint is present at the current address and
   ///in case it halts execution
   inline void checkBreakpoint(const AddressType address){
      #ifdef ENABLE_MYSQL
      if(!realtime)
        return;
      #endif
      if(!this->isGDBConnected)
        return;
      if(this->breakEnabled && this->breakManager.hasBreakpoint(address)){
         breakReached = this->breakManager.getBreakPoint(address);
         #ifndef NDEBUG
         if(breakReached == NULL){
            std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
            for(stubsIter = stubs.begin(), stubsEnd = stubs.end();
                                    stubsIter != stubsEnd; stubsIter++)
                (*stubsIter)->signalProgramEnd(true);
            THROW_EXCEPTION("I stopped because of a breakpoint, but no breakpoint was found");
         }
         if(verbosityLevel >= 2)
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Stopping because of breakpoint at address " << address << std::endl;
         #endif
         this->setStopped(BREAK);
         this->stepCalled = true;
       }
   }

   ///Checks if execution must be stopped because of a step command
   inline void checkStep(){
      #ifdef ENABLE_MYSQL
      if(!realtime)
        return;
      #endif
      if(!this->isGDBConnected)
        return;
      if(this->step == 1)
         this->step++;
      else if(this->step == 2){
         #ifndef NDEBUG
         if(verbosityLevel >= 2)
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Stopping because of STEP" << std::endl;
         #endif
         this->step = 0;
         this->setStopped(STEP);
      }
   }

   ///Listens for GDB connections and creates a new thread which will deal with them
   void initialize(){
      //Now I have to start listening for GDB connections
      if(!test) {
        this->connManager.initialize(this->port);
        //Now I have to listen for incoming GDB messages; this will
        //be done in a new thread, so that the console remains responsive;
        //I also have to signal that the current processor is
        //stopped (obviously, since SystemC hasn't been started yet)
        numStopped++;
        this->isGDBConnected = true;
        sc_controller::disableLatency = true;
        this->startThread();
      } else{
         //I have to create the connection in a boost thread
         boost::thread thrd(ConnectionThread(this));
      }
   }

   ///This method is called when we need asynchronously halt the
   ///execution of the processor this instance of the stub is
   ///connected to; it is usually used when a processor is halted
   ///and it has to communicated to the other processor that they have
   ///to halt too; note that this method halts SystemC execution and
   //it also starts new threads (one for each processor) which will
   //deal with communication with the stub; when a continue or
   //step signal is met, then the receving thread is killed. When
   //all the threads are killed execution can be resumed (this means
   //that all GDBs pressed the resume button)
   //This method is also called at the beginning of the simulation by
   //the first processor which starts execution
   void setStopped(stopType stopReason = UNK){
        boost::mutex::scoped_lock lock(stop_mutex);
      #ifndef NDEBUG
      if(numStopped != 0){
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " ERROR, num_stopped != 0: value " << numStopped << std::endl;
            abort();
      }
      #endif
      //saving current simulation time
      #ifdef ENABLE_MYSQL
      if(realtime)
      #endif
        curSimTime = this->simController.get_simulated_time();

      //Now I have to behave differently depending on whether database support is enabled or not
      //if it is enabled I do not stop simulation,  while if it is not enabled I have to stop simulation in
      //order to be able to inspect the content of the processor - memory - etc...
      #ifdef ENABLE_MYSQL
      if(realtime){
      #endif
      //Computing the next simulation time instant
      if(timeToGo > 0){
         timeToGo -= (curSimTime - simStartTime);
         if(timeToGo < 0)
            timeToGo = 0;
         simStartTime = curSimTime;
      }
      if(timeToJump > 0){
         timeToJump -= (curSimTime - simStartTime);
         if(timeToJump < 0)
            timeToJump = 0;
         simStartTime = curSimTime;
      }
      #ifndef ENABLE_MYSQL
      //pausing simulation
      if(stopReason != TIMEOUT && stopReason !=  PAUSED)
         this->simController.pause_simulation(false);
      #endif
      #ifdef ENABLE_MYSQL
        #ifndef NDEBUG
        if(this->verbosityLevel >= 2){
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Exiting from realtime" << std::endl;
        }
        #endif
        realtime = false;
      }
      #endif
      //Disabling break and watch points
      this->breakEnabled = false;

      //Signaling to all the stubs that they can resume GDB execution
      //this way GDB becomes responsive and it is possible to start
      //debugging; now I also have to start a thread (one for each stub)
      //which deals with managing GDB requests
      if(stopReason ==  STEP){
        this->stepCalled = false;
        if(stubs.size() > 1){
            GDBResponse response;
            response.type = GDBResponse::OUTPUT;
            response.message = "In order to awake the other GDB stubs issue the command \"monitor awake\"\n";
            this->connManager.sendResponse(response);
        }
        this->awakeGDB(stopReason);
        numStopped++;
        this->startThread();
      }
      else{
          std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
          for(stubsIter = stubs.begin(), stubsEnd = stubs.end();
                                   stubsIter != stubsEnd; stubsIter++){
             if(*stubsIter == this || stopReason == TIMEOUT || stopReason ==  PAUSED){
                dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->awakeGDB(stopReason);
             }
             else{
                 //First of all I send a message to the other GDB so that it knows why it stopped
                 GDBResponse response;
                 response.type = GDBResponse::OUTPUT;
                 response.message = "Pausing GDB because a breakpoint was encountered by CPU " + this->proc.getName() + "\n";
                 (*stubsIter)->connManager.sendResponse(response);
                 dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->awakeGDB();
             }
             numStopped++;
             //Now I start the thread which will manage requests
             dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->startThread();
          }
      }
   }

   ///Starts the thread which will manage the connection with the
   ///GDB debugger
   void startThread(){
      GDBThread thread(*this);

      boost::thread th(thread);
   }

   ///Sends a TRAP message to GDB so that it is awaken
   void awakeGDB(stopType stopReason = UNK){
     switch(stopReason){
         case STEP:{
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Step: awaking GDB" << std::endl;
             #endif
            GDBResponse response;
            response.type = GDBResponse::S;
            response.payload = SIGTRAP;
            this->connManager.sendResponse(response);
         break;}
         case BREAK:{
            //Here I have to determine the case of the breakpoint: it may be a normal
            //breakpoint placed on an instruction or it may be a watch on a variable
            #ifndef NDEBUG
            if(this->breakReached == NULL){
                THROW_EXCEPTION("I stopped because of a breakpoint, but it is NULL");
            }
            #endif

            if(this->breakReached->type == Breakpoint<AddressType>::HW ||
                           this->breakReached->type == Breakpoint<AddressType>::MEM){
                #ifndef NDEBUG
                if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Break: awaking GDB" << std::endl;
                #endif
               GDBResponse response;
               response.type = GDBResponse::S;
               response.payload = SIGTRAP;
               this->connManager.sendResponse(response);
            }
            else{
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Watch: awaking GDB" << std::endl;
             #endif
               GDBResponse response;
               response.type = GDBResponse::T;
               response.payload = SIGTRAP;
               std::pair<std::string, unsigned int> info;
               info.second = this->breakReached->address;
               switch(this->breakReached->type){
                  case Breakpoint<AddressType>::WRITE:
                     info.first = "watch";
                  break;
                  case Breakpoint<AddressType>::READ:
                     info.first = "rwatch";
                  break;
                  case Breakpoint<AddressType>::ACCESS:
                     info.first = "awatch";
                  break;
                  default:
                     info.first = "none";
                  break;
               }
               response.size = sizeof(AddressType);
               response.info.push_back(info);
               this->connManager.sendResponse(response);
            }
         break;}
         case SEG:{
             //An error has occurred during processor execution (illelgal instruction, reading out of memory);
             GDBResponse response;
             response.type = GDBResponse::S;
             response.payload = SIGILL;
             this->connManager.sendResponse(response);
         break;}
         case TIMEOUT:{
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Timeout: awaking GDB" << std::endl;
             #endif
             //the simulation time specified has elapsed,  so simulation halted
             GDBResponse resp;
             resp.type = GDBResponse::OUTPUT;
             resp.message = "Specified Simulation time completed - Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
             this->connManager.sendResponse(resp);
             this->connManager.sendInterrupt();
         break;}
         case PAUSED:{
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Pause: awaking GDB" << std::endl;
             #endif
             //the simulation time specified has elapsed,  so simulation halted
             GDBResponse resp;
             resp.type = GDBResponse::OUTPUT;
             resp.message = "Simulation Paused - Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
             this->connManager.sendResponse(resp);
             this->connManager.sendInterrupt();
         break;}
         default:
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Generic Interrupt: awaking GDB" << std::endl;
             #endif
            this->connManager.sendInterrupt();
         break;
      }
   }

   ///Signals to the GDB debugger that simulation ended; the error variable specifies
   ///if the program ended with an error
   void signalProgramEnd(bool error = false){
      if((!this->isKilled && !this->isWaiting) || error){
         #ifndef NDEBUG
         if(verbosityLevel >= 2)
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Signaling program end" << std::endl;
         #endif

         GDBResponse response;
         //Now I just print a message to the GDB console signaling the user that the program is ending
         if(error){
            //I start anyway by signaling an error
            GDBResponse rsp;
            rsp.type = GDBResponse::ERROR;
            this->connManager.sendResponse(rsp);
         }
         response.type = GDBResponse::OUTPUT;
         if(error){
            response.message = "Program Ended With an Error\n";
             #ifndef NDEBUG
             std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Program Ended With an Error" << std::endl;
             #endif
             if(sc_controller::error){
                response.message += sc_controller::errorMessage + "\n";
                 #ifndef NDEBUG
                 std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Error Message: " << sc_controller::errorMessage << std::endl;
                 #endif
            }
         }
         else
            response.message = "Program Correctly Ended\n";
         this->connManager.sendResponse(response);

         //Now I really communicate to GDB that the program ended
         response.type = GDBResponse::W;
         if(error)
            response.payload = SIGABRT;
         else
            response.payload = SIGQUIT;
         this->connManager.sendResponse(response);
      }
      #ifndef NDEBUG
      else if(verbosityLevel >= 2)
         std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Program ended because of a killing request from GDB" << std::endl;
      #endif
   }

  private:
   ///Waits for an incoming request by the GDB debugger and, once it
   ///has been received, it routes it to the appropriate handler
   ///Returns whether we must be listening for other incoming data or not
   bool waitForRequest(){
      GDBRequest req = connManager.processRequest();
      bool reListen = false;
      switch(req.type){
         case GDBRequest::QUEST:
            //? request: it asks the target the reason why it halted
            reListen = this->reqStopReason();
         break;
         case GDBRequest::EXCL:
            //! request: it asks if extended mode is supported
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::c:
            //c request: Continue command
            reListen = this->cont(req);
         break;
         case GDBRequest::C:
            //C request: Continue with signal command, currently not supported
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::D:
            //D request: disconnection from the remote target
            reListen = this->detach(req);
         break;
         case GDBRequest::g:
            //g request: read general register
            reListen = this->readRegisters();
         break;
         case GDBRequest::G:
            //G request: write general register
            reListen = this->writeRegisters(req);
         break;
         case GDBRequest::H:
            //H request: multithreading stuff, not currently supported
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::i:
            //i request: single clock cycle step; currently it is not supported
            //since it requires advancing systemc by a specified ammont of
            //time equal to the clock cycle (or one of its multiple) and I still
            //have to think how to know the clock cycle of the processor and
            //how to awake again all the processors after simulation stopped again
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::I:
            //i request: signal and single clock cycle step
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::k:
            //i request: kill application: I simply call the sc_stop method
            reListen = this->killApp();
         break;
         case GDBRequest::m:
            //m request: read memory
            reListen = this->readMemory(req);
         break;
         case GDBRequest::M:
         case GDBRequest::X:
            //M request: write memory
            reListen = this->writeMemory(req);
         break;
         case GDBRequest::p:
            //p request: register read
            reListen = this->readRegister(req);
         break;
         case GDBRequest::P:
            //P request: register write
            reListen = this->writeRegister(req);
         break;
         case GDBRequest::q:
            //P request: register write
            reListen = this->genericQuery(req);
         break;
         case GDBRequest::s:
            //s request: single step
            reListen = this->doStep(req);
         break;
         case GDBRequest::S:
            //S request: single step with signal
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::t:
            //t request: backward search: currently not supported
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::T:
            //T request: thread stuff: currently not supported
            reListen = this->emptyAction(req);
         break;
         case GDBRequest::z:
            //z request: breakpoint/watch removal
            reListen = this->removeBreakpoint(req);
         break;
         case GDBRequest::Z:
            //z request: breakpoint/watch addition
            reListen = this->addBreakpoint(req);
         break;
         case GDBRequest::ERROR:
            reListen = false;
         break;
         default:
            reListen = this->emptyAction(req);
         break;
      }
      this->isWaiting = reListen;
      return reListen;
   }

   #ifdef ENABLE_MYSQL
   ///Method used to resume execution after GDB has issued
   ///the continue or step signal; note that actually this command is issued
   ///when the Database is used to keep track of what is happening in
   ///the system: since,  in this mode, the debugged time is different from the
   ///one of the execution (we can also debug back in time),  we need to use
   ///special methods
   void resumeExecution(bool step){
        boost::mutex::scoped_lock lock(cont_mutex);
        std::vector<GDBStubBase *>::iterator currentStub;
         #ifndef NDEBUG
         if(verbosityLevel >= 2)
             std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Trying to Resume Exceution numStopped: " << numStopped << std::endl;
          #endif
         numStopped--;
         if(numStopped == 0){
             //I can finally resume execution: note that actually resuming execution means simply
             //that we examine the database for the next events; in order to avoid conflicts,  race
             //conditions and stuff like that .... the simulation is stopped while the database is
             //examined
             bool wasRunning = false;
             if(!simController.is_paused() && simController.isEnded()){
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                     std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Pausing simulation" << std::endl;
                  #endif
                simController.pause_simulation(false);
                wasRunning = true;
             }
             //I set the time at which I want to perform the simulations
             if(timeToJump > 0)
                curSimTime += timeToJump;
             //Now I determine which is the next event which is going to happen in the system (breakpoint etc...)
             std::pair<double, Breakpoint<AddressType> *> event;
             event.first = -1;
             bool hasToRestart = true;
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                 std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Looking for events" << std::endl;
              #endif
             std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
            for(stubsIter = stubs.begin(), stubsEnd = stubs.end(); stubsIter != stubsEnd; stubsIter++){
                std::pair<double, Breakpoint<AddressType> *> foundEv = dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->getEvent(step);
                if(foundEv.first >= 0){
                     #ifndef NDEBUG
                     if(verbosityLevel >= 2)
                        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Found event at time: " << foundEv.first << std::endl;
                     #endif
                     #ifndef NDEBUG
                     if(verbosityLevel >= 2)
                        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Current event: " << event.first << std::endl;
                     #endif
                    hasToRestart = false;
                    if(foundEv.second == NULL || ! (foundEv.first == curSimTime && dynamic_cast<GDBStub<AddressType> *>(*currentStub)->isSeen(event.second->address))){
                        if(event.first == -1 || (foundEv.first < event.first && direction == FORWARD) || (foundEv.first > event.first && direction == BACKWARD)){
                            event = foundEv;
                            currentStub = stubsIter;
                        }
                    }
                }
                #ifndef NDEBUG
                else{
                    if(verbosityLevel >= 2)
                        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Not found event in stub" << std::endl;
                }
                #endif
            }
            if(hasToRestart){
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                     std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " No events, I have to (re)start" << std::endl;
                  #endif
                 //Ok, there are no new events: this means that simulation restarts in realtime and gdb really goes
                 //aligned with the underlying simulation
                 if(direction == FORWARD){
                     if(simController.is_running()){
                        mySQLinstance.flushEvents();
                        double lastEvent = mySQLinstance.getLastEvTime();
                         #ifndef NDEBUG
                         if(lastEvent != this->simController.get_simulated_time())
                            THROW_EXCEPTION("I expect the last event logged in the database to be at the same time of the current simulation time");
                         #endif
                         this->breakEnabled = true;
                         realtime = true;
                         if(timeToJump > 0){
                             #ifndef NDEBUG
                             if(curSimTime <= lastEvent)
                                THROW_EXCEPTION("curSimTime <= lastEvent: this should never happen");
                             #endif
                             simStartTime = lastEvent;
                             this->simController.run_simulation(curSimTime - lastEvent);
                         }
                         else if(timeToGo > 0){
                             #ifndef NDEBUG
                             if((curSimTime + timeToGo) <= lastEvent)
                                THROW_EXCEPTION("(curSimTime + timeToGo) <= lastEvent: this should never happen");
                             #endif
                             simStartTime = lastEvent;
                             this->simController.run_simulation(curSimTime + timeToGo - lastEvent);
                         }
                         else{
                             this->simController.run_simulation();
                         }
                    }
                    else if(!this->simController.hasStarted()){
                        #ifndef NDEBUG
                        if(this->verbosityLevel >= 2)
                            std::cerr << "Processor Name: " << this->proc.getName() << "Starting the simulation for the first time" << std::endl;
                        #endif
                        this->simController.run_simulation();
                    }
                    else{
                        //Ok, since simualation ended and I have nothing in the DB left for processing I can signal the simulation
                        //end to the user
                        std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
                        for(stubsIter = stubs.begin(), stubsEnd = stubs.end();
                                                stubsIter != stubsEnd; stubsIter++){
                            (*stubsIter)->signalProgramEnd();
                        }
                    }
                }
                else{
                    //I'm debugging backwards: if there are no events it simply means that
                    //I reached the beginning of the simulation; I signal the fact and give back controll
                    //to GDB
                    GDBResponse rsp;
                    rsp.type = GDBResponse::OUTPUT;
                    rsp.message = "Debugging reached the beginning of the simulation (time 0)";
                    std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
                    for(stubsIter = stubs.begin(), stubsEnd = stubs.end();
                                            stubsIter != stubsEnd; stubsIter++){
                        dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->connManager.sendResponse(rsp);
                    }
                    this->setStopped();
                }
                return;
            }

            //Ok, there are usefull events
            #ifndef NDEBUG
            if(verbosityLevel >= 2)
               std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Found usefull events in the DB: processing them"<< std::endl;
            #endif
            
            //First of all I have to check that the found event is smaller than timeToGo; if it is not
            //I have to signal to the user that simulation ended because of a timeout
            if(timeToGo > 0 && fabs(event.first - curSimTime) > timeToGo){
                #ifndef NDEBUG
                if(verbosityLevel >= 2)
                   std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Timeout: the found event is after the timeout end"<< std::endl;
                #endif
                (*currentStub)->setStopped(TIMEOUT);
            }
            else{
                #ifndef NDEBUG
                if(verbosityLevel >= 2)
                   std::cerr << __PRETTY_FUNCTION__ << " Current simulation time: " << curSimTime << " first event " << event.first  << " Moving current simulation time" << std::endl;
                #endif
                //I have to move the simulation time to the
                //time of that event and then resume execution
                if(curSimTime != event.first){
                    //Ok,  I'm moving in time,  so I can clear the list of already added events
                     std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
                    for(stubsIter = stubs.begin(), stubsEnd = stubs.end(); stubsIter != stubsEnd; stubsIter++){
                        dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->clearSeenEvents();
                    }
                }
                 curSimTime = event.first;
                 if(event.second == NULL){
                    #ifndef NDEBUG
                    if(verbosityLevel >= 2)
                       std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Found a step event" << std::endl;
                    #endif
                     #ifndef NDEBUG
                     if(!step){
                        THROW_EXCEPTION("The command is not a step, but the event is NULL");
                     }
                     #endif
                     (*currentStub)->setStopped(STEP);
                 }
                 else{
                      #ifndef NDEBUG
                      if(verbosityLevel >= 2)
                          std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Found a normal event" << std::endl;
                      #endif
                      //First of all I have to add the event to the list of already seen events: this way
                      //I will not examine it in the future
                      dynamic_cast<GDBStub<AddressType> *>(*currentStub)->addSeenEvent(event.second->address);
                     breakReached = event.second;
                     (*currentStub)->setStopped(BREAK);
                 }
             }

             if(wasRunning || simController.is_running()){
                 this->simController.run_simulation();
            }
         }
         #ifndef NDEBUG
         else if(verbosityLevel >= 2)
             std::cerr << __PRETTY_FUNCTION__ << " Not Resuming execution: waiting for other " << numStopped << " Processors" << std::endl;
         #endif
   }
   #else
   ///Method used to resume execution after GDB has issued
   ///the continue or step signal
   void resumeExecution(){
        boost::mutex::scoped_lock lock(cont_mutex);
         #ifndef NDEBUG
         if(verbosityLevel >= 2)
             std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Trying to Resume Exceution numStopped: " << numStopped << std::endl;
          #endif
         numStopped--;
         //I'm going to restart execution, so I can again enable watch and break points
         if(timeToJump > 0)
            this->breakEnabled = false;
        else
            this->breakEnabled = true;
         if(numStopped == 0){
             //I can finally resume execution
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                 std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Resuming Exceution" << std::endl;
             #endif
             simStartTime = this->simController.get_simulated_time();
             if(timeToJump > 0){
                 this->simController.run_simulation(timeToJump);
             }
             else if(timeToGo > 0){
                 this->simController.run_simulation(timeToGo);
             }
             else{
                 this->simController.run_simulation();
             }
         }
         #ifndef NDEBUG
         else if(verbosityLevel >= 2)
             std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Not Resuming execution: waiting for other " << numStopped << " Processors" << std::endl;
         #endif
   }
   #endif

   /** Here start all the methods to handle the different GDB requests **/

   ///It does nothing, it simply sends an empty string back to the
   ///GDB debugger
   bool emptyAction(GDBRequest &req){
      #ifndef NDEBUG
      if(verbosityLevel >= 2)
        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Request: " << req.type << std::endl;
      #endif

      GDBResponse resp;
      resp.type = GDBResponse::NOT_SUPPORTED;

      this->connManager.sendResponse(resp);

      return true;
   }

   ///Asks for the reason why the processor is stopped
   bool reqStopReason(){
      this->awakeGDB();
      return true;
   }

   ///Reads the value of a register;
   bool readRegister(GDBRequest &req){
      GDBResponse rsp;
      rsp.type = GDBResponse::REG_READ;
      try{
          if(req.reg < this->proc.nRegs() && !sc_controller::error){
             #ifdef ENABLE_MYSQL
             mySQLinstance.flushEvents();
             AddressType regContent = this->proc.reg_read(req.reg, &mySQLinstance, curSimTime);
             #else
             AddressType regContent = this->proc.reg_read(req.reg);
             #endif
             this->valueToBytes(rsp.data, regContent);
          }
          else{
             this->valueToBytes(rsp.data, 0);
          }
      }
      catch(...){
         this->valueToBytes(rsp.data, 0);
     }
     
      if(sc_controller::error)
         rsp.type = GDBResponse::ERROR;
     
      this->connManager.sendResponse(rsp);

      if(!sc_controller::error)
         return true;
      else{
         rsp.type = GDBResponse::OUTPUT;
         rsp.message = sc_controller::errorMessage;
         this->connManager.sendResponse(rsp);
         return false;
     }
   }

   ///Reads the value of a memory location
   bool readMemory(GDBRequest &req){
      GDBResponse rsp;
      rsp.type = GDBResponse::MEM_READ;

      for(unsigned int i = 0; i < req.length; i++){
         try{
             #ifdef ENABLE_MYSQL
             mySQLinstance.flushEvents();
             unsigned char memContent = this->proc.mem_read(req.address + i, &mySQLinstance,  curSimTime);
             #else
             unsigned char memContent = this->proc.mem_read(req.address + i);
             #endif
             this->valueToBytes(rsp.data, memContent);
         }
         catch(...){
            this->valueToBytes(rsp.data, 0);
        }
         if(sc_controller::error)
            break;
      }

      if(sc_controller::error)
         rsp.type = GDBResponse::ERROR;

      this->connManager.sendResponse(rsp);

      if(!sc_controller::error)
         return true;
      else{
        rsp.type = GDBResponse::OUTPUT;
         rsp.message = sc_controller::errorMessage;
         this->connManager.sendResponse(rsp);
         return false;
     }
   }

   bool cont(GDBRequest &req){
      if(req.address != 0){
         #ifdef ENABLE_MYSQL
         mySQLinstance.flushEvents();
         this->proc.set_ac_pc(req.address, &mySQLinstance,  curSimTime);
         #else
         this->proc.set_ac_pc(req.address);
         #endif
      }

      //Now, I have to restart SystemC, since the processor
      //has to go on; note that actually SystemC restarts only
      //after all the gdbs has issued some kind of start command
      //(either a continue, a step ...)
      #ifdef ENABLE_MYSQL
      this->resumeExecution(false);
      #else
      this->resumeExecution();
      #endif

      return false;
   }

   bool detach(GDBRequest &req){
        //First of all I have to perform some cleanup
        this->breakManager.clearAllBreaks();
        this->isGDBConnected = false;
        //Finally I can send a positive response
        GDBResponse resp;
        resp.type = GDBResponse::OK;
        this->connManager.sendResponse(resp);
        this->isKilled = true;
        //Now,  if execution were stopped,  I have to resume it
        if(numStopped > 0){
            #ifdef ENABLE_MYSQL
            this->resumeExecution(false);
            #else
            this->resumeExecution();
            #endif
        }
        return false;
   }

   bool readRegisters(){
      //I have to read all the general purpose registers and
      //send their content back to GDB
      GDBResponse resp;
      resp.type = GDBResponse::REG_READ;
      for(unsigned int i = 0; i < this->proc.nRegs(); i++){
         try{
             #ifdef ENABLE_MYSQL
             mySQLinstance.flushEvents();
             AddressType regContent = this->proc.reg_read(i, &mySQLinstance,  curSimTime);
             #else
             AddressType regContent = this->proc.reg_read(i);
             #endif
             this->valueToBytes(resp.data, regContent);
        }
        catch(...){
           this->valueToBytes(resp.data, 0);
        }
      }

      if(sc_controller::error)
         resp.type = GDBResponse::ERROR;

      this->connManager.sendResponse(resp);

      if(!sc_controller::error)
         return true;
      else{
        resp.type = GDBResponse::OUTPUT;
         resp.message = sc_controller::errorMessage;
         this->connManager.sendResponse(resp);
         return false;
     }
   }

   bool writeRegisters(GDBRequest &req){
      std::vector<AddressType> regContent;
      this->bytesToValue(req.data, regContent);
      typename std::vector<AddressType>::iterator dataIter, dataEnd;
      bool error = false;
      unsigned int i = 0;
      for(dataIter = regContent.begin(), dataEnd = regContent.end();
                                    dataIter != dataEnd; dataIter++){
         try{
             #ifdef ENABLE_MYSQL
             mySQLinstance.flushEvents();
             this->proc.reg_write(i, *dataIter, &mySQLinstance,  curSimTime);
             #else
             this->proc.reg_write(i, *dataIter);
             #endif
         }
         catch(...){
            error = true;
         }
         i++;
      }

      GDBResponse resp;

      if(i != (unsigned int)this->proc.nRegs() || sc_controller::error || error){
         #ifndef NDEBUG
         std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Error, written: " << i << " registers out of range " << this->proc.nRegs() << std::endl;
         #endif
         resp.type = GDBResponse::ERROR;
      }
      else
         resp.type = GDBResponse::OK;
      this->connManager.sendResponse(resp);

      return true;
   }

   bool writeMemory(GDBRequest &req){
      bool error = false;
      unsigned int bytes = 0;
      std::vector<char>::iterator dataIter, dataEnd;
      for(dataIter = req.data.begin(), dataEnd = req.data.end(); dataIter != dataEnd; dataIter++){
        try{
             #ifdef ENABLE_MYSQL
             mySQLinstance.flushEvents();
             this->proc.mem_write(req.address + bytes, *dataIter, &mySQLinstance,  curSimTime);
             #else
             this->proc.mem_write(req.address + bytes, *dataIter);
             #endif
             bytes++;
         }
         catch(...){
            error = true;
            break;
         }
         if(sc_controller::error)
            break;
      }

      GDBResponse resp;
      resp.type = GDBResponse::OK;

      #ifndef NDEBUG
      if(bytes != (unsigned int)req.length){
         std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Error, written: " << bytes << " bytes out of " << req.length << std::endl;
         resp.type = GDBResponse::ERROR;
      }
      #endif
      if(sc_controller::error || error)
         resp.type = GDBResponse::ERROR;

      this->connManager.sendResponse(resp);
      if(sc_controller::error){
        resp.type = GDBResponse::OUTPUT;
         resp.message = sc_controller::errorMessage;
         this->connManager.sendResponse(resp);
         return false;
     }


      return true;
   }

   bool writeRegister(GDBRequest &req){
      GDBResponse rsp;
      if(req.reg <= this->proc.nRegs()){
         try{
             #ifdef ENABLE_MYSQL
             mySQLinstance.flushEvents();
             this->proc.reg_write(req.reg, req.value, &mySQLinstance, curSimTime);
             #else
             this->proc.reg_write(req.reg, req.value);
             #endif
             rsp.type = GDBResponse::OK;
         }
         catch(...){
            rsp.type = GDBResponse::ERROR;
         }
      }
      else{
         rsp.type = GDBResponse::ERROR;
      }
      if(sc_controller::error)
         rsp.type = GDBResponse::ERROR;
      this->connManager.sendResponse(rsp);

      return true;
   }

    bool killApp(){
        #ifndef NDEBUG
        if(verbosityLevel >= 2)
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Simulation stopped because of a kill request from GDB" << std::endl;
        #endif
        this->isKilled = true;
        if(this->simController.is_paused())
            this->simController.run_simulation();
        this->simController.stop_simulation();
        //Lets notify the other processors that the app has been killed
        std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
        for(stubsIter = stubs.begin(), stubsEnd = stubs.end();
                                stubsIter != stubsEnd; stubsIter++){
            if(*stubsIter != this){
                GDBResponse response;
                response.type = GDBResponse::OUTPUT;
                response.message = "CPU " + this->proc.getName() + " killed the simulation\n";
                dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->connManager.sendResponse(response);
                dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->signalProgramEnd(true);
            }
        }
        return false;
    }

   bool doStep(GDBRequest &req){
      #ifndef NDEBUG
      if(verbosityLevel >= 2)
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << std::endl;
      #endif
      if(req.address != 0){
         #ifdef ENABLE_MYSQL
         mySQLinstance.flushEvents();
         this->proc.set_ac_pc(req.address, &mySQLinstance,  curSimTime);
         #else
         this->proc.set_ac_pc(req.address);
         #endif
      }

      this->step = 1;
      #ifdef ENABLE_MYSQL
      this->resumeExecution(true);
      #else
      this->resumeExecution();
      #endif

      return false;
   }

   bool addBreakpoint(GDBRequest &req){
      GDBResponse resp;
      switch(req.value){
         /*case 0:
            if(this->breakManager.addBreakpoint(Breakpoint<AddressType>::MEM, req.address, req.length))
               resp.type = GDBResponse::OK;
            else
              resp.type = GDBResponse::ERROR;
         break;*/
         case 0:
         case 1:
            if(this->breakManager.addBreakpoint(Breakpoint<AddressType>::HW, req.address, req.length))
               resp.type = GDBResponse::OK;
            else
              resp.type = GDBResponse::ERROR;
         break;
         case 2:
            if(this->breakManager.addBreakpoint(Breakpoint<AddressType>::WRITE, req.address, req.length))
               resp.type = GDBResponse::OK;
            else
              resp.type = GDBResponse::ERROR;
         break;
         case 3:
            if(this->breakManager.addBreakpoint(Breakpoint<AddressType>::READ, req.address, req.length))
               resp.type = GDBResponse::OK;
            else
              resp.type = GDBResponse::ERROR;
         break;
         case 4:
            if(this->breakManager.addBreakpoint(Breakpoint<AddressType>::ACCESS, req.address, req.length))
               resp.type = GDBResponse::OK;
            else
              resp.type = GDBResponse::ERROR;
         break;
         default:
            resp.type = GDBResponse::NOT_SUPPORTED;
         break;
      }
      this->connManager.sendResponse(resp);
      return true;
   }

   bool removeBreakpoint(GDBRequest &req){
      GDBResponse resp;
      if(this->breakManager.removeBreakpoint(req.address))
         resp.type = GDBResponse::OK;
      else
         resp.type = GDBResponse::ERROR;
      this->connManager.sendResponse(resp);
      return true;
   }

   bool genericQuery(GDBRequest &req){
        //I have to determine the query packet; in case it is Rcmd I deal with it
        GDBResponse resp;
         #ifndef NDEBUG
         if(verbosityLevel >= 1)
            std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " custom query " << req.command << std::endl;
         #endif
        if(req.command != "Rcmd")
            resp.type = GDBResponse::NOT_SUPPORTED;
        else{
             //lets see which is the custom command being sent
             std::string::size_type spacePos = req.extension.find(' ');
             std::string custComm;
             if(spacePos == std::string::npos)
                custComm = req.extension;
            else{
                 custComm = req.extension.substr(0,  spacePos);
            }
             #ifndef NDEBUG
             if(verbosityLevel >= 1)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " custom command " << custComm << "- Extension " << req.extension << std::endl;
             #endif
             if(custComm == "go"){
                 //Ok,  finally I got the right command: lets see for
                 //how many nanoseconds I have to execute the continue
                timeToGo = atof(req.extension.substr(spacePos + 1).c_str());
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " TimeToGo " << timeToGo << std::endl;
                 #endif
                 if(timeToGo < 0){
                     #ifndef NDEBUG
                     if(verbosityLevel >= 2)
                        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " TimeToGo smaller than 0" << std::endl;
                     #endif
                     resp.type = GDBResponse::OUTPUT;
                     resp.message = "Please specify a positive offset; if then you desire to debug backwards in time, use the \"monitor backward\" command";
                     this->connManager.sendResponse(resp);
                     resp.type = GDBResponse::NOT_SUPPORTED;
                     timeToGo = 0;
                 }
                 else
                    resp.type = GDBResponse::OK;
            }
            else if(custComm == "go_abs"){
                 //This command specify to go up to a specified simulation time; the time is specified in nanoseconds
                 timeToGo = atof(req.extension.substr(spacePos + 1).c_str()) - this->simController.get_simulated_time();
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " TimeToGo " << timeToGo << std::endl;
                 #endif
                 if(timeToGo < 0){
                     #ifndef ENABLE_MYSQL
                     resp.type = GDBResponse::OUTPUT;
                     resp.message = "The database is not enabled, so debugging backwards is not allowed\n";
                     this->connManager.sendResponse(resp);
                     resp.type = GDBResponse::NOT_SUPPORTED;
                     timeToGo = 0;
                     #else
                     direction = BACKWARD;
                     timeToGo = -timeToGo;
                     resp.type = GDBResponse::OK;
                     #endif
                 }
                 else{
                    direction = FORWARD;
                    resp.type = GDBResponse::OK;
                }
             }
             else if(custComm == "jump"){
                 //Ok,  finally I got the right command: lets see for
                 //how many nanoseconds I have to execute the continue
                timeToJump = atof(req.extension.substr(spacePos + 1).c_str());
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " TimeToJump " << timeToJump << std::endl;
                 #endif
                 if(timeToJump < 0){
                     resp.type = GDBResponse::OUTPUT;
                     resp.message = "Please specify a positive offset; if then you desire to debug backwards in time, use the \"monitor backward\" command\n";
                     this->connManager.sendResponse(resp);
                     resp.type = GDBResponse::NOT_SUPPORTED;
                     timeToJump = 0;
                 }
                 else{
                    resp.type = GDBResponse::OK;
                    timeToGo = 0;
                }
            }
            else if(custComm == "jump_abs"){
                 //This command specify to go up to a specified simulation time; the time is specified in nanoseconds
                 timeToJump = atof(req.extension.substr(spacePos + 1).c_str()) - this->simController.get_simulated_time();
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " TimeToJump " << timeToJump << std::endl;
                 #endif
                 if(timeToJump < 0){
                     #ifndef ENABLE_MYSQL
                     resp.type = GDBResponse::OUTPUT;
                     resp.message = "The database is not enabled, so debugging backwards is not allowed\n";
                     this->connManager.sendResponse(resp);
                     resp.type = GDBResponse::NOT_SUPPORTED;
                     timeToJump = 0;
                     #else
                     direction = BACKWARD;
                     timeToJump = -timeToJump;
                     resp.type = GDBResponse::OK;
                     #endif
                 }
                 else{
                    direction = FORWARD;
                     timeToGo = 0;
                     resp.type = GDBResponse::OK;
                 }
            }
            else if(custComm == "backward"){
                 //This command specify that all the comands must be executed backwards in time (i.e. using the history)
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Direction backward" << std::endl;
                 #endif
                 #ifdef ENABLE_MYSQL
                 direction = BACKWARD;
                 resp.type = GDBResponse::OK;
                 #else
                 resp.type = GDBResponse::OUTPUT;
                 resp.message = "The database is not enabled, so debugging backwards is not allowed\n";
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::NOT_SUPPORTED;
                 #endif
            }
            else if(custComm == "forward"){
                //This command specify that all the comands must be executed forward in time (i.e. the normal debugging strategy)
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Direction forward" << std::endl;
                 #endif                
                 direction = FORWARD;
                 resp.type = GDBResponse::OK;
            }
            else if(custComm == "status"){
                 //Returns the current status of the STUB
                 resp.type = GDBResponse::OUTPUT;
                 resp.message = "Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
                 resp.message += "Direction: ";
                 if(direction == FORWARD)
                    resp.message += "Forward\n";
                 else
                    resp.message += "Backward\n";
                 if(timeToGo != 0)
                    resp.message += "Simulating for : " + boost::lexical_cast<std::string>(timeToGo) + " Nanoseconds\n";
                 if(timeToJump != 0)
                    resp.message += "Jumping for : " + boost::lexical_cast<std::string>(timeToJump) + " Nanoseconds\n";
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << " Current status " << resp.message << std::endl;
                 #endif
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::OK;
            }
            else if(custComm == "time"){
                //This command is simply a query to know the current simulation time
                resp.type = GDBResponse::OUTPUT;
                 resp.message = "Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::OK;
            }
            else if(custComm == "awake"){
                //This command is simply a query to know the current simulation time
                std::vector<GDBStubBase *>::iterator stubsIter, stubsEnd;
                for(stubsIter = stubs.begin(), stubsEnd = stubs.end();
                                        stubsIter != stubsEnd; stubsIter++){
                    if(*stubsIter != this){
                        GDBResponse response;
                        response.type = GDBResponse::OUTPUT;
                        response.message = "Received an awake command from CPU " + this->proc.getName() + "\n";
                        dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->connManager.sendResponse(response);
                        dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->awakeGDB();
                        numStopped++;
                        dynamic_cast<GDBStub<AddressType> *>(*stubsIter)->startThread();
                    }
                }
                resp.type = GDBResponse::OK;
            }
            else if(custComm == "help"){
                //This command is simply a query to know the current simulation time
                resp.type = GDBResponse::OUTPUT;
                 resp.message = "Help about the custom GDB commands available for the ReSP simulation platform:\n";
                 resp.message += "   monitor help:       prints the current message\n";
                 resp.message += "   monitor time:       returns the current simulation time\n";
                 resp.message += "   monitor status:     returns the status of the simulation\n";
                 resp.message += "   monitor forward:    sets the debugging direction forward in time\n";
                 resp.message += "   monitor backward:   sets the debugging direction backwards in time\n";
                 resp.message += "   monitor jump n:     moves the simulation time of an offset of n (ns) from the current time\n";
                 resp.message += "   monitor jump_abs n: moves the simulation time to instant n (ns)\n";
                 resp.message += "   monitor go n:       simulates for n (ns) starting from the current time\n";
                 resp.message += "   monitor go_abs n:   simulates up to instant n (ns)\n";
                 resp.message += "   monitor awake:      awakes all the other GDB instances in order to allow debugging of the other processors\n";
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::OK;
            }
            else{
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Command " << custComm << " not supported" << std::endl;
                 #endif
                resp.type = GDBResponse::NOT_SUPPORTED;
            }
        }
        this->connManager.sendResponse(resp);
        return true;
   }

   ///Separates the bytes which form an integer value and puts them
   ///into an array of bytes
   template <class ValueType> void valueToBytes(std::vector<char> &byteHolder, ValueType value){
         #ifndef NDEBUG
         if(verbosityLevel >= 3)
            std::cerr << __PRETTY_FUNCTION__ << " Got: " << std::hex << value << std::dec << std::endl;
         #endif
        if(!endianess){
             #ifndef NDEBUG
             if(verbosityLevel >= 3)
                std::cerr << __PRETTY_FUNCTION__ << " Converting: ";
             #endif
            for(unsigned int i = 0; i < sizeof(ValueType); i++){
                byteHolder.push_back((char)((value & (0x0FF << 8*i)) >> 8*i));
                 #ifndef NDEBUG
                 if(verbosityLevel >= 3)
                    std::cerr << std::hex << byteHolder.back() << std::dec << std::endl;
                 #endif
            }
             #ifndef NDEBUG
             if(verbosityLevel >= 3)
                std::cerr << std::endl;
             #endif
        }
        else{
             #ifndef NDEBUG
             if(verbosityLevel >= 3)
                std::cerr << __PRETTY_FUNCTION__ << " Converting: ";
             #endif
            for(int i = sizeof(ValueType) - 1; i >= 0; i--){
                byteHolder.push_back((char)((value & (0x0FF << 8*i)) >> 8*i));
                 #ifndef NDEBUG
                 if(verbosityLevel >= 3)
                    std::cerr << std::hex << byteHolder.back() << std::dec << std::endl;
                 #endif
            }
             #ifndef NDEBUG
             if(verbosityLevel >= 3)
                std::cerr << std::endl;
             #endif
        }
   }

   ///Converts a vector of bytes into a vector of integer values
   void bytesToValue(std::vector<char> &byteHolder, std::vector<AddressType> &values){
      for(unsigned int i = 0; i < byteHolder.size(); i += sizeof(AddressType)){
         AddressType buf = 0;
         for(unsigned int k = 0; k < sizeof(AddressType); k++){
            buf |= (byteHolder[i + k] << 8*k);
         }
         values.push_back(buf);
      }
   }

   
   #ifdef ENABLE_MYSQL
   ///It determines the nearest event (breakpoin or watch, or the next assembly instruction
   ///in case of a step command); note that if the direction is backward, then the next event is
   ///in the back. The first return parameter is true if there is an event (either a break,  a watch
   ///or a step),  while the second is a pointer to the found event (in case it is a breakpoint
   ///or a watch; NULL in case of a step command)
   std::pair<double, Breakpoint<AddressType> *> getEvent(bool step){
        //I have to examine all breakpoints and look for the event;
        //I then get the nearest to the current time; in case of a step
        //I simply have to query the next instruction and get the
        //events in this time frame
        std::vector<std::pair<double,  Breakpoint<AddressType> *> > happenedEv;
        if(step){
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Looking for step event" << std::endl;
            #endif
            double endTime = -1;
            mySQLinstance.flushEvents();
            endTime = this->proc.getNextInstruction(direction == FORWARD, curSimTime, &mySQLinstance);
            if(endTime == -1){
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " No next instruction found" << std::endl;
                #endif
                //Ok,  there is not next instruction
                std::pair<double, Breakpoint<AddressType> *> tempPair;
                tempPair.first = -1;
                tempPair.second = NULL;
                return tempPair;
            }
            //Now I have to go over all the breakpoints and check if at least one has happened
            std::map<AddressType, Breakpoint<AddressType> > & breaks = this->breakManager.getBreakpoints();
            typename std::map<AddressType, Breakpoint<AddressType> >::iterator breakInter,  breakEnd;
            for(breakInter = breaks.begin(),  breakEnd = breaks.end(); breakInter != breakEnd; breakInter++){
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Looking for breakpoint at address " << std::hex << breakInter->second.address << std::dec << std::endl;
                #endif
                mySQLinstance.flushEvents();
                double foundTime = this->proc.findEvent(breakInter->second, curSimTime,  endTime, &mySQLinstance);
                if(foundTime >= 0){
                     #ifndef NDEBUG
                     if(verbosityLevel >= 2)
                        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Found break at time " << foundTime << std::endl;
                    #endif
                    std::pair<double,  Breakpoint<AddressType> *> foundEv;
                    foundEv.first = foundTime;
                    foundEv.second = &(breakInter->second);
                    happenedEv.push_back(foundEv);
                }
            }
            if(happenedEv.size() == 0){
                //Ok,  the next instruction is too far: there are no breakpoints in between
                std::pair<double, Breakpoint<AddressType> *> tempPair;
                tempPair.first = endTime;
                tempPair.second = NULL;
                return tempPair;
            }
        }
        else{
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Looking for non-step event" << std::endl;
            #endif
            //Ok,  not step: I have to find all the events in both directions;
            std::map<AddressType, Breakpoint<AddressType> > & breaks = this->breakManager.getBreakpoints();
            typename std::map<AddressType, Breakpoint<AddressType> >::iterator breakInter,  breakEnd;
            double endTime = -1;
            if(direction == FORWARD)
                endTime = this->simController.get_simulated_time();
            else
                endTime = 0;
            for(breakInter = breaks.begin(),  breakEnd = breaks.end(); breakInter != breakEnd; breakInter++){
                 #ifndef NDEBUG
                 if(verbosityLevel >= 2)
                    std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Looking for breakpoint at address " << breakInter->second.address << std::endl;
                #endif
                mySQLinstance.flushEvents();
                double foundTime = this->proc.findEvent(breakInter->second, curSimTime, endTime, &mySQLinstance);
                if(foundTime >= 0){
                     #ifndef NDEBUG
                     if(verbosityLevel >= 2)
                        std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Found break at time " << foundTime << std::endl;
                    #endif
                    std::pair<double,  Breakpoint<AddressType> *> foundEv;
                    foundEv.first = foundTime;
                    foundEv.second = &(breakInter->second);
                    happenedEv.push_back(foundEv);
                }
            }
        }

        //Ok: now I have all the events; I have to go sort them according to the timestamp
        //and return the one with the first one (note that depending on the direction of the
        //debugging I might need to sort the events in ascending or descending order)
        if(happenedEv.size() > 0){
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Sorting the " << happenedEv.size() << " events" << std::endl;
            #endif
            if(direction == FORWARD)
                std::sort(happenedEv.begin(), happenedEv.end(), sortEventsAsc<AddressType>);
            else
                std::sort(happenedEv.begin(), happenedEv.end(), sortEventsDesc<AddressType>);
                
             #ifndef NDEBUG
             if(verbosityLevel >= 2)
                std::cerr << __PRETTY_FUNCTION__ << "Processor Name: " << this->proc.getName() << " Sorted" << std::endl;
            #endif
            return happenedEv.front();
        }
        else{
            std::pair<double, Breakpoint<AddressType> *> tempPair;
            tempPair.first = -1;
            tempPair.second = NULL;
            return tempPair;
        }
   }

    bool isSeen(unsigned int address){
        typename std::vector<AddressType>::iterator seenIter,  seenEnd;
        for(seenIter = this->seenBreaks.begin(),  seenEnd = this->seenBreaks.end(); seenIter != seenEnd; seenIter++){
            if(*seenIter == address)
                return true;
        }
        return false;
    }
    void clearSeenEvents(){
        this->seenBreaks.clear();
    }
    void addSeenEvent(unsigned int address){
        this->seenBreaks.push_back(address);
    }
   #endif

};


}

using namespace resp;

#endif
