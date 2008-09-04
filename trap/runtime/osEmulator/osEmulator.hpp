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

class SyscallCB;

template<class issueWidth> class OSEmulator{
    extern std::map<unsigned int, SyscallCB*> syscCallbacks;
    extern unsigned int syscMask;
    extern std::map<std::string,  std::string> env;
    extern std::map<std::string, int> sysconfmap;
    extern std::vector<std::string> programArgs;
    bool register_syscall(std::string funName, SyscallCB &callBack, std::map<std::string, sc_time> latencies, bool raiseError = true, std::string filename = "");
    void register_syscall(unsigned int address, SyscallCB &callBack, std::map<unsigned int, sc_time> latencies);
    void initSysCalls(std::string execName, std::map<std::string, sc_time> latencies);
    void initSysCalls(std::string execName);
    void reset();
    void eliminate_syscall(std::string funName);
    void eliminate_syscall(unsigned int address);
    void recreate_syscall_mask();
    void set_environ(std::string name,  std::string value);
    void add_program_args(std::vector<std::string> args);
    std::vector<std::string> getSysCallNames();
    std::vector<unsigned int> getSysCallAddr();
    extern int exitValue;
    extern int initialTime;
    int getExitValue();
    void correct_flags( int* val );
};

#endif
