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

#include "osEmulator.hpp"
#include "syscCallB.hpp"

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

#include "controller.hpp"
#include "utils.hpp"

bool openSysCall::operator()(ac_syscall_base &processorInstance){
    if(this->latency.to_double() > 0)
        wait(this->latency);

    unsigned char pathname[100];
    processorInstance.get_buffer(0, pathname, 100);
    #ifndef NDEBUG
    std::cerr << "Opening file -->" << pathname << "<--" << std::endl;
    #endif
    int flags = processorInstance.get_arg(1);
    archc::correct_flags(&flags);
    int mode = processorInstance.get_arg(2);
    int ret = ::open((char*)pathname, flags, mode);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();

    return false;
}

bool creatSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("creat");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    unsigned char pathname[100];
    processorInstance.get_buffer(0, pathname, 100);
    int mode = processorInstance.get_arg(1);
    #ifndef NDEBUG
    std::cerr << "Creating file -->" << pathname << "<--" << std::endl;
    #endif
    int ret = ::creat((char*)pathname, mode);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool closeSysCall::operator()(ac_syscall_base &processorInstance){
  DEBUG_SYSCALL("close");
  if(this->latency.to_double() > 0)
    wait(this->latency);

  resp::sc_controller::disableLatency = true;
  int fd = processorInstance.get_arg(0);
  if( fd == fileno(stdin) || fd == fileno(stdout) || fd == fileno(stderr) ){
     processorInstance.set_retVal(0, 0);
     processorInstance.return_from_syscall();
     resp::sc_controller::disableLatency = false;
     return false;
  }
  int ret = ::close(fd);
  processorInstance.set_retVal(0, ret);
  processorInstance.return_from_syscall();
  resp::sc_controller::disableLatency = false;

  return false;
}

bool readSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("read");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int fd = processorInstance.get_arg(0);
    unsigned count = processorInstance.get_arg(2);
    unsigned char *buf = new unsigned char[count];
    int ret = ::read(fd, buf, count);
    processorInstance.set_buffer(1, buf, ret);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    delete [] buf;
    return false;
}

bool writeSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("write");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int fd = processorInstance.get_arg(0);
    unsigned count = processorInstance.get_arg(2);
    unsigned char *buf = new unsigned char[count];
    processorInstance.get_buffer(1, buf, count);
    int ret = ::write(fd, buf, count);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    delete [] buf;
    return false;
}

bool isattySysCall::operator()(ac_syscall_base &processorInstance){
  DEBUG_SYSCALL("isatty");
  if(this->latency.to_double() > 0)
    wait(this->latency);

  resp::sc_controller::disableLatency = true;
  int desc = processorInstance.get_arg(0);
  int ret = ::isatty(desc);
  processorInstance.set_retVal(0, ret);
  processorInstance.return_from_syscall();
  resp::sc_controller::disableLatency = false;

  return false;
}

bool sbrkSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("sbrk");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    unsigned int base = ac_heap_ptr;
    unsigned int increment = processorInstance.get_arg(0);

    #ifndef NDEBUG
    std::cerr << "Allocating " << increment << " bytes starting at address " << std::showbase << std::hex << base << std::dec << std::endl;
    #endif

    ac_heap_ptr += increment;

    //I try to read from meory to see if it is possible to access the just allocated address;
    //In case it is not it means that I'm out of memory and I signal the error
    unsigned char memValue;
    try{
        processorInstance.set_arg(0, ac_heap_ptr);
        processorInstance.get_buffer(0, &memValue, 1);
        processorInstance.set_arg(0, increment);
        processorInstance.set_retVal(0, base);
    }
    catch(...){
        processorInstance.set_retVal(0, -1);
        std::cerr << "SBRK: tried to allocate " << increment << " bytes of memory starting at address 0x" << std::hex << base << std::dec << " but it seems there is not enough memory" << std::endl;
    }

    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool lseekSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("lseek");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int fd = processorInstance.get_arg(0);
    int offset = processorInstance.get_arg(1);
    int whence = processorInstance.get_arg(2);
    int ret = ::lseek(fd, offset, whence);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool fstatSysCall::operator()(ac_syscall_base &processorInstance){
    struct stat buf_stat;
    DEBUG_SYSCALL("fstat");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int fd = processorInstance.get_arg(0);
    int retAddr = processorInstance.get_arg(1);
    int ret = ::fstat(fd, &buf_stat);
    if(ret >= 0 && retAddr != 0){
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_dev), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_ino), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_mode), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_nlink), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_uid), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_gid), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_rdev), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_size), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_atime), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 8);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_mtime), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 8);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_ctime), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 8);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_blksize), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_blocks), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_arg(1, retAddr);
    }
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool statSysCall::operator()(ac_syscall_base &processorInstance){
    struct stat buf_stat;
    DEBUG_SYSCALL("stat");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    unsigned char pathname[100];
    processorInstance.get_buffer(0, pathname, 100);
    int retAddr = processorInstance.get_arg(1);
    int ret = ::stat((char *)pathname, &buf_stat);
    if(ret >= 0 && retAddr != 0){
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_dev), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_ino), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_mode), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_nlink), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_uid), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_gid), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_rdev), 2);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 2);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_size), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_atime), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 8);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_mtime), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 8);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_ctime), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 8);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_blksize), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_buffer_endian(1, (unsigned char *)&(buf_stat.st_blocks), 4);
        processorInstance.set_arg(1, processorInstance.get_arg(1) + 4);
        processorInstance.set_arg(1, retAddr);
    }
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool _exitSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("_exit");
    if(this->latency.to_double() > 0)
        wait(this->latency);
    archc::exitValue = processorInstance.get_arg(0);
    std::cerr << std::endl << "Program exited with value " << exitValue << std::endl << std::endl;
    if(sc_is_running())
        sc_stop();
    return false;
}

bool timesSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("times");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    unsigned int curSimTime = (unsigned int)(sc_time_stamp().to_double()/1.0e+6);
    int timesRetLoc = processorInstance.get_arg(0);
    if(timesRetLoc != 0){
        struct tms buf;
        buf.tms_utime = curSimTime;
        buf.tms_stime = curSimTime;
        buf.tms_cutime = curSimTime;
        buf.tms_cstime = curSimTime;
        processorInstance.set_buffer_endian(0, (unsigned char *)&(buf.tms_utime), 4);
        timesRetLoc += 4;
        processorInstance.set_arg(0, timesRetLoc);
        processorInstance.set_buffer_endian(0, (unsigned char *)&(buf.tms_stime), 4);
        timesRetLoc += 4;
        processorInstance.set_arg(0, timesRetLoc);
        processorInstance.set_buffer_endian(0, (unsigned char *)&(buf.tms_cutime), 4);
        timesRetLoc += 4;
        processorInstance.set_arg(0, timesRetLoc);
        processorInstance.set_buffer_endian(0, (unsigned char *)&(buf.tms_cstime), 4);
        processorInstance.set_arg(0, timesRetLoc - 12);
    }
    processorInstance.set_retVal(0, curSimTime);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool timeSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("time");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int t = processorInstance.get_arg(0);
    int ret = initialTime + (int)(sc_time_stamp().to_double()/1.0e+12);
    if (t != 0)
        processorInstance.set_buffer_endian(0, (unsigned char *)&ret, 4);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool randomSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("random");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int ret = ::random();
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool getpidSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("getpid");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    processorInstance.set_retVal(0, 123);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool chmodSysCall::operator()(ac_syscall_base &processorInstance){
    unsigned char pathname[100];
    DEBUG_SYSCALL("chmod");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    processorInstance.get_buffer(0, pathname, 100);
    int mode = processorInstance.get_arg(0);
    int ret = ::chmod((char*)pathname, mode);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

/*#include <Python.h>
#include <boost/python/exec.hpp>
#include <boost/python/import.hpp>
#include <boost/python/object.hpp>*/

bool dupSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("dup");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int fd = processorInstance.get_arg(0);
    int ret = ::dup(fd);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool dup2SysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("dup2");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int fd = processorInstance.get_arg(0);
    int newfd = processorInstance.get_arg(1);
    int ret = ::dup2(fd,  newfd);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool getenvSysCall::operator()(ac_syscall_base &processorInstance){
    char envname[100];
    DEBUG_SYSCALL("getenv");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int envNameAddr = processorInstance.get_arg(0);
    if(envNameAddr != 0){
        processorInstance.get_buffer(0, (unsigned char *)envname, 100);
        #ifndef NDEBUG
        std::cerr << "Reading variable -->" << envname << "<--" << std::endl;
        #endif
        std::map<std::string,  std::string>::iterator curEnv = archc::env.find((std::string(envname)));
        if(curEnv == archc::env.end()){
            #ifndef NDEBUG
            std::cerr << "Not Found" << std::endl;
            #endif
            processorInstance.set_retVal(0, 0);
            processorInstance.return_from_syscall();
        }
        else{
            //I have to allocate memory for the result on the simulated memory;
            //I then have to copy the read environment variable here and return
            //the pointer to it
            #ifndef NDEBUG
            std::cerr << "Found with value -->" << curEnv->second << "<--" << std::endl;
            #endif
            unsigned int base = ac_heap_ptr;
            ac_heap_ptr += curEnv->second.size();
            processorInstance.set_arg(0, base);
            processorInstance.set_buffer(0, (unsigned char *)curEnv->second.c_str(), curEnv->second.size() + 1);
            processorInstance.set_arg(0, envNameAddr);
            processorInstance.set_retVal(0, base);
            processorInstance.return_from_syscall();
        }
    }
    else{
            processorInstance.set_retVal(0, 0);
            processorInstance.return_from_syscall();
    }
    resp::sc_controller::disableLatency = false;

    return false;
}

bool gettimeofdaySysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("gettimeofday");
    if(this->latency.to_double() > 0)
        wait(this->latency);
    double curSimTime = sc_time_stamp().to_double();

    #ifndef NDEBUG
    std::cerr << "Current simulated time " << curSimTime << std::endl;
    #endif

    resp::sc_controller::disableLatency = true;
    int timesRetLoc = processorInstance.get_arg(0);
    if(timesRetLoc != 0){
        struct timeval buf;
        buf.tv_sec = (time_t)(curSimTime/1.0e+12);
        buf.tv_usec = (suseconds_t)((curSimTime - buf.tv_sec*1.0e+12)/1.0e+6);
        processorInstance.set_buffer_endian(0, (unsigned char *)&(buf.tv_sec), 4);
        timesRetLoc += 4;
        processorInstance.set_arg(0, timesRetLoc);
        processorInstance.set_buffer_endian(0, (unsigned char *)&(buf.tv_usec), 4);
        processorInstance.set_arg(0, timesRetLoc - 4);
    }
    processorInstance.set_retVal(0, 0);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool killSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("kill");
    if(this->latency.to_double() > 0)
        wait(this->latency);
    THROW_EXCEPTION("KILL SystemCall not yet implemented");
    return false;
}

bool errorSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("error");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int status = processorInstance.get_arg(0);
    int errnum = processorInstance.get_arg(1);
    char*  errorString = ::strerror(errnum);
    if(status != 0){
        archc::exitValue = status;
        std::cerr << std::endl << "Program exited with value " << archc::exitValue << std::endl << " Error message: " << errorString << std::endl;
        if(sc_is_running())
            sc_stop();
    }
    else{
        std::cerr << "An error occurred in the execution of the program: message = " << errorString << std::endl;
    }
    resp::sc_controller::disableLatency = false;

    return false;
}

bool chownSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("chwon");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    unsigned char pathname[100];
    processorInstance.get_buffer(0, pathname, 100);
    uid_t owner = processorInstance.get_arg(1);
    gid_t group = processorInstance.get_arg(2);
    #ifndef NDEBUG
    std::cerr << "Chowning file -->" << pathname << "<--" << std::endl;
    #endif
    int ret = ::chown((char*)pathname, owner, group);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool unlinkSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("unlink");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    unsigned char pathname[100];
    processorInstance.get_buffer(0, pathname, 100);
    #ifndef NDEBUG
    std::cerr << "Unlinking file -->" << pathname << "<--" << std::endl;
    #endif
    int ret = ::unlink((char*)pathname);
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool usleepSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("usleep");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    //Since we have a single process this function doesn't do anything :-)
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}

bool mainSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("main");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    //I have to write the program arguments into the heap
    //and also set the appropriate registers
    #ifndef NDEBUG
    std::cerr << "Going to set " << archc::programArgs.size() << " program arguments" << std::endl;
    #endif
    unsigned int argAddr = ((unsigned int)ac_heap_ptr) + (archc::programArgs.size() + 1)*4;
    unsigned int argNumAddr = ac_heap_ptr;
    unsigned char zero = '\x0';
    std::vector<std::string>::iterator argsIter, argsEnd;
    for(argsIter = archc::programArgs.begin(), argsEnd = archc::programArgs.end(); argsIter != argsEnd; argsIter++){
        #ifndef NDEBUG
        std::cerr << "Setting argument --> " << *argsIter << std::endl;
        #endif
        processorInstance.set_arg(0, argNumAddr);
        argNumAddr += 4;
        processorInstance.set_buffer_endian(0, (unsigned char *)&argAddr, 4);
        processorInstance.set_arg(0, argAddr);
        processorInstance.set_buffer(0, (unsigned char *)argsIter->c_str(), argsIter->size());
        argAddr += argsIter->size();
        processorInstance.set_arg(0, argAddr);
        processorInstance.set_buffer(0, &zero, 1);
        argAddr++;
    }
    processorInstance.set_arg(0, argNumAddr);
    processorInstance.set_buffer_endian(0, &zero, 4);

    processorInstance.set_arg(0, archc::programArgs.size());
    processorInstance.set_arg(1, ac_heap_ptr);
    ac_heap_ptr = argAddr;
    resp::sc_controller::disableLatency = false;

    return true;
}

/*
 *  sysconf values per IEEE Std 1003.1, 2004 Edition
 */
#define NEWLIB_SC_ARG_MAX                       0
#define NEWLIB_SC_CHILD_MAX                     1
#define NEWLIB_SC_CLK_TCK                       2
#define NEWLIB_SC_NGROUPS_MAX                   3
#define NEWLIB_SC_OPEN_MAX                      4
#define NEWLIB_SC_JOB_CONTROL                   5
#define NEWLIB_SC_SAVED_IDS                     6
#define NEWLIB_SC_VERSION                       7
#define NEWLIB_SC_PAGESIZE                      8
#define NEWLIB_SC_PAGE_SIZE                     NEWLIB_SC_PAGESIZE
/* These are non-POSIX values we accidentally introduced in 2000 without
   guarding them.  Keeping them unguarded for backward compatibility. */
#define NEWLIB_SC_NPROCESSORS_CONF              9
#define NEWLIB_SC_NPROCESSORS_ONLN             10
#define NEWLIB_SC_PHYS_PAGES                   11
#define NEWLIB_SC_AVPHYS_PAGES                 12
/* End of non-POSIX values. */
#define NEWLIB_SC_MQ_OPEN_MAX                  13
#define NEWLIB_SC_MQ_PRIO_MAX                  14
#define NEWLIB_SC_RTSIG_MAX                    15
#define NEWLIB_SC_SEM_NSEMS_MAX                16
#define NEWLIB_SC_SEM_VALUE_MAX                17
#define NEWLIB_SC_SIGQUEUE_MAX                 18
#define NEWLIB_SC_TIMER_MAX                    19
#define NEWLIB_SC_TZNAME_MAX                   20
#define NEWLIB_SC_ASYNCHRONOUS_IO              21
#define NEWLIB_SC_FSYNC                        22
#define NEWLIB_SC_MAPPED_FILES                 23
#define NEWLIB_SC_MEMLOCK                      24
#define NEWLIB_SC_MEMLOCK_RANGE                25
#define NEWLIB_SC_MEMORY_PROTECTION            26
#define NEWLIB_SC_MESSAGE_PASSING              27
#define NEWLIB_SC_PRIORITIZED_IO               28
#define NEWLIB_SC_REALTIME_SIGNALS             29
#define NEWLIB_SC_SEMAPHORES                   30
#define NEWLIB_SC_SHARED_MEMORY_OBJECTS        31
#define NEWLIB_SC_SYNCHRONIZED_IO              32
#define NEWLIB_SC_TIMERS                       33
#define NEWLIB_SC_AIO_LISTIO_MAX               34
#define NEWLIB_SC_AIO_MAX                      35
#define NEWLIB_SC_AIO_PRIO_DELTA_MAX           36
#define NEWLIB_SC_DELAYTIMER_MAX               37
#define NEWLIB_SC_THREAD_KEYS_MAX              38
#define NEWLIB_SC_THREAD_STACK_MIN             39
#define NEWLIB_SC_THREAD_THREADS_MAX           40
#define NEWLIB_SC_TTY_NAME_MAX                 41
#define NEWLIB_SC_THREADS                      42
#define NEWLIB_SC_THREAD_ATTR_STACKADDR        43
#define NEWLIB_SC_THREAD_ATTR_STACKSIZE        44
#define NEWLIB_SC_THREAD_PRIORITY_SCHEDULING   45
#define NEWLIB_SC_THREAD_PRIO_INHERIT          46
/* NEWLIB_SC_THREAD_PRIO_PROTECT was NEWLIB_SC_THREAD_PRIO_CEILING in early drafts */
#define NEWLIB_SC_THREAD_PRIO_PROTECT          47
#define NEWLIB_SC_THREAD_PRIO_CEILING          NEWLIB_SC_THREAD_PRIO_PROTECT
#define NEWLIB_SC_THREAD_PROCESS_SHARED        48
#define NEWLIB_SC_THREAD_SAFE_FUNCTIONS        49
#define NEWLIB_SC_GETGR_R_SIZE_MAX             50
#define NEWLIB_SC_GETPW_R_SIZE_MAX             51
#define NEWLIB_SC_LOGIN_NAME_MAX               52
#define NEWLIB_SC_THREAD_DESTRUCTOR_ITERATIONS 53
#define NEWLIB_SC_ADVISORY_INFO                54
#define NEWLIB_SC_ATEXIT_MAX                   55
#define NEWLIB_SC_BARRIERS                     56
#define NEWLIB_SC_BC_BASE_MAX                  57
#define NEWLIB_SC_BC_DIM_MAX                   58
#define NEWLIB_SC_BC_SCALE_MAX                 59
#define NEWLIB_SC_BC_STRING_MAX                60
#define NEWLIB_SC_CLOCK_SELECTION              61
#define NEWLIB_SC_COLL_WEIGHTS_MAX             62
#define NEWLIB_SC_CPUTIME                      63
#define NEWLIB_SC_EXPR_NEST_MAX                64
#define NEWLIB_SC_HOST_NAME_MAX                65
#define NEWLIB_SC_IOV_MAX                      66
#define NEWLIB_SC_IPV6                         67
#define NEWLIB_SC_LINE_MAX                     68
#define NEWLIB_SC_MONOTONIC_CLOCK              69
#define NEWLIB_SC_RAW_SOCKETS                  70
#define NEWLIB_SC_READER_WRITER_LOCKS          71
#define NEWLIB_SC_REGEXP                       72
#define NEWLIB_SC_RE_DUP_MAX                   73
#define NEWLIB_SC_SHELL                        74
#define NEWLIB_SC_SPAWN                        75
#define NEWLIB_SC_SPIN_LOCKS                   76
#define NEWLIB_SC_SPORADIC_SERVER              77
#define NEWLIB_SC_SS_REPL_MAX                  78
#define NEWLIB_SC_SYMLOOP_MAX                  79
#define NEWLIB_SC_THREAD_CPUTIME               80
#define NEWLIB_SC_THREAD_SPORADIC_SERVER       81
#define NEWLIB_SC_TIMEOUTS                     82
#define NEWLIB_SC_TRACE                        83
#define NEWLIB_SC_TRACE_EVENT_FILTER           84
#define NEWLIB_SC_TRACE_EVENT_NAME_MAX         85
#define NEWLIB_SC_TRACE_INHERIT                86
#define NEWLIB_SC_TRACE_LOG                    87
#define NEWLIB_SC_TRACE_NAME_MAX               88
#define NEWLIB_SC_TRACE_SYS_MAX                89
#define NEWLIB_SC_TRACE_USER_EVENT_MAX         90
#define NEWLIB_SC_TYPED_MEMORY_OBJECTS         91
#define NEWLIB_SC_V6_ILP32_OFF32               92
#define NEWLIB_SC_XBS5_ILP32_OFF32             NEWLIB_SC_V6_ILP32_OFF32
#define NEWLIB_SC_V6_ILP32_OFFBIG              93
#define NEWLIB_SC_XBS5_ILP32_OFFBIG            NEWLIB_SC_V6_ILP32_OFFBIG
#define NEWLIB_SC_V6_LP64_OFF64                94
#define NEWLIB_SC_XBS5_LP64_OFF64              NEWLIB_SC_V6_LP64_OFF64
#define NEWLIB_SC_V6_LPBIG_OFFBIG              95
#define NEWLIB_SC_XBS5_LPBIG_OFFBIG            NEWLIB_SC_V6_LPBIG_OFFBIG
#define NEWLIB_SC_XOPEN_CRYPT                  96
#define NEWLIB_SC_XOPEN_ENH_I18N               97
#define NEWLIB_SC_XOPEN_LEGACY                 98
#define NEWLIB_SC_XOPEN_REALTIME               99
#define NEWLIB_SC_STREAM_MAX                  100
#define NEWLIB_SC_PRIORITY_SCHEDULING         101
#define NEWLIB_SC_XOPEN_REALTIME_THREADS      102
#define NEWLIB_SC_XOPEN_SHM                   103
#define NEWLIB_SC_XOPEN_STREAMS               104
#define NEWLIB_SC_XOPEN_UNIX                  105
#define NEWLIB_SC_XOPEN_VERSION               106
#define NEWLIB_SC_2_CHAR_TERM                 107
#define NEWLIB_SC_2_C_BIND                    108
#define NEWLIB_SC_2_C_DEV                     109
#define NEWLIB_SC_2_FORT_DEV                  110
#define NEWLIB_SC_2_FORT_RUN                  111
#define NEWLIB_SC_2_LOCALEDEF                 112
#define NEWLIB_SC_2_PBS                       113
#define NEWLIB_SC_2_PBS_ACCOUNTING            114
#define NEWLIB_SC_2_PBS_CHECKPOINT            115
#define NEWLIB_SC_2_PBS_LOCATE                116
#define NEWLIB_SC_2_PBS_MESSAGE               117
#define NEWLIB_SC_2_PBS_TRACK                 118
#define NEWLIB_SC_2_SW_DEV                    119
#define NEWLIB_SC_2_UPE                       120
#define NEWLIB_SC_2_VERSION                   121

bool sysconfSysCall::operator()(ac_syscall_base &processorInstance){
    DEBUG_SYSCALL("sysconf");
    if(this->latency.to_double() > 0)
        wait(this->latency);

    resp::sc_controller::disableLatency = true;
    int argId = processorInstance.get_arg(0);
    int ret = -1;
    switch(argId){
        case NEWLIB_SC_NPROCESSORS_ONLN:
            if(sysconfmap.find("_SC_NPROCESSORS_ONLN") == sysconfmap.end())
                ret = 1;
            else
                ret = sysconfmap["_SC_NPROCESSORS_ONLN"];
        break;
        case NEWLIB_SC_CLK_TCK:
            if(sysconfmap.find("_SC_CLK_TCK") == sysconfmap.end())
                ret = 1000000;
            else
                ret = sysconfmap["_SC_CLK_TCK"];
        break;
        default:
            ret = -1;
        break;
    }
    processorInstance.set_retVal(0, ret);
    processorInstance.return_from_syscall();
    resp::sc_controller::disableLatency = false;

    return false;
}
