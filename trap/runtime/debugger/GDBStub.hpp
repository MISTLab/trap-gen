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
            while(stub.waitForRequest())
                ;
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
    ///Specifies whether GDB server side is waiting for input from the user
    bool isWaiting;
    ///Contains the current simulation time; when the GDB stub stops,  it might be that
    ///we want simulation to go on (this just if MYSQL is enabled): this way simulation
    ///continues (faster) but we might debug a given simulation time
    double curSimTime;
    ///In case we decided to run the simulation only for a limited ammount of time
    ///this variable contains that time
    double timeToGo;
    ///In case we decided to jump onwards or backwards for a specified ammount of time,
    ///this variable contains that time
    double timeToJump;
    ///In case the simulation is run only for a specified ammount of time,  this variable
    ///contains the simulation time at that start time
    double simStartTime;

    /********************************************************************/
    ///Checks if a breakpoint is present at the current address and
    ///in case it halts execution
    #ifndef NDEBUG
    inline void checkBreakpoint(const AddressType address) const{
    #else
    inline void checkBreakpoint(const AddressType address) const throw(){
    #endif
        if(this->breakEnabled && this->breakManager.hasBreakpoint(address)){
            breakReached = this->breakManager.getBreakPoint(address);
            #ifndef NDEBUG
            if(breakReached == NULL){
                THROW_EXCEPTION("I stopped because of a breakpoint, but no breakpoint was found");
            }
            #endif
            this->setStopped(BREAK);
            this->stepCalled = true;
        }
    }
    ///Checks if execution must be stopped because of a step command
    inline void checkStep() const throw(){
        if(this->step == 1)
            this->step++;
        else if(this->step == 2){
            this->step = 0;
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
        this->curSimTime = sc_time_stamp().to_double();

        //Now I have to behave differently depending on whether database support is enabled or not
        //if it is enabled I do not stop simulation,  while if it is not enabled I have to stop simulation in
        //order to be able to inspect the content of the processor - memory - etc...
        //Computing the next simulation time instant
        if(this->timeToGo > 0){
            this->timeToGo -= (this->curSimTime - simStartTime);
            if(this->timeToGo < 0)
                this->timeToGo = 0;
            this->simStartTime = this->curSimTime;
        }
        //pausing simulation
        if(stopReason != TIMEOUT && stopReason !=  PAUSED)
            wait();
        //Disabling break and watch points
        this->breakEnabled = false;
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

                if(this->breakReached->type == Breakpoint<AddressType>::HW ||
                            this->breakReached->type == Breakpoint<AddressType>::MEM){
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
                resp.message = "Specified Simulation time completed - Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
                this->connManager.sendResponse(resp);
                this->connManager.sendInterrupt();
            break;}
            case PAUSED:{
                //the simulation time specified has elapsed, so simulation halted
                GDBResponse resp;
                resp.type = GDBResponse::OUTPUT;
                resp.message = "Simulation Paused - Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
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
        if((!this->isKilled && !this->isWaiting) || error){
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
    bool waitForRequest(){
        GDBRequest req = connManager.processRequest();
        bool reListen = false;
        switch(req.type){
            case GDBRequest::QUEST:
                //? request: it asks the target the reason why it halted
                reListen = this->reqStopReason();
            break;
            case GDBRequest::EXCL:
                // ! request: it asks if extended mode is supported
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

    ///Method used to resume execution after GDB has issued
    ///the continue or step signal
    void resumeExecution(){
        //I'm going to restart execution, so I can again enable watch and break points
        this->breakEnabled = true;
        if(numStopped == 0){
            //I can finally resume execution
            simStartTime = this->simController.get_simulated_time();
            if(timeToGo > 0){
                this->simController.run_simulation(timeToGo);
            }
            else{
                this->simController.run_simulation();
            }
        }
    }

    /** Here start all the methods to handle the different GDB requests **/

    ///It does nothing, it simply sends an empty string back to the
    ///GDB debugger
    bool emptyAction(GDBRequest &req){
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
                AddressType regContent = this->proc.reg_read(req.reg);
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
                unsigned char memContent = this->proc.mem_read(req.address + i);
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
            this->proc.set_ac_pc(req.address);
        }

        //Now, I have to restart SystemC, since the processor
        //has to go on; note that actually SystemC restarts only
        //after all the gdbs has issued some kind of start command
        //(either a continue, a step ...)
        this->resumeExecution();

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
        return false;
    }

    bool readRegisters(){
        //I have to read all the general purpose registers and
        //send their content back to GDB
        GDBResponse resp;
        resp.type = GDBResponse::REG_READ;
        for(unsigned int i = 0; i < this->proc.nRegs(); i++){
            try{
                AddressType regContent = this->proc.reg_read(i);
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
                this->proc.reg_write(i, *dataIter);
            }
            catch(...){
                error = true;
            }
            i++;
        }

        GDBResponse resp;

        if(i != (unsigned int)this->proc.nRegs() || error){
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
                this->proc.mem_write(req.address + bytes, *dataIter);
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
                this->proc.reg_write(req.reg, req.value);
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
        if(req.address != 0){
            this->proc.set_ac_pc(req.address);
        }

        this->step = 1;
        this->resumeExecution();

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
             if(custComm == "go"){
                 //Ok,  finally I got the right command: lets see for
                 //how many nanoseconds I have to execute the continue
                timeToGo = atof(req.extension.substr(spacePos + 1).c_str());
                 if(timeToGo < 0){
                     resp.type = GDBResponse::OUTPUT;
                     resp.message = "Please specify a positive offset";
                     this->connManager.sendResponse(resp);
                     resp.type = GDBResponse::NOT_SUPPORTED;
                     timeToGo = 0;
                 }
                 else
                    resp.type = GDBResponse::OK;
            }
            else if(custComm == "go_abs"){
                 //This command specify to go up to a specified simulation time; the time is specified in nanoseconds
                 timeToGo = atof(req.extension.substr(spacePos + 1).c_str()) - sc_time_stamp().to_double();
                 if(timeToGo < 0){
                     direction = BACKWARD;
                     timeToGo = -timeToGo;
                     resp.type = GDBResponse::OK;
                 }
                 else{
                    direction = FORWARD;
                    resp.type = GDBResponse::OK;
                }
             }
            else if(custComm == "status"){
                 //Returns the current status of the STUB
                 resp.type = GDBResponse::OUTPUT;
                 resp.message = "Current simulation time: " + boost::lexical_cast<std::string>(this->simController.get_simulated_time()) + " (ps)\n";
                 if(timeToGo != 0)
                    resp.message += "Simulating for : " + boost::lexical_cast<std::string>(timeToGo) + " Nanoseconds\n";
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
        return true;
    }

    ///Separates the bytes which form an integer value and puts them
    ///into an array of bytes
    template <class ValueType> void valueToBytes(std::vector<char> &byteHolder, ValueType value){
        if(!endianess){
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
    void bytesToValue(std::vector<char> &byteHolder, std::vector<AddressType> &values){
        for(unsigned int i = 0; i < byteHolder.size(); i += sizeof(AddressType)){
            AddressType buf = 0;
            for(unsigned int k = 0; k < sizeof(AddressType); k++){
                buf |= (byteHolder[i + k] << 8*k);
            }
            values.push_back(buf);
        }
    }

  public:
    GDBStub(ABIIf<issueWidth> &processorInstance, unsigned int port = 1500) :
                    sc_module("debugger"), connManager(processorInstance.matchEndian()), processorInstance(processorInstance),
                step(0), breakReached(NULL), breakEnabled(true), isKilled(false), isWaiting(true){
        this->connManager.initialize(port);
        //Now I have to listen for incoming GDB messages; this will
        //be done in a new thread, so that the console remains responsive;
        this->isGDBConnected = true;
        this->startThread();
    }
    ///Overloading of the end_of_simulation method; it can be used to execute methods
    ///at the end of the simulation
    void end_of_simulation(){
        this->signalProgramEnd();
    }
    ///Method called at every cycle from the processor's main loop
    bool newIssue(const issueWidth &curPC) const throw(){
        this->checkStep();
        this->checkBreakpoint(curPC);
        return false;
    }
};

#endif
