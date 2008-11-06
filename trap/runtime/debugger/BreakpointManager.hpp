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

#ifndef BREAKPOINTMANAGER_HPP
#define BREAKPOINTMANAGER_HPP

#include <iostream>
#include <vector>
#include <ext/hash_map>
#include <string>

template <class AddressType> struct Breakpoint{
    enum Type{MEM=0, HW, WRITE, READ, ACCESS};
    AddressType address;
    unsigned int length;
    Type type;
};

template <class AddressType> class BreakpointManager{
  private:
    __gnu_cxx::hash_map<AddressType, Breakpoint<AddressType> > breakpoints;
    __gnu_cxx::hash_map<AddressType, Breakpoint<AddressType> >::const_iterator lastBreak;
  public:
    //Eliminates all the breakpoints
    void clearAllBreaks(){
        this->breakpoints.clear();
    }
    bool addBreakpoint(typename Breakpoint<AddressType>::Type type, AddressType address, unsigned int length){
        #ifndef NDEBUG
        std::cerr << "GDB-break " << __PRETTY_FUNCTION__ << ": Adding Breakpoint at address " << address << std::endl;
        #endif
        if(this->breakpoints.find(address) != this->lastBreak)
            return false;
        this->breakpoints[address].address = address;
        this->breakpoints[address].length = length;
        this->breakpoints[address].type = type;
        this->lastBreak = this->breakpoints.end();
        return true;
    }

    bool removeBreakpoint(AddressType address){
        #ifndef NDEBUG
        std::cerr << "GDB-break " << __PRETTY_FUNCTION__ << ": Removing Breakpoint at address " << address << std::endl;
        #endif
        if(this->breakpoints.find(address) == this->lastBreak)
            return false;
        this->breakpoints.erase(address);
        return true;
    }

    bool hasBreakpoint(AddressType address){
        return this->breakpoints.find(address) != this->lastBreak;
    }

    Breakpoint<AddressType> * getBreakPoint(AddressType address){
        if(this->breakpoints.find(address) == this->lastBreak)
            return NULL;
        else
            return &(this->breakpoints[address]);
    }

    __gnu_cxx::hash_map<AddressType, Breakpoint<AddressType> > & getBreakpoints(){
        return this->breakpoints;
    }
};

#endif
