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

#include <string>
#include <map>
#include <iostream>

#include "trap_utils.hpp"

extern "C" {
#include <gelf.h>
}

#include "elfFrontend.hpp"
#include "execLoader.hpp"

#include <boost/filesystem.hpp>
#include <boost/filesystem/fstream.hpp>

trap::ExecLoader::ExecLoader(std::string fileName, bool plainFile) : plainFile(plainFile){
    this->programData = NULL;
    this->execImage = NULL;
    this->progDim = 0;
    this->dataStart = 0;
    char ** matching = NULL;
    if(plainFile){
        ///Here I simply have to read the input file, putting all the bytes
        ///of its content in the programData array
        boost::filesystem::path fileNamePath = boost::filesystem::system_complete(boost::filesystem::path(fileName, boost::filesystem::native));
        if ( !boost::filesystem::exists( fileNamePath ) ){
            THROW_EXCEPTION("Path " << fileName << " specified in the executable loader does not exists");
        }
        std::ifstream plainExecFile(fileName.c_str(), std::ifstream::in | std::ifstream::binary);
        if(!plainExecFile.good())
            THROW_EXCEPTION("Error in opening file " << fileName);

        //Here I determine the size of the program being loaded
        plainExecFile.seekg (0, std::ios::end);
        this->progDim = plainExecFile.tellg();
        plainExecFile.seekg (0, std::ios::beg);
        this->programData = new unsigned char[this->progDim];
        //Now I read the whole file
        plainExecFile.read((char *)this->programData, this->progDim);
        this->dataStart = 0;
        plainExecFile.close();
    }
    else{
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
}

trap::ExecLoader::~ExecLoader(){
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

unsigned int trap::ExecLoader::getProgStart(){
    if(this->execImage == NULL && !this->plainFile){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    if(this->plainFile)
        return this->dataStart;
    else
        return bfd_get_start_address(this->execImage);
}

unsigned int trap::ExecLoader::getProgDim(){
    if(this->execImage == NULL && !this->plainFile){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    return this->progDim;
}

unsigned char * trap::ExecLoader::getProgData(){
    if(this->execImage == NULL && !this->plainFile){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    if(this->programData == NULL){
        THROW_ERROR("The program data was not correcly computed");
    }
    return this->programData;
}

unsigned int trap::ExecLoader::getDataStart(){
    if(this->execImage == NULL && !this->plainFile){
        THROW_ERROR("The binary parser not yet correcly created");
    }
    return this->dataStart;
}
