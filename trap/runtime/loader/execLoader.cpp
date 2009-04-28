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

#include <string>
#include <map>
#include <iostream>

#include "utils.hpp"

extern "C" {
#include <bfd.h>
}

#include "execLoader.hpp"


ExecLoader::ExecLoader(std::string fileName){
    this->programData = NULL;
    this->execImage = NULL;
    this->progDim = 0;
    this->dataStart = 0;
    char ** matching = NULL;
    bfd_init();
    this->execImage = bfd_openr(fileName.c_str(), "default");
    if(this->execImage == NULL){
        //An error has occurred,  lets see what it is
        THROW_ERROR("Error in reading input file " << fileName << " --> " << bfd_errmsg(bfd_get_error()));
    }
    if (bfd_check_format (this->execImage, bfd_archive)){
        THROW_ERROR("Error in reading input file " << fileName << " --> The input file is an archive; executable file required");
    }
    if (!bfd_check_format_matches (this->execImage, bfd_object, &matching)){
        THROW_ERROR("Error in reading input file " << fileName << " --> The input file is not an object file or the target is ambiguous -- " << this->getMatchingFormats(matching));
    }
    this->loadProgramData();
}

ExecLoader::~ExecLoader(){
    if(this->execImage != NULL){
        if(!bfd_close_all_done(this->execImage)){
            //An Error has occurred; lets see what it is
            THROW_ERROR("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
    }
    if(this->programData != NULL){
        delete [] this->programData;
    }
}

unsigned int ExecLoader::getProgStart(){
    if(this->execImage == NULL){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    return bfd_get_start_address(this->execImage);
}

unsigned int ExecLoader::getProgDim(){
    if(this->execImage == NULL){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    return this->progDim;
}

unsigned char * ExecLoader::getProgData(){
    if(this->execImage == NULL){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    if(this->programData == NULL){
        THROW_ERROR("The program data was not correcly computed");
    }
    return this->programData;
}

unsigned int ExecLoader::getDataStart(){
    if(this->execImage == NULL){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    return this->dataStart;
}

void ExecLoader::loadProgramData(){
    bfd_section *p = NULL;
    std::map<unsigned long, unsigned char> memMap;
    for (p = this->execImage->sections; p != NULL; p = p->next){
        flagword flags = bfd_get_section_flags(this->execImage, p);
        if((flags & SEC_ALLOC) != 0 && (flags & SEC_DEBUGGING) == 0 && (flags & SEC_THREAD_LOCAL) == 0){
            //Ok,  this is a section which must be in the final executable;
            //Lets see if it has content: if not I have to pad the section with zeros,
            //otherwise I load it
            bfd_size_type datasize = bfd_section_size(this->execImage, p);
            bfd_vma vma = bfd_get_section_vma(this->execImage, p);
            std::map<unsigned long, unsigned char>::iterator curMapPos = memMap.begin();
            if((flags & SEC_HAS_CONTENTS) != 0){
//                #ifndef NDEBUG
//                std::cerr << "Loading data fom section " << p->name << " Start Address " << std::showbase << std::hex << vma << " Size " << std::hex << datasize << " End Address " << std::hex << datasize + vma << std::dec << " Swap Endianess " << swapEndianess << " flags " << std::hex << std::showbase << flags << std::dec << std::endl;
//                #endif
                bfd_byte *data = new bfd_byte[datasize];
                bfd_get_section_contents (this->execImage, p, data, 0, datasize);
                for(unsigned int i = 0; i < datasize; i++){
                     curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i, data[i]));
                }
                delete [] data;
            }
            else{
/*                #ifndef NDEBUG
                std::cerr << "Filling with 0s section " << p->name << " Start Address " << std::showbase << std::hex << vma << " Size " << std::hex << datasize << " End Address " << std::hex << datasize + vma << std::dec << std::endl;
                #endif*/
                for(unsigned int i = 0; i < datasize; i++)
                    curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i, 0));
            }
        }
    }
    //ok,  I now have all the map of the memory; I simply have to fill in the
    //this->programData  array
    this->dataStart = memMap.begin()->first;
    this->progDim = memMap.rbegin()->first - this->dataStart + 1;
    this->programData = new unsigned char[this->progDim];
    std::map<unsigned long, unsigned char>::iterator memBeg,  memEnd;
    for(memBeg = memMap.begin(),  memEnd = memMap.end(); memBeg != memEnd; memBeg++){
        this->programData[memBeg->first - this->dataStart] = memBeg->second;
    }
}

std::string ExecLoader::getMatchingFormats (char **p){
    std::string match = "";
    if(p != NULL){
        while (*p){
            match += *p;
            *p++;
            match += " ";
        }
    }
    return match;
}
