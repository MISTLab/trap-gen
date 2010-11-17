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
 *   the Free Software Foundation; either version 3 of the License, or
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
 *   (c) Luca Fossati, fossati@elet.polimi.it, fossati.l@gmail.com
 *
\***************************************************************************/

#ifndef ANALYZER_HPP
#define ANALYZER_HPP

#include <iostream>
#include <fstream>
#include <string>
#include <map>

#include <boost/filesystem.hpp>

namespace trap{

struct MemAccessType;

class MemAnalyzer{
    private:
    std::ifstream dumpFile;
    unsigned int memSize;

    ///Given an array of chars (either in hex or decimal form) if converts it to the
    ///corresponding integer representation
    unsigned int toIntNum(const std::string &numStr);

    public:
    MemAnalyzer(std::string fileName, std::string memSize);
    ~MemAnalyzer();
    ///Creates the image of the memory as it was at cycle procCycle
    void createMemImage(boost::filesystem::path &outFile, double simTime = -1);
    ///Returns the first memory access that modifies the address addr after
    ///procCycle
    std::map<unsigned int, MemAccessType> getFirstModAfter(std::string addr, unsigned int width, double simTime = 0);
    ///Returns the last memory access that modified addr
    std::map<unsigned int, MemAccessType> getLastMod(std::string addr, unsigned int width);
    ///Prints all the modifications done to address addr
    void getAllModifications(std::string addr, boost::filesystem::path &outFile, unsigned int width, double initSimTime = 0, double endSimTime = -1);
};

}

#endif
