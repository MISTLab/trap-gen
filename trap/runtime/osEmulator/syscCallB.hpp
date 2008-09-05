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

#include "ABIIf.hpp"
#include <systemc.h>

#include <iostream>
#include <string>
#include <map>
#include <systemc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#if !(defined(__MACOSX__) || defined(__DARWIN__) || defined(__APPLE__))
#include <error.h>
#endif
#include <errno.h>
#if !defined(errno) && !defined(HAVE_ERRNO_DECL)
extern int errno;
#endif
#include <sstream>
#include <sys/times.h>
#include <time.h>

///Base class for each emulated system call;
///Operator () implements the behaviour of the
///emulated call
template<class wordSize> class SyscallCB{
    public:
    sc_time latency;
    SyscallCB(sc_time latency = SC_ZERO_TIME) : latency(latency){}
    virtual ~SyscallCB(){}
    virtual bool operator()(ABIIf<wordSize> &processorInstance) = 0;
};

template<class wordSize> class openSysCall : public SyscallCB<wordSize>{
    public:
    openSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class creatSysCall : public SyscallCB<wordSize>{
    public:
    creatSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class closeSysCall : public SyscallCB<wordSize>{
    public:
    closeSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class readSysCall : public SyscallCB<wordSize>{
    public:
    readSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class writeSysCall : public SyscallCB<wordSize>{
    public:
    writeSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class isattySysCall : public SyscallCB<wordSize>{
    public:
    isattySysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class sbrkSysCall : public SyscallCB<wordSize>{
    public:
    sbrkSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class lseekSysCall : public SyscallCB<wordSize>{
    public:
    lseekSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class fstatSysCall : public SyscallCB<wordSize>{
    public:
    fstatSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class statSysCall : public SyscallCB<wordSize>{
    public:
    statSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class _exitSysCall : public SyscallCB<wordSize>{
    public:
    _exitSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class timesSysCall : public SyscallCB<wordSize>{
    public:
    timesSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class timeSysCall : public SyscallCB<wordSize>{
    public:
    timeSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class randomSysCall : public SyscallCB<wordSizeABIIf<wordSize>>{
    public:
    randomSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class getpidSysCall : public SyscallCB<wordSize>{
    public:
    getpidSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class chmodSysCall : public SyscallCB<wordSize>{
    public:
    chmodSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class dupSysCall : public SyscallCB<wordSize>{
    public:
    dupSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class dup2SysCall : public SyscallCB<wordSize>{
    public:
    dup2SysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class getenvSysCall : public SyscallCB<wordSize>{
    public:
    getenvSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class sysconfSysCall : public SyscallCB<wordSize>{
    public:
    sysconfSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class gettimeofdaySysCall : public SyscallCB<wordSize>{
    public:
    gettimeofdaySysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class killSysCall : public SyscallCB<wordSize>{
    public:
    killSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class errorSysCall : public SyscallCB<wordSize>{
    public:
    errorSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class chownSysCall : public SyscallCB<wordSize>{
    public:
    chownSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class unlinkSysCall : public SyscallCB<wordSize>{
    public:
    unlinkSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class usleepSysCall : public SyscallCB<wordSize>{
    public:
    usleepSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

template<class wordSize> class mainSysCall : public SyscallCB<wordSize>{
    public:
    mainSysCall(sc_time latency = SC_ZERO_TIME) : SyscallCB<wordSize>(latency){}
    bool operator()(ABIIf<wordSize> &processorInstance);
};

#endif
