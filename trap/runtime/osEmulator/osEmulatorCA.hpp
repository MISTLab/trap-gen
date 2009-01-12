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

#ifndef OSEMULATORCA_HPP
#define OSEMULATORCA_HPP

#include <map>
#include <string>

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
#include <ext/hash_map>
#define  template_map __gnu_cxx::hash_map
#endif

#include "ABIIf.hpp"
#include "bfdFrontend.hpp"
#include "ToolsIf.hpp"

#include "syscCallB.hpp"

template<class issueWidth, int stageOffset> class OSEmulatorCA : public ToolsIf<issueWidth>, OSEmulatorBase{
  private:
    template_map<issueWidth, SyscallCB<issueWidth>* > syscCallbacks;
    ABIIf<issueWidth> &processorInstance;
    typename template_map<issueWidth, SyscallCB<issueWidth>* >::const_iterator syscCallbacksEnd;
    void *NOPInstr;

    unsigned int countBits(issueWidth bits){
        unsigned int numBits = 0;
        for(unsigned int i = 0; i < sizeof(issueWidth)*8; i++){
            if((bits & (0x1 << i)) != 0)
                numBits++;
        }
        return numBits;
    }

    bool register_syscall(std::string funName, SyscallCB<issueWidth> &callBack){
        BFDFrontend &bfdFE = BFDFrontend::getInstance();
        bool valid = false;
        unsigned int symAddr = bfdFE.getSymAddr(funName, valid);
        if(!valid){
            return false;
        }

        typename template_map<issueWidth, SyscallCB<issueWidth>* >::iterator foundSysc = this->syscCallbacks.find(symAddr);
        if(foundSysc != this->syscCallbacks.end()){
            int numMatch = 0;
            typename template_map<issueWidth, SyscallCB<issueWidth>* >::iterator allCallIter, allCallEnd;
            for(allCallIter = this->syscCallbacks.begin(), allCallEnd = this->syscCallbacks.end(); allCallIter != allCallEnd; allCallIter++){
                if(allCallIter->second == foundSysc->second)
                    numMatch++;
            }
            if(numMatch <= 1){
                delete foundSysc->second;
            }
        }

        this->syscCallbacks[symAddr] = &callBack;
        this->syscCallbacksEnd = this->syscCallbacks.end();

        return true;
    }

  public:
    OSEmulatorCA(ABIIf<issueWidth> &processorInstance, void *NOPInstr) : processorInstance(processorInstance), NOPInstr(NOPInstr){
        OSEmulatorBase::heapPointer = (unsigned int)this->processorInstance.getCodeLimit();
        this->syscCallbacksEnd = this->syscCallbacks.end();
    }
    void initSysCalls(std::string execName){
        BFDFrontend::getInstance(execName);
        //Now I perform the registration of the basic System Calls
        bool registered = false;

        openSysCall<issueWidth> *a = new openSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("open", *a);
        registered |= this->register_syscall("_open", *a);
        if(!registered)
            delete a;
        creatSysCall<issueWidth> *b = new creatSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("creat", *b);
        registered |= this->register_syscall("_creat", *b);
        if(!registered)
            delete b;
        closeSysCall<issueWidth> *c = new closeSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("close", *c);
        registered |= this->register_syscall("_close", *c);
        if(!registered)
            delete c;
        readSysCall<issueWidth> *d = new readSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("read", *d);
        registered |= this->register_syscall("_read", *d);
        if(!registered)
            delete d;
        writeSysCall<issueWidth> *e = new writeSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("write", *e);
        registered |= this->register_syscall("_write", *e);
        if(!registered)
            delete e;
        isattySysCall<issueWidth> *f = new isattySysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("isatty", *f);
        registered |= this->register_syscall("_isatty", *f);
        if(!registered)
            delete f;
        sbrkSysCall<issueWidth> *g = new sbrkSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("sbrk", *g);
        registered |= this->register_syscall("_sbrk", *g);
        if(!registered)
            delete g;
        lseekSysCall<issueWidth> *h = new lseekSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("lseek", *h);
        registered |= this->register_syscall("_lseek", *h);
        if(!registered)
            delete h;
        fstatSysCall<issueWidth> *i = new fstatSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("fstat", *i);
        registered |= this->register_syscall("_fstat", *i);
        if(!registered)
            delete i;
        _exitSysCall<issueWidth> *j = new _exitSysCall<issueWidth>(this->processorInstance);
        if(!this->register_syscall("_exit", *j))
            delete j;
        timesSysCall<issueWidth> *k = new timesSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("times", *k);
        registered |= this->register_syscall("_times", *k);
        if(!registered)
            delete k;
        timeSysCall<issueWidth> *l = new timeSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("time", *l);
        registered |= this->register_syscall("_time", *l);
        if(!registered)
            delete l;
        randomSysCall<issueWidth> *m = new randomSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("random", *m);
        registered |= this->register_syscall("_random", *m);
        if(!registered)
            delete m;
        getpidSysCall<issueWidth> * n = new getpidSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("getpid", *n);
        registered |= this->register_syscall("_getpid", *n);
        if(!registered)
            delete n;
        chmodSysCall<issueWidth> * o = new chmodSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("chmod", *o);
        registered |= this->register_syscall("_chmod", *o);
        if(!registered)
            delete o;
        dupSysCall<issueWidth> * p = new dupSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("dup", *p);
        registered |= this->register_syscall("_dup", *p);
        if(!registered)
            delete p;
        dup2SysCall<issueWidth> * q = new dup2SysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("dup2", *q);
        registered |= this->register_syscall("_dup2", *q);
        if(!registered)
            delete q;
        getenvSysCall<issueWidth> *r = new getenvSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("getenv", *r);
        registered |= this->register_syscall("_getenv", *r);
        if(!registered)
            delete r;
        sysconfSysCall<issueWidth> *s = new sysconfSysCall<issueWidth>(this->processorInstance);
        if(!this->register_syscall("sysconf", *s))
            delete s;
        gettimeofdaySysCall<issueWidth> *t = new gettimeofdaySysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("gettimeofday", *t);
        registered |= this->register_syscall("_gettimeofday", *t);
        if(!registered)
            delete t;
        killSysCall<issueWidth> *u = new killSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("kill", *u);
        registered |= this->register_syscall("_kill", *u);
        if(!registered)
            delete u;
        errorSysCall<issueWidth> *v = new errorSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("error", *v);
        registered |= this->register_syscall("_error", *v);
        if(!registered)
            delete v;
        chownSysCall<issueWidth> *w = new chownSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("chown", *w);
        registered |= this->register_syscall("_chown", *w);
        if(!registered)
            delete w;
        unlinkSysCall<issueWidth> *x = new unlinkSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("unlink", *x);
        registered |= this->register_syscall("_unlink", *x);
        if(!registered)
            delete x;
        usleepSysCall<issueWidth> *y = new usleepSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("usleep", *y);
        registered |= this->register_syscall("_usleep", *y);
        if(!registered)
            delete y;
        statSysCall<issueWidth> *z = new statSysCall<issueWidth>(this->processorInstance);
        registered = this->register_syscall("stat", *z);
        registered |= this->register_syscall("_stat", *z);
        if(!registered)
            delete z;
        mainSysCall<issueWidth> * mainCallBack = new mainSysCall<issueWidth>(this->processorInstance);
        if(!this->register_syscall("main", *mainCallBack))
            THROW_EXCEPTION("Fatal Error, unable to find main function in current application");
    }
    bool newIssue(const issueWidth &curPC, const void *curInstr) throw(){
        //I have to go over all the registered system calls and check if there is one
        //that matches the current program counter. In case I simply call the corresponding
        //callback.
        if(curInstr != NOPInstr){
            typename template_map<issueWidth, SyscallCB<issueWidth>* >::const_iterator foundSysc = this->syscCallbacks.find(curPC + stageOffset);
            if(foundSysc != this->syscCallbacksEnd){
                return (*(foundSysc->second))();
            }
        }
        return false;
    }
    virtual ~OSEmulatorCA(){}
};

#endif
