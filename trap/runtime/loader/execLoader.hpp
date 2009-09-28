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

#ifndef EXECLOADER_HPP
#define EXECLOADER_HPP

#include <string>

extern "C" {
#include <bfd.h>
}

namespace trap{

class ExecLoader{
  private:
    ///Variable holding the binary image of the application according to the BFD format
    bfd * execImage;
    ///Specifies whether a normal binary file (ELF; COFF, etc.) or a plain file (just the
    ///opcodes of the instructions) was used.
    bool plainFile;
    ///Variables holding info on the program being loaded
    unsigned char * programData;
    unsigned int progDim;
    unsigned int dataStart;

    ///examines the bfd in order to find the sections containing data
    ///to be loaded; at the same time it fills the programData
    ///array
    void loadProgramData();
    std::string getMatchingFormats (char **p);
  public:
    ///Initializes the loader of executable files by creating
    ///the corresponding bfd image of the executable file
    ///specified as parameter
    ExecLoader(std::string fileName, bool plainFile = false);
    ~ExecLoader();
    ///Returns the entry point of the loaded program
    ///(usually the same as the program start address, but
    ///not always)
    unsigned int getProgStart();
    ///Returns the start address of the program being loaded
    ///(the lowest address of the program)
    unsigned int getDataStart();
    ///Returns the dimension of the loaded program
    unsigned int getProgDim();
    ///Returns a pointer to the array contianing the program data
    unsigned char * getProgData();
};

};

#endif
