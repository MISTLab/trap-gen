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
 *   This file is part of objcodeFrontend.
 *
 *   objcodeFrontend is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation; either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This library is distributed in the hope that it will be useful,
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
 *   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
 *
\***************************************************************************/

extern "C" {
#include <gelf.h>
}

// **************************** HAVE_ABI____CXA_DEMANGLE

#ifdef HAVE_CXXABI_H
#include <cxxabi.h>
#endif

#include <cstdlib>
#include <cstdio>
#include <cstdarg>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

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
#ifdef _WIN32
#include <hash_map>
#define  template_map stdext::hash_map
#else
#include <map>
#define  template_map std::map
#endif
#endif

#include <map>
#include <string>
#include <vector>
#include <list>
#include <iostream>

#include "trap_utils.hpp"

#include "elfFrontend.hpp"


trap::ELFFrontend * trap::ELFFrontend::curInstance = NULL;

trap::ELFFrontend & trap::ELFFrontend::getInstance(std::string fileName){
    if(ELFFrontend::curInstance == NULL){
        if(fileName != "")
            ELFFrontend::curInstance = new ELFFrontend(fileName);
        else
            THROW_ERROR("An instance of BFDFrontend does not exists yet, so the file name of the binary image must be specified");
    }
    return *ELFFrontend::curInstance;
}

void trap::ELFFrontend::reset(){
    delete ELFFrontend::curInstance;
    ELFFrontend::curInstance = NULL;
}

trap::ELFFrontend::ELFFrontend(std::string binaryName){
}

trap::ELFFrontend::~ELFFrontend(){
    if(this->execImage != NULL){
        if(!bfd_close_all_done(this->execImage)){
            //An Error has occurred; lets see what it is
            THROW_ERROR("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
        this->execImage = NULL;
    }
}

///Given an address, it returns the symbols found there,(more than one
///symbol can be mapped to an address). Note
///That if address is in the middle of a function, the symbol
///returned refers to the function itself
std::list<std::string> trap::ELFFrontend::symbolsAt(unsigned int address) const throw(){
    template_map<unsigned int, std::list<std::string> >::const_iterator symMap1 = this->addrToSym.find(address);
    if(symMap1 == this->addrToSym.end()){
        template_map<unsigned int, std::string>::const_iterator symMap2 = this->addrToFunction.find(address);
        std::list<std::string> functionsList;
        if(symMap2 != this->addrToFunction.end())
            functionsList.push_back(symMap2->second);
        return functionsList;
    }
    return symMap1->second;
}

///Given an address, it returns the first symbol found there
///"" if no symbol is found at the specified address; note
///That if address is in the middle of a function, the symbol
///returned refers to the function itself
std::string trap::ELFFrontend::symbolAt(unsigned int address) const throw(){
    template_map<unsigned int, std::list<std::string> >::const_iterator symMap1 = this->addrToSym.find(address);
    if(symMap1 == this->addrToSym.end()){
        template_map<unsigned int, std::string>::const_iterator symMap2 = this->addrToFunction.find(address);
        if(symMap2 != this->addrToFunction.end()){
            return symMap2->second;
        }
        else{
            return "";
        }
    }
    return symMap1->second.front();
}

///Given the name of a symbol it returns its value
///(which usually is its address);
///valid is set to false if no symbol with the specified
///name is found
unsigned int trap::ELFFrontend::getSymAddr(const std::string &symbol, bool &valid) const throw(){
    std::map<std::string, unsigned int>::const_iterator addrMap = this->symToAddr.find(symbol);
    if(addrMap == this->symToAddr.end()){
        valid = false;
        return 0;
    }
    else{
        valid = true;
        return addrMap->second;
    }
}

///Returns the name of the executable file
std::string trap::ELFFrontend::getExecName() const{
    return this->execName;
}

///Returns the end address of the loadable code
unsigned int trap::ELFFrontend::getBinaryEnd() const{
    return (this->codeSize.first + this->wordsize);
}

///Specifies whether the address is the first one of a rountine
bool trap::ELFFrontend::isRoutineEntry(unsigned int address) const{
    template_map<unsigned int, std::string>::const_iterator funNameIter = this->addrToFunction.find(address);
    template_map<unsigned int, std::string>::const_iterator endFunNames = this->addrToFunction.end();
    if(funNameIter == endFunNames)
        return false;
    std::string curName = funNameIter->second;
    funNameIter = this->addrToFunction.find(address + this->wordsize);
    if(funNameIter != endFunNames && curName == funNameIter->second){
        funNameIter = this->addrToFunction.find(address - this->wordsize);
        if(funNameIter == endFunNames || curName != funNameIter->second)
            return true;
    }
    return false;
}

///Specifies whether the address is the last one of a routine
bool trap::ELFFrontend::isRoutineExit(unsigned int address) const{
    template_map<unsigned int, std::string>::const_iterator funNameIter = this->addrToFunction.find(address);
    template_map<unsigned int, std::string>::const_iterator endFunNames = this->addrToFunction.end();
    if(funNameIter == endFunNames)
        return false;
    std::string curName = funNameIter->second;
    funNameIter = this->addrToFunction.find(address - this->wordsize);
    if(funNameIter != endFunNames && curName == funNameIter->second){
        funNameIter = this->addrToFunction.find(address + this->wordsize);
        if(funNameIter == endFunNames || curName != funNameIter->second)
            return true;
    }
    return false;
}

///Given an address, it sets fileName to the name of the source file
///which contains the code and line to the line in that file. Returns
///false if the address is not valid
bool trap::ELFFrontend::getSrcFile(unsigned int address, std::string &fileName, unsigned int &line) const{
    template_map<unsigned int, std::pair<std::string, unsigned int> >::const_iterator srcMap = this->addrToSrc.find(address);
    if(srcMap == this->addrToSrc.end()){
        return false;
    }
    else{
        fileName = srcMap->second.first;
        line = srcMap->second.second;
        return true;
    }
}

///Returns the start address of the loadable code
unsigned int trap::ELFFrontend::getBinaryStart() const{
    return this->codeSize.second;
}
