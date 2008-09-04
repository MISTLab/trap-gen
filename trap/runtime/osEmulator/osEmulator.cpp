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

#include <map>
#include <string>
#include <boost/regex.hpp>

#include "bfdFrontend.hpp"
#include "osEmulator.hpp"

#include "syscCallB.hpp"

#include "utils.hpp"

#define NEWLIB_O_RDONLY          0x0000
#define NEWLIB_O_WRONLY          0x0001
#define NEWLIB_O_RDWR            0x0002
#define NEWLIB_O_APPEND          0x0008
#define NEWLIB_O_CREAT           0x0200
#define NEWLIB_O_TRUNC           0x0400
#define NEWLIB_O_EXCL            0x0800
#define NEWLIB_O_NOCTTY          0x8000
#define NEWLIB_O_NONBLOCK        0x4000

#define CORRECT_O_RDONLY             00
#define CORRECT_O_WRONLY             01
#define CORRECT_O_RDWR               02
#define CORRECT_O_CREAT            0100
#define CORRECT_O_EXCL             0200
#define CORRECT_O_NOCTTY           0400
#define CORRECT_O_TRUNC           01000
#define CORRECT_O_APPEND          02000
#define CORRECT_O_NONBLOCK        04000

void archc::correct_flags( int* val ){
    int f = *val;
    int flags = 0;

    if( f &  NEWLIB_O_RDONLY )
        flags |= CORRECT_O_RDONLY;
    if( f &  NEWLIB_O_WRONLY )
        flags |= CORRECT_O_WRONLY;
    if( f &  NEWLIB_O_RDWR )
        flags |= CORRECT_O_RDWR;
    if( f & NEWLIB_O_CREAT )
        flags |= CORRECT_O_CREAT;
    if( f & NEWLIB_O_EXCL )
        flags |= CORRECT_O_EXCL;
    if( f & NEWLIB_O_NOCTTY )
        flags |= CORRECT_O_NOCTTY;
    if( f & NEWLIB_O_TRUNC )
        flags |= CORRECT_O_TRUNC;
    if( f & NEWLIB_O_APPEND )
        flags |= CORRECT_O_APPEND;
    if( f & NEWLIB_O_NONBLOCK )
        flags |= CORRECT_O_NONBLOCK;

    *val = flags;
}

std::map<unsigned int, archc::SyscallCB*> archc::syscCallbacks;
unsigned int archc::syscMask = (unsigned int)-1L;
BFDFrontend * bfdFE = NULL;
int archc::exitValue = 0;
int archc::initialTime = 0;
std::map<std::string,  std::string> archc::env;
std::map<std::string, int> archc::sysconfmap;
std::map<std::string,  unsigned int> regsSysCalls;
std::vector<std::string> archc::programArgs;

void archc::initSysCalls(std::string execName){
    archc::initSysCalls(execName, std::map<std::string, sc_time>());
}

void archc::reset(){
    archc::syscCallbacks.clear();
    regsSysCalls.clear();
    archc::env.clear();
    archc::sysconfmap.clear();
    archc::programArgs.clear();

    archc::exitValue = 0;
    archc::initialTime = 0;
    archc::syscMask = (unsigned int)-1L;

    if( bfdFE != NULL ) {
        delete bfdFE;
        bfdFE = NULL;
    }
}

void archc::initSysCalls(std::string execName, std::map<std::string, sc_time> latencies){
    bfdFE = new BFDFrontend(execName);
    //First of all lets set the heap pointer to the end of
    //the executable code
    bool valid = false;
    unsigned int symAddr = bfdFE->getSymAddr("__end", valid);
    if(!valid)
        symAddr = bfdFE->getSymAddr("_end", valid);
    if(!valid)
        symAddr = bfdFE->getSymAddr("end", valid);
    ac_heap_ptr = bfdFE->getBinaryEnd();
    if(valid && symAddr > ac_heap_ptr)
        ac_heap_ptr = symAddr;
    #ifndef NDEBUG
    std::cerr << "heap pointer (end of executable) set to " << std::showbase << std::hex << ac_heap_ptr << " Symbol end found at " << std::showbase << std::hex << symAddr << std::dec << std::endl;
    #endif
    //Now I perform the registration of the basic System Calls
    bool registered = false;

    openSysCall *a = new openSysCall();
    registered = archc::register_syscall("open", *a, latencies, false);
    registered |= archc::register_syscall("_open", *a, latencies, false);
    if(!registered)
        delete a;
    creatSysCall *b = new creatSysCall();
    registered = archc::register_syscall("creat", *b, latencies, false);
    registered |= archc::register_syscall("_creat", *b, latencies, false);
    if(!registered)
        delete b;
    closeSysCall *c = new closeSysCall();
    registered = archc::register_syscall("close", *c, latencies, false);
    registered |= archc::register_syscall("_close", *c, latencies, false);
    if(!registered)
        delete c;
    readSysCall *d = new readSysCall();
    registered = archc::register_syscall("read", *d, latencies, false);
    registered |= archc::register_syscall("_read", *d, latencies, false);
    if(!registered)
        delete d;
    writeSysCall *e = new writeSysCall();
    registered = archc::register_syscall("write", *e, latencies, false);
    registered |= archc::register_syscall("_write", *e, latencies, false);
    if(!registered)
        delete e;
    isattySysCall *f = new isattySysCall();
    registered = archc::register_syscall("isatty", *f, latencies, false);
    registered |= archc::register_syscall("_isatty", *f, latencies, false);
    if(!registered)
        delete f;
    sbrkSysCall *g = new sbrkSysCall();
    registered = archc::register_syscall("sbrk", *g, latencies, false);
    registered |= archc::register_syscall("_sbrk", *g, latencies, false);
    if(!registered)
        delete g;
    lseekSysCall *h = new lseekSysCall();
    registered = archc::register_syscall("lseek", *h, latencies, false);
    registered |= archc::register_syscall("_lseek", *h, latencies, false);
    if(!registered)
        delete h;
    fstatSysCall *i = new fstatSysCall();
    registered = archc::register_syscall("fstat", *i, latencies, false);
    registered |= archc::register_syscall("_fstat", *i, latencies, false);
    if(!registered)
        delete i;
    _exitSysCall *j = new _exitSysCall();
    if(!archc::register_syscall("_exit", *j, latencies, false))
        delete j;
    timesSysCall *k = new timesSysCall();
    registered = archc::register_syscall("times", *k, latencies, false);
    registered |= archc::register_syscall("_times", *k, latencies, false);
    if(!registered)
        delete k;
    timeSysCall *l = new timeSysCall();
    registered = archc::register_syscall("time", *l, latencies, false);
    registered |= archc::register_syscall("_time", *l, latencies, false);
    if(!registered)
        delete l;
    randomSysCall *m = new randomSysCall();
    registered = archc::register_syscall("random", *m, latencies, false);
    registered |= archc::register_syscall("_random", *m, latencies, false);
    if(!registered)
        delete m;
    getpidSysCall * n = new getpidSysCall();
    registered = archc::register_syscall("getpid", *n, latencies, false);
    registered |= archc::register_syscall("_getpid", *n, latencies, false);
    if(!registered)
        delete n;
    chmodSysCall * o = new chmodSysCall();
    registered = archc::register_syscall("chmod", *o, latencies, false);
    registered |= archc::register_syscall("_chmod", *o, latencies, false);
    if(!registered)
        delete o;
    dupSysCall * p = new dupSysCall();
    registered = archc::register_syscall("dup", *p, latencies, false);
    registered |= archc::register_syscall("_dup", *p, latencies, false);
    if(!registered)
        delete p;
    dup2SysCall * q = new dup2SysCall();
    registered = archc::register_syscall("dup2", *q, latencies, false);
    registered |= archc::register_syscall("_dup2", *q, latencies, false);
    if(!registered)
        delete q;
    getenvSysCall *r = new getenvSysCall();
    registered = archc::register_syscall("getenv", *r, latencies, false);
    registered |= archc::register_syscall("_getenv", *r, latencies, false);
    if(!registered)
        delete r;
    sysconfSysCall *s = new sysconfSysCall();
    if(!archc::register_syscall("sysconf", *s, latencies, false))
        delete s;
    gettimeofdaySysCall *t = new gettimeofdaySysCall();
    registered = archc::register_syscall("gettimeofday", *t, latencies, false);
    registered |= archc::register_syscall("_gettimeofday", *t, latencies, false);
    if(!registered)
        delete t;
    killSysCall *u = new killSysCall();
    registered = archc::register_syscall("kill", *u, latencies, false);
    registered |= archc::register_syscall("_kill", *u, latencies, false);
    if(!registered)
        delete u;
    errorSysCall *v = new errorSysCall();
    registered = archc::register_syscall("error", *v, latencies, false);
    registered |= archc::register_syscall("_error", *v, latencies, false);
    if(!registered)
        delete v;
    chownSysCall *w = new chownSysCall();
    registered = archc::register_syscall("chown", *w, latencies, false);
    registered |= archc::register_syscall("_chown", *w, latencies, false);
    if(!registered)
        delete w;
    unlinkSysCall *x = new unlinkSysCall();
    registered = archc::register_syscall("unlink", *x, latencies, false);
    registered |= archc::register_syscall("_unlink", *x, latencies, false);
    if(!registered)
        delete x;
    usleepSysCall *y = new usleepSysCall();
    registered = archc::register_syscall("usleep", *y, latencies, false);
    registered |= archc::register_syscall("_usleep", *y, latencies, false);
    if(!registered)
        delete y;
    statSysCall *z = new statSysCall();
    registered = archc::register_syscall("stat", *z, latencies, false);
    registered |= archc::register_syscall("_stat", *z, latencies, false);
    if(!registered)
        delete z;

    initialTime = time(0);
}

bool archc::register_syscall(std::string funName, SyscallCB &callBack, std::map<std::string, sc_time> latencies, bool raiseError, string filename){
    if(bfdFE == NULL){
        if( filename != "" ) {
            bfdFE = new BFDFrontend(filename);
        } else {
            THROW_EXCEPTION("Please specify the executable name using the \"initSysCalls\" function before calling " << __PRETTY_FUNCTION__);
        }
    }
    bool valid = false;
    unsigned int symAddr = bfdFE->getSymAddr(funName, valid);
    if(!valid){
        if(raiseError){
            THROW_EXCEPTION("No symbol " << funName << " found in executable " << bfdFE->getExecName());
        }
        else
            return false;
    }

    std::map<unsigned int, SyscallCB*>::iterator foundSysc = archc::syscCallbacks.find(symAddr);
    if(foundSysc != archc::syscCallbacks.end()){
        int numMatch = 0;
        std::map<unsigned int, SyscallCB*>::iterator allCallIter, allCallEnd;
        for(allCallIter = archc::syscCallbacks.begin(), allCallEnd = archc::syscCallbacks.end(); allCallIter != allCallEnd; allCallIter++){
            if(allCallIter->second == foundSysc->second)
                numMatch++;
        }
        if(numMatch <= 1){
            #ifndef NDEBUG
            std::cerr << "Deleting callback at address " << std::showbase << std::hex << symAddr << std::endl;
            #endif
            delete foundSysc->second;
        }
    }

    std::map<std::string, sc_time>::iterator latIter, latEnd;
    for(latIter = latencies.begin(), latEnd = latencies.end(); latIter != latEnd; latIter++){
        if(latIter->first != ""){
            boost::regex regExp(latIter->first);
            if(boost::regex_match(funName, regExp)){
                #ifndef NDEBUG
                std::cerr << "Registering latency " << latIter->second << " for system call " << funName << std::endl;
                #endif
                callBack.latency = latIter->second;
            }
        }
    }

    archc::syscCallbacks[symAddr] = &callBack;
    archc::syscMask &= symAddr;
    regsSysCalls[funName] = symAddr;
    #ifndef NDEBUG
    std::cerr << "Registering OS emulation call " << funName << " address " << std::showbase << std::hex << symAddr << " current mask " << std::showbase << std::hex << archc::syscMask << std::dec << std::endl;
    #endif

    return true;
}

void archc::register_syscall(unsigned int address, SyscallCB &callBack, std::map<unsigned int, sc_time> latencies){
    std::map<unsigned int, SyscallCB*>::iterator foundSysc = archc::syscCallbacks.find(address);
    if(foundSysc != archc::syscCallbacks.end()){
        int numMatch = 0;
        std::map<unsigned int, SyscallCB*>::iterator allCallIter, allCallEnd;
        for(allCallIter = archc::syscCallbacks.begin(), allCallEnd = archc::syscCallbacks.end(); allCallIter != allCallEnd; allCallIter++){
            if(allCallIter->second == foundSysc->second)
                numMatch++;
        }
        if(numMatch <= 1)
            delete foundSysc->second;
    }

    if(latencies.find(address) != latencies.end())
        callBack.latency = latencies[address];

    archc::syscCallbacks[address] = &callBack;
    archc::syscMask &= address;
    #ifndef NDEBUG
    std::cerr << "Registering unnamed OS emulation call address " << std::showbase << std::hex << address << " current mask " << std::showbase << std::hex << archc::syscMask << std::dec << std::endl;
    #endif
}

void archc::recreate_syscall_mask(){
    archc::syscMask = (unsigned int)-1L;
    std::map<unsigned int, SyscallCB*>::iterator syscIter, syscEnd;
    for(syscIter = archc::syscCallbacks.begin(), syscEnd = archc::syscCallbacks.end(); syscIter != syscEnd; syscEnd++){
        archc::syscMask &= syscIter->first;
    }
}

void archc::eliminate_syscall(std::string funName){
    if(bfdFE == NULL){
        THROW_EXCEPTION("Please specify the executable name using the \"initSysCalls\" function before calling " << __PRETTY_FUNCTION__);
    }
    bool valid = false;
    unsigned int symAddr = bfdFE->getSymAddr(funName, valid);
    if(!valid){
        THROW_EXCEPTION("No symbol " << funName << " found in executable " << bfdFE->getExecName());
    }
    if(archc::syscCallbacks.find(symAddr) == archc::syscCallbacks.end()){
        THROW_EXCEPTION(funName << " is not registered, unable to unregister");
    }
    if(regsSysCalls.find(funName) == regsSysCalls.end()){
        THROW_EXCEPTION(funName << " is not registered, unable to unregister");
    }

    int numMatch = 0;
    std::map<unsigned int, SyscallCB*>::iterator allCallIter, allCallEnd;
    for(allCallIter = archc::syscCallbacks.begin(), allCallEnd = archc::syscCallbacks.end(); allCallIter != allCallEnd; allCallIter++){
        if(allCallIter->second == archc::syscCallbacks[symAddr])
            numMatch++;
    }
    if(numMatch <= 1)
        delete archc::syscCallbacks[symAddr];
    archc::syscCallbacks.erase(symAddr);
    regsSysCalls.erase(funName);
    #ifndef NDEBUG
    std::cerr << "Un-Registering OS emulation call " << funName << std::endl;
    #endif
}

void archc::eliminate_syscall(unsigned int address){
    if(archc::syscCallbacks.find(address) == archc::syscCallbacks.end()){
        THROW_EXCEPTION(std::showbase << std::hex << address << " is not registered, unable to unregister" << std::dec);
    }
    int numMatch = 0;
    std::map<unsigned int, SyscallCB*>::iterator allCallIter, allCallEnd;
    for(allCallIter = archc::syscCallbacks.begin(), allCallEnd = archc::syscCallbacks.end(); allCallIter != allCallEnd; allCallIter++){
        if(allCallIter->second == archc::syscCallbacks[address])
            numMatch++;
    }
    if(numMatch <= 1)
        delete archc::syscCallbacks[address];
    archc::syscCallbacks.erase(address);

    #ifndef NDEBUG
    std::cerr << "Un-Registering unnamed OS emulation call at address " << std::showbase << std::hex << address << std::dec << std::endl;
    #endif
}

void archc::set_environ(std::string name,  std::string value){
    archc::env[name] = value;
}

void archc::add_program_args(std::vector<std::string> args){
    if(bfdFE == NULL){
        THROW_EXCEPTION("Please specify the executable name using the \"initSysCalls\" function before calling " << __PRETTY_FUNCTION__);
    }

    archc::programArgs = args;
    mainSysCall * mainCallBack = new mainSysCall();
    archc::register_syscall("main", *mainCallBack, std::map<std::string, sc_time>());
}

std::vector<std::string> archc::getSysCallNames(){
    std::vector<std::string> retVector;
    std::map<std::string,  unsigned int>::iterator sysCIter, sysCEnd;
    for(sysCIter = regsSysCalls.begin(), sysCEnd = regsSysCalls.end(); sysCIter != sysCEnd; sysCIter++){
        retVector.push_back(sysCIter->first);
    }
    return retVector;
}

std::vector<unsigned int> archc::getSysCallAddr(){
    std::vector<unsigned int> retVector;
    std::map<std::string,  unsigned int>::iterator sysCIter, sysCEnd;
    for(sysCIter = regsSysCalls.begin(), sysCEnd = regsSysCalls.end(); sysCIter != sysCEnd; sysCIter++){
        retVector.push_back(sysCIter->second);
    }
    return retVector;
}

int archc::getExitValue(){
    return exitValue;
}
