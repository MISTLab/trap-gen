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

#ifndef BFDFRONTEND_H
#define BFDFRONTEND_H

//Part of the code of this class is taken from the binutils sources

extern "C" {
#include <bfd.h>
}

#include <map>
#include <string>
#include <list>
#include <vector>
#include <boost/regex.hpp>

namespace trap{

struct Section{
    struct bfd_section *descriptor;
    bfd_byte * data;
    bfd_vma startAddr;
    bfd_size_type datasize;
    std::string name;
};

class BFDFrontend{
  private:
    //Contains the list of all the symbols in the binary file
    asymbol **sy;
    ///Size of each assembly instruction in bytes
    unsigned int wordsize;
    ///Descriptor of the binary file
    bfd * execImage;
    std::string execName;

    ///Variables holding what read from the file
    std::map<unsigned int, std::list<std::string> > addrToSym;
    std::map<unsigned int, std::string> addrToFunction;
    std::map<std::string, unsigned int> symToAddr;
    std::map<unsigned int, std::pair<std::string, unsigned int> > addrToSrc;

    //end address and start address (not necessarily the entry point) of the loadable part of the binary file
    std::pair<unsigned int, unsigned int> codeSize;

    ///Contains a list of the sections which contain executable code
    std::vector<Section> secList;

    ///Accesses the BFD internal structures in order to get correspondence among machine code and
    ///the source code
    void readSrc();
    ///Accesses the BFD internal structures in order to get the symbols
    void readSyms();
    ///In case it is not possible to open the BFD because it is not possible to determine
    ///it target, this function extracts the list of possible targets
    std::string getMatchingFormats (char **p);
    static BFDFrontend *curInstance;
  public:
    BFDFrontend(std::string binaryName);
    ~BFDFrontend();
    static BFDFrontend & getInstance(std::string fileName = "");
    ///Given an address, it returns the symbols found there,(more than one
    ///symbol can be mapped to an address). Note
    ///That if address is in the middle of a function, the symbol
    ///returned refers to the function itself
    std::list<std::string> symbolsAt(unsigned int address);
    ///Given an address, it returns the first symbol found there
    ///"" if no symbol is found at the specified address; note
    ///That if address is in the middle of a function, the symbol
    ///returned refers to the function itself
    std::string symbolAt(unsigned int address);
    ///Given the name of a symbol it returns its value
    ///(which usually is its address);
    ///valid is set to false if no symbol with the specified
    ///name is found
    unsigned int getSymAddr(std::string symbol, bool &valid);
    ///Returns the name of the executable file
    std::string getExecName();
    ///Specifies whether the address is the entry point of a rountine
    bool isRoutineEntry(unsigned int address);
    ///Specifies whether the address is the exit point of a rountine
    bool isRoutineExit(unsigned int address);
    ///Returns the end address of the loadable code
    unsigned int getBinaryEnd();
    ///Returns the start address of the loadable code
    unsigned int getBinaryStart();
    ///Given an address, it sets fileName to the name of the source file
    ///which contains the code and line to the line in that file. Returns
    ///false if the address is not valid
    bool getSrcFile(unsigned int address, std::string &fileName, unsigned int &line);
//    ///It returns all the symbols that match the given regular expression
//    std::map<std::string,  unsigned int> findFunction(boost::regex &regEx);
};

};

#endif
