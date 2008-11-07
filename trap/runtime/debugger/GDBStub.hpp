/***************************************************************************\
 *
 *
 *            ___        ___           ___           ___
 *           /  /\      /  /\         /  /\         /  /\
 *          /  /:/     /  /::\       /  /::\       /  /::\
 *         /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
 *        /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
 *       /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
 *      /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
 *      \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
 *           \  \:\   \  \:\        \  \:\        \  \:\
 *            \  \ \   \  \:\        \  \:\        \  \:\
 *             \__\/    \__\/         \__\/         \__\/
 *
 *
 *
 *
 *   This file is part of TRAP.
 *
 *   TRAP is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Lesser General Public License for more details.
 *
 *   You should have received a copy of the GNU Lesser General Public License
 *   along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *   or see <http://www.gnu.org/licenses/>.
 *
 *
 *
 *   (c) Luca Fossati, fossati@elet.polimi.it
 *
\***************************************************************************/

/**
 * This file contains the methods necessary to communicate with GDB in
 * order to debug software running on simulators. Source code takes inspiration
 * from the linux kernel (sparc-stub.c) and from ac_gdb.H in the ArchC sources
 */

#ifndef GDBSTUB_HPP
#define GDBSTUB_HPP

#include <systemc.h>

#include <vector>
#include <boost/thread/thread.hpp>
#include <boost/thread/xtime.hpp>
#include <boost/thread/condition.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/lexical_cast.hpp>

#include "utils.hpp"

#include "ABIIf.hpp"
#include "ToolsIf.hpp"

#include "BreakpointManager.hpp"
#include "GDBConnectionManager.hpp"

template<class issueWidth> class GDBStub : public ToolsIf<issueWidth>, public sc_module{
  private:
    enum stopType {BREAK=0, STEP, SEG, TIMEOUT, PAUSED, UNK};
    ///Thread used to send and receive responses with the GDB debugger
    struct GDBThread{
        GDBStub<issueWidth> &stub;
        GDBThread(GDBStub<issueWidth> &stub) : stub(stub){}
        ///Main body of the thread: it simply waits for GDB requests
        ///and takes the appropriate actions once the requests are decoded
        void operator()(){
            while(stub.isConnected)
                stub.waitForRequest();
        }
    };

    ///Manages connection among the GDB target stub (this class) and
    ///the GDB debugger
    GDBConnectionManager connManager;
    ///Interface for communication with the internal processor's structure
    ABIIf<issueWidth> &processorInstance;
    ///Handles the breakpoints which have been set in the system
    BreakpointManager<issueWidth> breakManager;
    ///Determines whether the processor has to halt as a consequence of a
    ///step command
    unsigned int step;
    ///Keeps track of the last breakpoint encountered by this processor
    Breakpoint<issueWidth> * breakReached;
    ///Specifies whether the watchpoints and breakpoints are enabled or not
    bool breakEnabled;
    ///Specifies whether GDB server side killed the simulation
    bool isKilled;
    ///In case we decided to run the simulation only for a limited ammount of time
    ///this variable contains that time
    double timeToGo;
    ///In case we decided to jump onwards or backwards for a specified ammount of time,
    ///this variable contains that time
    double timeToJump;
    ///In case the simulation is run only for a specified ammount of time,  this variable
    ///contains the simulation time at that start time
    double simStartTime;
    ///Specifies that we have to stop because a timeout was encountered
    bool timeout;
    ///Event used to manage execution for a specified ammount of time
    sc_event pauseEvent;
    ///Condition used to stop processor execution until simulation is restarted
    boost::condition gdbPausedEvent;
    ///Mutex used to access the condition
    boost::mutex global_mutex;
    ///Sepecifies if GDB is connected to this stub or not
    bool isConnected;
    ///Specifies that the first run is being made
    bool firstRun;

    /********************************************************************/
    ///Checks if a breakpoint is present at the current address and
    ///in case it halts execution
    #ifndef NDEBUG
    inline void checkBreakpoint(const issueWidth &address){
    #else
    inline void checkBreakpoint(const issueWidth &address) throw(){
    #endif
        if(this->breakEnabled && this->breakManager.hasBreakpoint(address)){
            this->breakReached = this->breakManager.getBreakPoint(address);
            if(breakReached == NULL){
                THROW_EXCEPTION("I stopped because of a breakpoint, but no breakpoint was found");
            }
            this->setStopped(BREAK);
        }
    }
    ///Checks if execution must be stopped because of a step command
    inline void checkStep() throw(){
        if(this->step == 1)
            this->step++;
        else if(this->step == 2){
            this->step = 0;
            if(this->timeout){
                this->timeout = false;
                this->setStopped(TIMEOUT);
            }
            else
                this->setStopped(STEP);
        }
    }

    ///Starts the thread which will manage the connection with the
    ///GDB debugger
    void startThread(){
        GDBThread thread(*this);
        boost::thread th(thread);
    }

    ///This method is called when we need asynchronously halt the
    ///execution of the processor this instance of the stub is
    ///connected to; it is usually used when a processor is halted
    ///and it has to communicated to the other processor that they have
    ///to halt too; note that this method halts SystemC execution and
    ///it also starts new threads (one for each processor) which will
    ///deal with communication with the stub; when a continue or
    ///step signal is met, then the receving thread is killed. When
    ///all the threads are killed execution can be resumed (this means
    ///that all GDBs pressed the resume button)
    ///This method is also called at the beginning of the simulation by
    ///the first processor which starts execution
    void setStopped(stopType stopReason = UNK){
        //saving current simulation time
        double curSimTime = sc_time_stamp().to_double();

        //Now I have to behave differently depending on whether database support is enabled or not
        //if it is enabled I do not stop simulation,  while if it is not enabled I have to stop simulation in
        //order to be able to inspect the content of the processor - memory - etc...
        //Computing the next simulation time instant
        if(this->timeToGo > 0){
            this->timeToGo -= (curSimTime - this->simStartTime);
            if(this->timeToGo < 0)
                this->timeToGo = 0;
            this->simStartTime = curSimTime;
        }
        //Disabling break and watch points
        this->breakEnabled = false;
        this->awakeGDB(stopReason);
        //pausing simulation
        if(stopReason != TIMEOUT && stopReason !=  PAUSED){
            boost::mutex::scoped_lock lk(this->global_mutex);
            this->gdbPausedEvent.wait(lk);
        }
    }

    ///Sends a TRAP message to GDB so that it is awaken
    void awakeGDB(stopType stopReason = UNK){
        switch(stopReason){
            case STEP:{
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

                if(this->breakReached->type == Breakpoint<issueWidth>::HW ||
                            this->breakReached->type == Breakpoint<issueWidth>::MEM){
                    GDBResponse response;
                    response.type = GDBResponse::S;
                    response.payload = SIGTRAP;
                    this->connManager.sendResponse(response);
                }
                else{
                    GDBResponse response;
                    response.type = GDBResponse::T;
                    response.payload = SIGTRAP;
                    std::pair<std::string, unsigned int> info;
                    info.second = this->breakReached->address;
                    switch(this->breakReached->type){
                        case Breakpoint<issueWidth>::WRITE:
                            info.first = "watch";
                        break;
                        case Breakpoint<issueWidth>::READ:
                            info.first = "rwatch";
                        break;
                        case Breakpoint<issueWidth>::ACCESS:
                            info.first = "awatch";
                        break;
                        default:
                            info.first = "none";
                        break;
                    }
                    response.size = sizeof(issueWidth);
                    response.info.push_back(info);
                    this->connManager.sendResponse(response);
                }
            break;}
            case SEG:{
                //An error has occurred during processor execution (illelgal instruction, reading out of memory, ...);
                GDBResponse response;
                response.type = GDBResponse::S;
                response.payload = SIGILL;
                this->connManager.sendResponse(response);
            break;}
            case TIMEOUT:{
                //the simulation time specified has elapsed,  so simulation halted
                GDBResponse resp;
                resp.type = GDBResponse::OUTPUT;
                resp.message = "Specified Simulation time completed - Current simulation time: " + sc_time_stamp().to_string() + " (ps)\n";
                this->connManager.sendResponse(resp);
                this->connManager.sendInterrupt();
            break;}
            case PAUSED:{
                //the simulation time specified has elapsed, so simulation halted
                GDBResponse resp;
                resp.type = GDBResponse::OUTPUT;
                resp.message = "Simulation Paused - Current simulation time: " + sc_time_stamp().to_string() + " (ps)\n";
                this->connManager.sendResponse(resp);
                this->connManager.sendInterrupt();
            break;}
            default:
                this->connManager.sendInterrupt();
            break;
        }
    }

    ///Signals to the GDB debugger that simulation ended; the error variable specifies
    ///if the program ended with an error
    void signalProgramEnd(bool error = false){
        if(!this->isKilled || error){
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
    }

    ///Waits for an incoming request by the GDB debugger and, once it
    ///has been received, it routes it to the appropriate handler
    ///Returns whether we must be listening for other incoming data or not
    void waitForRequest(){
        GDBRequest req = connManager.processRequest();
        switch(req.type){
            case GDBRequest::QUEST:
                //? request: it asks the target the reason why it halted
                this->reqStopReason();
            break;
            case GDBRequest::EXCL:
                // ! request: it asks if extended mode is supported
                this->emptyAction(req);
            break;
            case GDBRequest::c:
                //c request: Continue command
                this->cont(req);
            break;
            case GDBRequest::C:
                //C request: Continue with signal command, currently not supported
                this->emptyAction(req);
            break;
            case GDBRequest::D:
                //D request: disconnection from the remote target
                this->detach(req);
            break;
            case GDBRequest::g:
                //g request: read general register
                this->readRegisters();
            break;
            case GDBRequest::G:
                //G request: write general register
                this->writeRegisters(req);
            break;
            case GDBRequest::H:
                //H request: multithreading stuff, not currently supported
                this->emptyAction(req);
            break;
            case GDBRequest::i:
                //i request: single clock cycle step; currently it is not supported
                //since it requires advancing systemc by a specified ammont of
                //time equal to the clock cycle (or one of its multiple) and I still
                //have to think how to know the clock cycle of the processor and
                //how to awake again all the processors after simulation stopped again
                this->emptyAction(req);
            break;
            case GDBRequest::I:
                //i request: signal and single clock cycle step
                this->emptyAction(req);
            break;
            case GDBRequest::k:
                //i request: kill application: I simply call the sc_stop method
                this->killApp();
            break;
            case GDBRequest::m:
                //m request: read memory
                this->readMemory(req);
            break;
            case GDBRequest::M:
            case GDBRequest::X:
                //M request: write memory
                this->writeMemory(req);
            break;
            case GDBRequest::p:
                //p request: register read
                this->readRegister(req);
            break;
            case GDBRequest::P:
                //P request: register write
                this->writeRegister(req);
            break;
            case GDBRequest::q:
                //P request: register write
                this->genericQuery(req);
            break;
            case GDBRequest::s:
                //s request: single step
                this->doStep(req);
            break;
            case GDBRequest::S:
                //S request: single step with signal
                this->emptyAction(req);
            break;
            case GDBRequest::t:
                //t request: backward search: currently not supported
                this->emptyAction(req);
            break;
            case GDBRequest::T:
                //T request: thread stuff: currently not supported
                this->emptyAction(req);
            break;
            case GDBRequest::z:
                //z request: breakpoint/watch removal
                this->removeBreakpoint(req);
            break;
            case GDBRequest::Z:
                //z request: breakpoint/watch addition
                this->addBreakpoint(req);
            break;
            case GDBRequest::INTR:
                //received an iterrupt from GDB: I pause simulation and signal GDB that I stopped
                this->recvIntr();
            break;
            case GDBRequest::ERROR:
                std::cerr << "Error in the connection with the GDB debugger, connection will be terminated" << std::endl;
                this->isConnected = false;
                this->resumeExecution();
                this->breakEnabled = false;
            break;
            default:
                this->emptyAction(req);
            break;
        }
    }

    ///Method used to resume execution after GDB has issued
    ///the continue or step signal
    void resumeExecution(){
        //I'm going to restart execution, so I can again enable watch and break points
        this->breakEnabled = true;
        this->simStartTime = sc_time_stamp().to_double();
        this->gdbPausedEvent.notify_all();
        if(timeToGo > 0){
            this->pauseEvent.notify(sc_time(timeToGo, SC_PS));
        }
    }

    /** Here start all the methods to handle the different GDB requests **/

    ///It does nothing, it simply sends an empty string back to the
    ///GDB debugger
    void emptyAction(GDBRequest &req){
        GDBResponse resp;
        resp.type = GDBResponse::NOT_SUPPORTED;
        this->connManager.sendResponse(resp);
    }

    ///Asks for the reason why the processor is stopped
    void reqStopReason(){
        this->awakeGDB();
    }

    ///Reads the value of a register;
    void readRegister(GDBRequest &req){
        GDBResponse rsp;
        rsp.type = GDBResponse::REG_READ;
        try{
            if(req.reg < this->processorInstance.nGDBRegs()){
                issueWidth regContent = this->processorInstance.readGDBReg(req.reg);
                this->valueToBytes(rsp.data, regContent);
            }
            else{
                this->valueToBytes(rsp.data, 0);
            }
        }
        catch(...){
            this->valueToBytes(rsp.data, 0);
        }

        this->connManager.sendResponse(rsp);
    }

    ///Reads the value of a memory location
    void readMemory(GDBRequest &req){
        GDBResponse rsp;
        rsp.type = GDBResponse::MEM_READ;

        for(unsigned int i = 0; i < req.length; i++){
            try{
                unsigned char memContent = this->processorInstance.readMem(req.address + i);
                this->valueToBytes(rsp.data, memContent);
            }
            catch(...){
                this->valueToBytes(rsp.data, 0);
            }
        }

        this->connManager.sendResponse(rsp);
    }

    void cont(GDBRequest &req){
        if(req.address != 0){
            this->processorInstance.setPC(req.address);
        }

        //Now, I have to restart SystemC, since the processor
        //has to go on; note that actually SystemC restarts only
        //after all the gdbs has issued some kind of start command
        //(either a continue, a step ...)
        this->resumeExecution();
    }

    void detach(GDBRequest &req){
        //First of all I have to perform some cleanup
        this->breakManager.clearAllBreaks();
        //Finally I can send a positive response
        GDBResponse resp;
        resp.type = GDBResponse::OK;
        this->connManager.sendResponse(resp);
        this->step = 0;
        this->isConnected = false;
        this->resumeExecution();
        this->breakEnabled = false;
    }

    void readRegisters(){
        //I have to read all the general purpose registers and
        //send their content back to GDB
        GDBResponse resp;
        resp.type = GDBResponse::REG_READ;
        for(unsigned int i = 0; i < this->processorInstance.nGDBRegs(); i++){
            try{
                issueWidth regContent = this->processorInstance.readGDBReg(i);
                this->valueToBytes(resp.data, regContent);
            }
            catch(...){
                this->valueToBytes(resp.data, 0);
            }
        }
        this->connManager.sendResponse(resp);
    }

    void writeRegisters(GDBRequest &req){
        std::vector<issueWidth> regContent;
        this->bytesToValue(req.data, regContent);
        typename std::vector<issueWidth>::iterator dataIter, dataEnd;
        bool error = false;
        unsigned int i = 0;
        for(dataIter = regContent.begin(), dataEnd = regContent.end();
                                        dataIter != dataEnd; dataIter++){
            try{
                this->processorInstance.setGDBReg(*dataIter, i);
            }
            catch(...){
                error = true;
            }
            i++;
        }

        GDBResponse resp;

        if(i != (unsigned int)this->processorInstance.nGDBRegs() || error)
            resp.type = GDBResponse::ERROR;
        else
            resp.type = GDBResponse::OK;
        this->connManager.sendResponse(resp);
    }

    void writeMemory(GDBRequest &req){
        bool error = false;
        unsigned int bytes = 0;
        std::vector<char>::iterator dataIter, dataEnd;
        for(dataIter = req.data.begin(), dataEnd = req.data.end(); dataIter != dataEnd; dataIter++){
            try{
                this->processorInstance.writeMem(req.address + bytes, *dataIter);
                bytes++;
            }
            catch(...){
                error = true;
                break;
            }
        }

        GDBResponse resp;
        resp.type = GDBResponse::OK;

        if(bytes != (unsigned int)req.length || error){
            resp.type = GDBResponse::ERROR;
        }

        this->connManager.sendResponse(resp);
    }

    void writeRegister(GDBRequest &req){
        GDBResponse rsp;
        if(req.reg <= this->processorInstance.nGDBRegs()){
            try{
                this->processorInstance.setGDBReg(req.value, req.reg);
                rsp.type = GDBResponse::OK;
            }
            catch(...){
                rsp.type = GDBResponse::ERROR;
            }
        }
        else{
            rsp.type = GDBResponse::ERROR;
        }
        this->connManager.sendResponse(rsp);
    }

    void killApp(){
        this->isKilled = true;
        sc_stop();
        wait();
    }

    void doStep(GDBRequest &req){
        if(req.address != 0){
            this->processorInstance.setPC(req.address);
        }

        this->step = 1;
        this->resumeExecution();
    }

    void recvIntr(){
        ;
    }

    void addBreakpoint(GDBRequest &req){
        GDBResponse resp;
        switch(req.value){
            /*case 0:
                if(this->breakManager.addBreakpoint(Breakpoint<issueWidth>::MEM, req.address, req.length))
                resp.type = GDBResponse::OK;
                else
                resp.type = GDBResponse::ERROR;
            break;*/
            case 0:
            case 1:
                if(this->breakManager.addBreakpoint(Breakpoint<issueWidth>::HW, req.address, req.length))
                    resp.type = GDBResponse::OK;
                else
                    resp.type = GDBResponse::ERROR;
            break;
            case 2:
                if(this->breakManager.addBreakpoint(Breakpoint<issueWidth>::WRITE, req.address, req.length))
                    resp.type = GDBResponse::OK;
                else
                    resp.type = GDBResponse::ERROR;
            break;
            case 3:
                if(this->breakManager.addBreakpoint(Breakpoint<issueWidth>::READ, req.address, req.length))
                    resp.type = GDBResponse::OK;
                else
                    resp.type = GDBResponse::ERROR;
            break;
            case 4:
                if(this->breakManager.addBreakpoint(Breakpoint<issueWidth>::ACCESS, req.address, req.length))
                    resp.type = GDBResponse::OK;
                else
                    resp.type = GDBResponse::ERROR;
            break;
            default:
                resp.type = GDBResponse::NOT_SUPPORTED;
            break;
        }
        this->connManager.sendResponse(resp);
    }

    void removeBreakpoint(GDBRequest &req){
        GDBResponse resp;
        if(this->breakManager.removeBreakpoint(req.address))
            resp.type = GDBResponse::OK;
        else
            resp.type = GDBResponse::ERROR;
        this->connManager.sendResponse(resp);
    }

    void genericQuery(GDBRequest &req){
        //I have to determine the query packet; in case it is Rcmd I deal with it
        GDBResponse resp;
        if(req.command != "Rcmd")
            resp.type = GDBResponse::NOT_SUPPORTED;
        else{
            //lets see which is the custom command being sent
            std::string::size_type spacePos = req.extension.find(' ');
            std::string custComm;
            if(spacePos == std::string::npos)
                custComm = req.extension;
            else
                custComm = req.extension.substr(0,  spacePos);
            if(custComm == "go"){
                //Ok,  finally I got the right command: lets see for
                //how many nanoseconds I have to execute the continue
                this->timeToGo = atof(req.extension.substr(spacePos + 1).c_str())/1e3;
                if(this->timeToGo < 0){
                    resp.type = GDBResponse::OUTPUT;
                    resp.message = "Please specify a positive offset";
                    this->connManager.sendResponse(resp);
                    resp.type = GDBResponse::NOT_SUPPORTED;
                    this->timeToGo = 0;
                }
                else
                    resp.type = GDBResponse::OK;
            }
            else if(custComm == "go_abs"){
                //This command specify to go up to a specified simulation time; the time is specified in nanoseconds
                this->timeToGo = atof(req.extension.substr(spacePos + 1).c_str())/1e3 - sc_time_stamp().to_double();
                if(this->timeToGo < 0){
                    resp.type = GDBResponse::OUTPUT;
                    resp.message = "Please specify a positive offset";
                    this->connManager.sendResponse(resp);
                    resp.type = GDBResponse::NOT_SUPPORTED;
                    this->timeToGo = 0;
                }
                else{
                    resp.type = GDBResponse::OK;
                }
            }
            else if(custComm == "status"){
                 //Returns the current status of the STUB
                 resp.type = GDBResponse::OUTPUT;
                 resp.message = "Current simulation time: " + boost::lexical_cast<std::string>(sc_time_stamp().to_double()) + " (ps)\n";
                 if(this->timeToGo != 0)
                    resp.message += "Simulating for : " + boost::lexical_cast<std::string>(this->timeToGo) + " Nanoseconds\n";
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::OK;
            }
            else if(custComm == "time"){
                //This command is simply a query to know the current simulation time
                resp.type = GDBResponse::OUTPUT;
                 resp.message = "Current simulation time: " + boost::lexical_cast<std::string>(sc_time_stamp().to_double()) + " (ps)\n";
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::OK;
            }
            else if(custComm == "help"){
                //This command is simply a query to know the current simulation time
                resp.type = GDBResponse::OUTPUT;
                 resp.message = "Help about the custom GDB commands available for the ReSP simulation platform:\n";
                 resp.message += "   monitor help:       prints the current message\n";
                 resp.message += "   monitor time:       returns the current simulation time\n";
                 resp.message += "   monitor status:     returns the status of the simulation\n";
                 resp.message += "   monitor go n:       simulates for n (ns) starting from the current time\n";
                 resp.message += "   monitor go_abs n:   simulates up to instant n (ns)\n";
                 this->connManager.sendResponse(resp);
                 resp.type = GDBResponse::OK;
            }
            else{
                resp.type = GDBResponse::NOT_SUPPORTED;
            }
        }
        this->connManager.sendResponse(resp);
    }

    ///Separates the bytes which form an integer value and puts them
    ///into an array of bytes
    template <class ValueType> void valueToBytes(std::vector<char> &byteHolder, ValueType value){
        if(this->processorInstance.matchEndian()){
            for(unsigned int i = 0; i < sizeof(ValueType); i++){
                byteHolder.push_back((char)((value & (0x0FF << 8*i)) >> 8*i));
            }
        }
        else{
            for(int i = sizeof(ValueType) - 1; i >= 0; i--){
                byteHolder.push_back((char)((value & (0x0FF << 8*i)) >> 8*i));
            }
        }
    }

    ///Converts a vector of bytes into a vector of integer values
    void bytesToValue(std::vector<char> &byteHolder, std::vector<issueWidth> &values){
        for(unsigned int i = 0; i < byteHolder.size(); i += sizeof(issueWidth)){
            issueWidth buf = 0;
            for(unsigned int k = 0; k < sizeof(issueWidth); k++){
                buf |= (byteHolder[i + k] << 8*k);
            }
            values.push_back(buf);
        }
    }

  public:
    SC_HAS_PROCESS(GDBStub);
    GDBStub(ABIIf<issueWidth> &processorInstance) :
                    sc_module("debugger"), connManager(processorInstance.matchEndian()), processorInstance(processorInstance),
                step(0), breakReached(NULL), breakEnabled(true), isKilled(false), timeout(false), isConnected(false),
                timeToGo(0), timeToJump(0), simStartTime(0), firstRun(true){
        SC_METHOD(pauseMethod);
        sensitive << this->pauseEvent;
        dont_initialize();

        end_module();
    }
    ///Method used to pause simulation
    void pauseMethod(){
        this->step = 2;
        this->timeout = true;
    }
    ///Overloading of the end_of_simulation method; it can be used to execute methods
    ///at the end of the simulation
    void end_of_simulation(){
        if(this->isConnected)
            this->signalProgramEnd();
    }
    ///Starts the connection with the GDB client
    void initialize(unsigned int port = 1500){
        this->connManager.initialize(port);
        this->isConnected = true;
        //Now I have to listen for incoming GDB messages; this will
        //be done in a new thread.
        this->startThread();
    }
    ///Method called at every cycle from the processor's main loop
    bool newIssue(const issueWidth &curPC) throw(){
        if(this->firstRun){
            this->firstRun = false;
            this->breakEnabled = false;
            boost::mutex::scoped_lock lk(this->global_mutex);
            this->gdbPausedEvent.wait(lk);
        }
        else{
            this->checkStep();
            this->checkBreakpoint(curPC);
        }
        return false;
    }
};

#endif
