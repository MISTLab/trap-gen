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

#ifndef SYSCCALLB_H
#define SYSCCALLB_H

#include <systemc.h>

///Base class for each emulated system call;
///Operator () implements the behaviour of the
///emulated call
class SyscallCB{
    public:
    sc_time latency;
    SyscallCB(sc_time latency = SC_ZERO_TIME) : latency(latency){}
    virtual ~SyscallCB(){}
    virtual bool operator()(ac_syscall_base &processorInstance) = 0;
};

class openSysCall : public SyscallCB{
    public:
    openSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class creatSysCall : public SyscallCB{
    public:
    creatSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class closeSysCall : public SyscallCB{
    public:
    closeSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class readSysCall : public SyscallCB{
    public:
    readSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class writeSysCall : public SyscallCB{
    public:
    writeSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class isattySysCall : public SyscallCB{
    public:
    isattySysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class sbrkSysCall : public SyscallCB{
    public:
    sbrkSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class lseekSysCall : public SyscallCB{
    public:
    lseekSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class fstatSysCall : public SyscallCB{
    public:
    fstatSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class statSysCall : public SyscallCB{
    public:
    statSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class _exitSysCall : public SyscallCB{
    public:
    _exitSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class timesSysCall : public SyscallCB{
    public:
    timesSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class timeSysCall : public SyscallCB{
    public:
    timeSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class randomSysCall : public SyscallCB{
    public:
    randomSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class getpidSysCall : public SyscallCB{
    public:
    getpidSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class chmodSysCall : public SyscallCB{
    public:
    chmodSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class dupSysCall : public SyscallCB{
    public:
    dupSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class dup2SysCall : public SyscallCB{
    public:
    dup2SysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class getenvSysCall : public SyscallCB{
    public:
    getenvSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class sysconfSysCall : public SyscallCB{
    public:
    sysconfSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class gettimeofdaySysCall : public SyscallCB{
    public:
    gettimeofdaySysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class killSysCall : public SyscallCB{
    public:
    killSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class errorSysCall : public SyscallCB{
    public:
    errorSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class chownSysCall : public SyscallCB{
    public:
    chownSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class unlinkSysCall : public SyscallCB{
    public:
    unlinkSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class usleepSysCall : public SyscallCB{
    public:
    usleepSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

class mainSysCall : public SyscallCB{
    public:
    mainSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB(latency){}
    bool operator()(ac_syscall_base &processorInstance);
};

#endif
