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

class SyscallCB;

template<class issueWidth> class OSEmulator{
  private:
    std::map<unsigned int, SyscallCB*> syscCallbacks;
    unsigned int syscMask;
    std::map<std::string,  std::string> env;
    std::map<std::string, int> sysconfmap;
    std::vector<std::string> programArgs;
  public:
    bool register_syscall(std::string funName, SyscallCB &callBack){
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
                delete foundSysc->second;
            }
        }

        std::map<std::string, sc_time>::iterator latIter, latEnd;
        for(latIter = latencies.begin(), latEnd = latencies.end(); latIter != latEnd; latIter++){
            if(latIter->first != ""){
                boost::regex regExp(latIter->first);
                if(boost::regex_match(funName, regExp)){
                    callBack.latency = latIter->second;
                }
            }
        }

        archc::syscCallbacks[symAddr] = &callBack;
        archc::syscMask &= symAddr;
        regsSysCalls[funName] = symAddr;

        return true;
    }
    void initSysCalls(std::string execName){
        BFDFrontend &bfdFE = BFDFrontend::getInstance(execName);
        bool valid = false;
        //Now I perform the registration of the basic System Calls
        bool registered = false;

        openSysCall *a = new openSysCall();
        registered = this->register_syscall("open", *a, latencies, false);
        registered |= this->register_syscall("_open", *a, latencies, false);
        if(!registered)
            delete a;
        creatSysCall *b = new creatSysCall();
        registered = this->register_syscall("creat", *b, latencies, false);
        registered |= this->register_syscall("_creat", *b, latencies, false);
        if(!registered)
            delete b;
        closeSysCall *c = new closeSysCall();
        registered = this->register_syscall("close", *c, latencies, false);
        registered |= this->register_syscall("_close", *c, latencies, false);
        if(!registered)
            delete c;
        readSysCall *d = new readSysCall();
        registered = this->register_syscall("read", *d, latencies, false);
        registered |= this->register_syscall("_read", *d, latencies, false);
        if(!registered)
            delete d;
        writeSysCall *e = new writeSysCall();
        registered = this->register_syscall("write", *e, latencies, false);
        registered |= this->register_syscall("_write", *e, latencies, false);
        if(!registered)
            delete e;
        isattySysCall *f = new isattySysCall();
        registered = this->register_syscall("isatty", *f, latencies, false);
        registered |= this->register_syscall("_isatty", *f, latencies, false);
        if(!registered)
            delete f;
        sbrkSysCall *g = new sbrkSysCall();
        registered = this->register_syscall("sbrk", *g, latencies, false);
        registered |= this->register_syscall("_sbrk", *g, latencies, false);
        if(!registered)
            delete g;
        lseekSysCall *h = new lseekSysCall();
        registered = this->register_syscall("lseek", *h, latencies, false);
        registered |= this->register_syscall("_lseek", *h, latencies, false);
        if(!registered)
            delete h;
        fstatSysCall *i = new fstatSysCall();
        registered = this->register_syscall("fstat", *i, latencies, false);
        registered |= this->register_syscall("_fstat", *i, latencies, false);
        if(!registered)
            delete i;
        _exitSysCall *j = new _exitSysCall();
        if(!this->register_syscall("_exit", *j, latencies, false))
            delete j;
        timesSysCall *k = new timesSysCall();
        registered = this->register_syscall("times", *k, latencies, false);
        registered |= this->register_syscall("_times", *k, latencies, false);
        if(!registered)
            delete k;
        timeSysCall *l = new timeSysCall();
        registered = this->register_syscall("time", *l, latencies, false);
        registered |= this->register_syscall("_time", *l, latencies, false);
        if(!registered)
            delete l;
        randomSysCall *m = new randomSysCall();
        registered = this->register_syscall("random", *m, latencies, false);
        registered |= this->register_syscall("_random", *m, latencies, false);
        if(!registered)
            delete m;
        getpidSysCall * n = new getpidSysCall();
        registered = this->register_syscall("getpid", *n, latencies, false);
        registered |= this->register_syscall("_getpid", *n, latencies, false);
        if(!registered)
            delete n;
        chmodSysCall * o = new chmodSysCall();
        registered = this->register_syscall("chmod", *o, latencies, false);
        registered |= this->register_syscall("_chmod", *o, latencies, false);
        if(!registered)
            delete o;
        dupSysCall * p = new dupSysCall();
        registered = this->register_syscall("dup", *p, latencies, false);
        registered |= this->register_syscall("_dup", *p, latencies, false);
        if(!registered)
            delete p;
        dup2SysCall * q = new dup2SysCall();
        registered = this->register_syscall("dup2", *q, latencies, false);
        registered |= this->register_syscall("_dup2", *q, latencies, false);
        if(!registered)
            delete q;
        getenvSysCall *r = new getenvSysCall();
        registered = this->register_syscall("getenv", *r, latencies, false);
        registered |= this->register_syscall("_getenv", *r, latencies, false);
        if(!registered)
            delete r;
        sysconfSysCall *s = new sysconfSysCall();
        if(!this->register_syscall("sysconf", *s, latencies, false))
            delete s;
        gettimeofdaySysCall *t = new gettimeofdaySysCall();
        registered = this->register_syscall("gettimeofday", *t, latencies, false);
        registered |= this->register_syscall("_gettimeofday", *t, latencies, false);
        if(!registered)
            delete t;
        killSysCall *u = new killSysCall();
        registered = this->register_syscall("kill", *u, latencies, false);
        registered |= this->register_syscall("_kill", *u, latencies, false);
        if(!registered)
            delete u;
        errorSysCall *v = new errorSysCall();
        registered = this->register_syscall("error", *v, latencies, false);
        registered |= this->register_syscall("_error", *v, latencies, false);
        if(!registered)
            delete v;
        chownSysCall *w = new chownSysCall();
        registered = this->register_syscall("chown", *w, latencies, false);
        registered |= this->register_syscall("_chown", *w, latencies, false);
        if(!registered)
            delete w;
        unlinkSysCall *x = new unlinkSysCall();
        registered = this->register_syscall("unlink", *x, latencies, false);
        registered |= this->register_syscall("_unlink", *x, latencies, false);
        if(!registered)
            delete x;
        usleepSysCall *y = new usleepSysCall();
        registered = this->register_syscall("usleep", *y, latencies, false);
        registered |= this->register_syscall("_usleep", *y, latencies, false);
        if(!registered)
            delete y;
        statSysCall *z = new statSysCall();
        registered = this->register_syscall("stat", *z, latencies, false);
        registered |= this->register_syscall("_stat", *z, latencies, false);
        if(!registered)
            delete z;
    }
    void set_environ(std::string name,  std::string value){
        archc::env[name] = value;
    }
    void set_program_args(std::vector<std::string> args){
        if(bfdFE == NULL){
            THROW_EXCEPTION("Please specify the executable name using the \"initSysCalls\" function before calling " << __PRETTY_FUNCTION__);
        }

        archc::programArgs = args;
        mainSysCall * mainCallBack = new mainSysCall();
        archc::register_syscall("main", *mainCallBack, std::map<std::string, sc_time>());
    }
    void correct_flags(int &val){
        int flags = 0;

        if( val &  NEWLIB_O_RDONLY )
            flags |= CORRECT_O_RDONLY;
        if( val &  NEWLIB_O_WRONLY )
            flags |= CORRECT_O_WRONLY;
        if( val &  NEWLIB_O_RDWR )
            flags |= CORRECT_O_RDWR;
        if( val & NEWLIB_O_CREAT )
            flags |= CORRECT_O_CREAT;
        if( val & NEWLIB_O_EXCL )
            flags |= CORRECT_O_EXCL;
        if( val & NEWLIB_O_NOCTTY )
            flags |= CORRECT_O_NOCTTY;
        if( val & NEWLIB_O_TRUNC )
            flags |= CORRECT_O_TRUNC;
        if( val & NEWLIB_O_APPEND )
            flags |= CORRECT_O_APPEND;
        if( val & NEWLIB_O_NONBLOCK )
            flags |= CORRECT_O_NONBLOCK;

        val = flags;
    }
};

#endif
