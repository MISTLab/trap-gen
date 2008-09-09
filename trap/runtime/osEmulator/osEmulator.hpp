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

#ifndef OSEMULATOR_HPP
#define OSEMULATOR_HPP

#include <map>
#include <string>

#include "ABIIf.hpp"
#include "bfdFrontend.hpp"
#include "ToolsIf.hpp"

extern unsigned int heapPointer;
extern std::map<std::string,  std::string> env;
extern std::map<std::string, int> sysconfmap;
extern std::vector<std::string> programArgs;

class SyscallCB;

template<class issueWidth> class OSEmulator : public ToolsIf{
  private:
    std::map<unsigned int, SyscallCB*> syscCallbacks;
    unsigned int syscMask;
    ABIIf<issueWidth> &processorInstance
  public:
    OSEmulator(ABIIf<issueWidth> &processorInstance) : processorInstance(processorInstance){
        this->syscMask = (unsigned int)-1L;
        heapPointer = (unsigned int)this->processorInstance.getCodeLimit();
    }
    bool register_syscall(std::string funName, SyscallCB &callBack){
        BFDFrontend &bfdFE = BFDFrontend::getInstance(execName);
        bool valid = false;
        unsigned int symAddr = bfdFE.getSymAddr(funName, valid);
        if(!valid){
            return false;
        }

        std::map<unsigned int, SyscallCB*>::iterator foundSysc = this->syscCallbacks.find(symAddr);
        if(foundSysc != this->syscCallbacks.end()){
            int numMatch = 0;
            std::map<unsigned int, SyscallCB*>::iterator allCallIter, allCallEnd;
            for(allCallIter = this->syscCallbacks.begin(), allCallEnd = this->syscCallbacks.end(); allCallIter != allCallEnd; allCallIter++){
                if(allCallIter->second == foundSysc->second)
                    numMatch++;
            }
            if(numMatch <= 1){
                delete foundSysc->second;
            }
        }

        this->syscCallbacks[symAddr] = &callBack;
        this->syscMask &= symAddr;

        return true;
    }
    void initSysCalls(std::string execName){
        BFDFrontend &bfdFE = BFDFrontend::getInstance(execName);
        bool valid = false;
        //Now I perform the registration of the basic System Calls
        bool registered = false;

        openSysCall *a = new openSysCall(this->processorInstance);
        registered = this->register_syscall("open", *a);
        registered |= this->register_syscall("_open", *a);
        if(!registered)
            delete a;
        creatSysCall *b = new creatSysCall(this->processorInstance);
        registered = this->register_syscall("creat", *b);
        registered |= this->register_syscall("_creat", *b);
        if(!registered)
            delete b;
        closeSysCall *c = new closeSysCall(this->processorInstance);
        registered = this->register_syscall("close", *c);
        registered |= this->register_syscall("_close", *c);
        if(!registered)
            delete c;
        readSysCall *d = new readSysCall(this->processorInstance);
        registered = this->register_syscall("read", *d);
        registered |= this->register_syscall("_read", *d);
        if(!registered)
            delete d;
        writeSysCall *e = new writeSysCall(this->processorInstance);
        registered = this->register_syscall("write", *e);
        registered |= this->register_syscall("_write", *e);
        if(!registered)
            delete e;
        isattySysCall *f = new isattySysCall(this->processorInstance);
        registered = this->register_syscall("isatty", *f);
        registered |= this->register_syscall("_isatty", *f);
        if(!registered)
            delete f;
        sbrkSysCall *g = new sbrkSysCall(this->processorInstance);
        registered = this->register_syscall("sbrk", *g);
        registered |= this->register_syscall("_sbrk", *g);
        if(!registered)
            delete g;
        lseekSysCall *h = new lseekSysCall(this->processorInstance);
        registered = this->register_syscall("lseek", *h);
        registered |= this->register_syscall("_lseek", *h);
        if(!registered)
            delete h;
        fstatSysCall *i = new fstatSysCall(this->processorInstance);
        registered = this->register_syscall("fstat", *i);
        registered |= this->register_syscall("_fstat", *i);
        if(!registered)
            delete i;
        _exitSysCall *j = new _exitSysCall(this->processorInstance);
        if(!this->register_syscall("_exit", *j))
            delete j;
        timesSysCall *k = new timesSysCall(this->processorInstance);
        registered = this->register_syscall("times", *k);
        registered |= this->register_syscall("_times", *k);
        if(!registered)
            delete k;
        timeSysCall *l = new timeSysCall(this->processorInstance);
        registered = this->register_syscall("time", *l);
        registered |= this->register_syscall("_time", *l);
        if(!registered)
            delete l;
        randomSysCall *m = new randomSysCall(this->processorInstance);
        registered = this->register_syscall("random", *m);
        registered |= this->register_syscall("_random", *m);
        if(!registered)
            delete m;
        getpidSysCall * n = new getpidSysCall(this->processorInstance);
        registered = this->register_syscall("getpid", *n);
        registered |= this->register_syscall("_getpid", *n);
        if(!registered)
            delete n;
        chmodSysCall * o = new chmodSysCall(this->processorInstance);
        registered = this->register_syscall("chmod", *o);
        registered |= this->register_syscall("_chmod", *o);
        if(!registered)
            delete o;
        dupSysCall * p = new dupSysCall(this->processorInstance);
        registered = this->register_syscall("dup", *p);
        registered |= this->register_syscall("_dup", *p);
        if(!registered)
            delete p;
        dup2SysCall * q = new dup2SysCall(this->processorInstance);
        registered = this->register_syscall("dup2", *q);
        registered |= this->register_syscall("_dup2", *q);
        if(!registered)
            delete q;
        getenvSysCall *r = new getenvSysCall(this->processorInstance);
        registered = this->register_syscall("getenv", *r);
        registered |= this->register_syscall("_getenv", *r);
        if(!registered)
            delete r;
        sysconfSysCall *s = new sysconfSysCall(this->processorInstance);
        if(!this->register_syscall("sysconf", *s))
            delete s;
        gettimeofdaySysCall *t = new gettimeofdaySysCall(this->processorInstance);
        registered = this->register_syscall("gettimeofday", *t);
        registered |= this->register_syscall("_gettimeofday", *t);
        if(!registered)
            delete t;
        killSysCall *u = new killSysCall(this->processorInstance);
        registered = this->register_syscall("kill", *u);
        registered |= this->register_syscall("_kill", *u);
        if(!registered)
            delete u;
        errorSysCall *v = new errorSysCall(this->processorInstance);
        registered = this->register_syscall("error", *v);
        registered |= this->register_syscall("_error", *v);
        if(!registered)
            delete v;
        chownSysCall *w = new chownSysCall(this->processorInstance);
        registered = this->register_syscall("chown", *w);
        registered |= this->register_syscall("_chown", *w);
        if(!registered)
            delete w;
        unlinkSysCall *x = new unlinkSysCall(this->processorInstance);
        registered = this->register_syscall("unlink", *x);
        registered |= this->register_syscall("_unlink", *x);
        if(!registered)
            delete x;
        usleepSysCall *y = new usleepSysCall(this->processorInstance);
        registered = this->register_syscall("usleep", *y);
        registered |= this->register_syscall("_usleep", *y);
        if(!registered)
            delete y;
        statSysCall *z = new statSysCall(this->processorInstance);
        registered = this->register_syscall("stat", *z);
        registered |= this->register_syscall("_stat", *z);
        if(!registered)
            delete z;
    }
    void set_environ(std::string name,  std::string value){
        env[name] = value;
    }
    void set_program_args(std::vector<std::string> args){
        BFDFrontend &bfdFE = BFDFrontend::getInstance();

        programArgs = args;
        mainSysCall * mainCallBack = new mainSysCall(this->processorInstance);
        if(!this->register_syscall("main", *mainCallBack);)
            THROW_EXCEPTION("Fatal Error, unable to find main function in current application");
    }
    bool newIssue(){
        //I have to go over all the registered system calls and check if there is one
        //that matches the current program counter. In case I simply call the corresponding
        //callback.
        regWidth curPC = this->processorInstance.readPC();
        if((this->syscMask & curPC) == this->syscMask){

            std::map<unsigned int, SyscallCB*>::iterator foundSysc = this->syscCallbacks.find(curPC);
            if(foundSysc != this->syscCallbacks.end()){
                (*(foundSysc->second))();
            }
        }
        return true;
    }
};

#endif
