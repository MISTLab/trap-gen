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

#include <map>
#include <string>
#include <iostream>

#include <boost/program_options.hpp>
#include <boost/filesystem.hpp>

#include "trap_utils.hpp"

#include "memAccessType.hpp"
#include "analyzer.hpp"

using namespace trap;

int main(int argc, char *argv[]){
    boost::program_options::options_description desc("Memory Analyzer");
    desc.add_options()
    ("help,h", "produces the help message")
    ("operation,o", boost::program_options::value<int>(), "specifies the operation which we want to execute [1: create memory image - 2: get all modifications to a specified address - 3: gets the first modification to an address after a given simulation time 4: - gets the last modification to an address]")
    ("dump,d", boost::program_options::value<std::string>(), "the name of the dump file")
    ("outFile,f", boost::program_options::value<std::string>(), "the name of the output file for the operations which need it (1 and 2)")
    ("address,a", boost::program_options::value<std::string>(), "the address of which we want to get the modifications")
    ("startTime,s", boost::program_options::value<double>(), "the time at which we want to analyze the modifications (start time if needed by the chosen option)")
    ("endTime,e", boost::program_options::value<double>(), "the end time until which we want to get the modification")
    ("memSize,m", boost::program_options::value<std::string>(), "the maximum memory size [default 5MB]")
    ("width,w", boost::program_options::value<unsigned int>(), "the width of each data operation in bytes [default 4 bytes] (used only by 2, 3, 4)")
    ;

    boost::program_options::variables_map vm;
    boost::program_options::store(boost::program_options::parse_command_line(argc, argv, desc), vm);
    boost::program_options::notify(vm);

    // Checking that the parameters are correctly specified
    if(vm.count("help") != 0){
        std::cout << desc << std::endl;
        return 0;
    }
    if(vm.count("operation") == 0){
        std::cerr << "Error, it is necessary to specify the operation which has to be executed" << std::endl;
        std::cerr << desc << std::endl;
        return -1;
    }
    if(vm.count("dump") == 0){
        std::cerr << "Error, it is necessary to specify the name of the dump file" << std::endl;
        std::cerr << desc << std::endl;
        return -1;
    }
    std::string memSize = boost::lexical_cast<std::string>(5242880);
    unsigned int width = 4;
    if(vm.count("width") > 0){
        width = vm["width"].as<unsigned int>();
    }
    if(vm.count("memSize") > 0){
        memSize = vm["memSize"].as<std::string>();
    }
    MemAnalyzer analyzer(vm["dump"].as<std::string>(), memSize);
    switch(vm["operation"].as<int>()){
        case 1:{
            if(vm.count("outFile") == 0){
                std::cerr << "Error, it is necessary to specify the output file with the (1) operation" << std::endl;
                std::cerr << desc << std::endl;
                return -1;
            }
            boost::filesystem::path outFilePath = boost::filesystem::system_complete(boost::filesystem::path(vm["outFile"].as<std::string>(), boost::filesystem::native));
            if(vm.count("startTime") == 0){
                analyzer.createMemImage(outFilePath);
            }
            else{
                analyzer.createMemImage(outFilePath, vm["startTime"].as<double>());
            }
        break;}
        case 2:{
            if(vm.count("address") == 0){
                std::cerr << "Error, it is necessary to specify the address with the (2) operation" << std::endl;
                std::cerr << desc << std::endl;
                return -1;
            }
            if(vm.count("outFile") == 0){
                std::cerr << "Error, it is necessary to specify the output file with the (2) operation" << std::endl;
                std::cerr << desc << std::endl;
                return -1;
            }
            double startTime = 0;
            if(vm.count("startTime") > 0){
                startTime = vm["startTime"].as<double>();
            }
            double endTime = -1;
            if(vm.count("endTime") > 0){
                endTime = vm["endTime"].as<double>();
            }
            boost::filesystem::path outFilePath = boost::filesystem::system_complete(boost::filesystem::path(vm["outFile"].as<std::string>(), boost::filesystem::native));
            analyzer.getAllModifications(vm["address"].as<std::string>(), outFilePath, width, startTime, endTime);
        break;}
        case 3:{
            if(vm.count("address") == 0){
                std::cerr << "Error, it is necessary to specify the address with the (3) operation" << std::endl;
                std::cerr << desc << std::endl;
                return -1;
            }
            std::map<unsigned int, MemAccessType> modification;
            if(vm.count("startTime") == 0){
                modification = analyzer.getFirstModAfter(vm["address"].as<std::string>(), width);
            }
            else{
                modification = analyzer.getFirstModAfter(vm["address"].as<std::string>(), width, vm["startTime"].as<double>());
            }
            std::map<unsigned int, MemAccessType>::iterator modIter, modEnd;
            for(modIter = modification.begin(), modEnd = modification.end(); modIter != modEnd; modIter++){
                std::cout << "Address " << std::hex << std::showbase << modIter->second.address << " - Value " << std::hex << std::showbase << modIter->second.val << " - PC " << std::hex << std::showbase << modIter->second.programCounter << " - Time " << std::dec << modIter->second.simulationTime << std::endl;
            }
        break;}
        case 4:{
            if(vm.count("address") == 0){
                std::cerr << "Error, it is necessary to specify the address with the (4) operation" << std::endl;
                std::cerr << desc << std::endl;
                return -1;
            }
            std::map<unsigned int, MemAccessType> modification = analyzer.getLastMod(vm["address"].as<std::string>(), width);
            std::map<unsigned int, MemAccessType>::iterator modIter, modEnd;
            for(modIter = modification.begin(), modEnd = modification.end(); modIter != modEnd; modIter++){
                std::cout << "Address " << std::hex << std::showbase << modIter->second.address << " - Value " << std::hex << std::showbase << modIter->second.val << " - PC " << std::hex << std::showbase << modIter->second.programCounter << " - Time " << std::dec << modIter->second.simulationTime << std::endl;
            }
        break;}
        default:
            THROW_EXCEPTION("Error, unrecognized option " << vm["operation"].as<int>());
        break;
    }

    return 0;
}
