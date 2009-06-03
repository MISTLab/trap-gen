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

extern "C" {
#include <bfd.h>
}

#include <sys/types.h>
#include <cstdio>
#include <cstdarg>

#include <map>
#include <string>
#include <vector>
#include <list>
#include <iostream>

#include "trap_utils.hpp"

#include <boost/regex.hpp>

#include "bfdFrontend.hpp"

#define DMGL_NO_OPTS     0              /* For readability... */
#define DMGL_PARAMS      (1 << 0)       /* Include function args */
#define DMGL_ANSI        (1 << 1)       /* Include const, volatile, etc */
#define DMGL_JAVA        (1 << 2)       /* Demangle as Java rather than C++. */
#define DMGL_VERBOSE     (1 << 3)       /* Include implementation details.  */
#define DMGL_TYPES       (1 << 4)       /* Also try to demangle type encodings.  */
#define DMGL_RET_POSTFIX (1 << 5)       /* Print function return types (when present) after function signature */

#define DMGL_AUTO        (1 << 8)
#define DMGL_GNU         (1 << 9)
#define DMGL_LUCID       (1 << 10)
#define DMGL_ARM         (1 << 11)
#define DMGL_HP          (1 << 12)
#define DMGL_EDG         (1 << 13)
#define DMGL_GNU_V3      (1 << 14)
#define DMGL_GNAT        (1 << 15)

trap::BFDFrontend * trap::BFDFrontend::curInstance = NULL;

trap::BFDFrontend & trap::BFDFrontend::getInstance(std::string fileName){
    if(BFDFrontend::curInstance == NULL){
        if(fileName != "")
            BFDFrontend::curInstance = new BFDFrontend(fileName);
        else
            THROW_ERROR("An instance of BFDFrontend does not exists yet, so the file name of the binary image must be specified");
    }
    return *BFDFrontend::curInstance;
}

trap::BFDFrontend::BFDFrontend(std::string binaryName){
    char ** matching = NULL;
    this->sy = NULL;

    bfd_init();
    this->execImage = bfd_openr(binaryName.c_str(), "default");
    if(this->execImage == NULL){
        THROW_ERROR("Error in reading input file " << binaryName << " --> " << bfd_errmsg(bfd_get_error()));
    }
    if (bfd_check_format (this->execImage, bfd_archive)){
        THROW_ERROR("Error in reading input file " << binaryName << " --> The input file is an archive; executable file required");
    }
    if (!bfd_check_format_matches (this->execImage, bfd_object, &matching)){
        THROW_ERROR("Error in reading input file " << binaryName << " --> The input file is not an object file or the target is ambiguous -- " << this->getMatchingFormats(matching));
    }

    this->wordsize = bfd_get_arch_size(this->execImage)/(8*bfd_octets_per_byte(this->execImage));

    //Now I read the different sections and save them in a temporary vector
    struct bfd_section *p = NULL;
    bfd_vma gblStartAddr = (bfd_vma)-1;
    bfd_size_type gblEndAddr = 0;
    for (p = this->execImage->sections; p != NULL; p = p->next){
        flagword flags = bfd_get_section_flags(this->execImage, p);
        if((flags & SEC_ALLOC) != 0 && (flags & SEC_DEBUGGING) == 0 && (flags & SEC_THREAD_LOCAL) == 0){
            bfd_size_type datasize = bfd_section_size(this->execImage, p);
            bfd_vma vma = bfd_get_section_vma(this->execImage, p);
/*            #ifndef NDEBUG
            std::cerr << "Section " << p->name << " Start Address " << std::hex << vma << " Size " << std::hex << datasize << " End Address " << std::hex << datasize + vma << std::dec << std::endl;
            #endif*/
            if((datasize + vma) > gblEndAddr)
                gblEndAddr = datasize + vma;
            if(gblStartAddr > vma || gblStartAddr == (bfd_vma)-1)
                gblStartAddr = vma;
             if((flags & SEC_HAS_CONTENTS) != 0){
                Section sec;
                sec.datasize = datasize;
                sec.startAddr = vma;
                sec.data = new bfd_byte[sec.datasize];
                sec.descriptor = p;
                sec.name = p->name;
                bfd_get_section_contents (this->execImage, p, sec.data, 0, sec.datasize);
                this->secList.push_back(sec);
            }
        }
    }
    this->codeSize.first = gblEndAddr;
    this->codeSize.second = gblStartAddr;
    this->execName = bfd_get_filename(this->execImage);

    if(!(bfd_get_file_flags (this->execImage) & HAS_SYMS)){
        THROW_ERROR("There are no symbols in file " << bfd_get_filename(this->execImage));
    }
    int storage = bfd_get_symtab_upper_bound(this->execImage);
    if (storage < 0){
        THROW_ERROR("Error in getting symbol table upper bound -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }
    if(storage != 0)
        this->sy = (asymbol **)malloc (storage);
    if (this->sy == NULL){
        THROW_ERROR("Error in allocating space for symbol storage -- " << bfd_get_filename(this->execImage));
    }
    long symcount = 0;
    symcount = bfd_canonicalize_symtab (this->execImage, this->sy);
    if (symcount < 0){
        THROW_ERROR("Error in getting symbol count -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }

    //Now I call the various functions which extract all the necessary information form the BFD
    this->readSyms();

    //Finally I deallocate part of the memory
    std::vector<Section>::iterator sectionsIter, sectionsEnd;
    for(sectionsIter = this->secList.begin(), sectionsEnd = this->secList.end(); sectionsIter != sectionsEnd; sectionsIter++){
        delete [] sectionsIter->data;
    }
    this->secList.clear();
    free(this->sy);

    if(this->execImage != NULL){
        if(!bfd_close_all_done(this->execImage)){
            //An Error has occurred; lets see what it is
            THROW_ERROR("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
        this->execImage = NULL;
    }
}

trap::BFDFrontend::~BFDFrontend(){
    if(this->execImage != NULL){
        if(!bfd_close_all_done(this->execImage)){
            //An Error has occurred; lets see what it is
            THROW_ERROR("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
        this->execImage = NULL;
    }
}

///It returns all the symbols that match the given regular expression
// std::map<std::string,  unsigned int> BFDFrontend::findFunction(boost::regex &regEx){
//     std::map<std::string,  unsigned int> foundSyms;
//     std::map<std::string, unsigned int>::iterator addrMap, addrMapEnd;
//     for(addrMap = this->symToAddr.begin(), addrMapEnd = this->symToAddr.end(); addrMap != addrMapEnd; addrMap++){
//         if(boost::regex_match(addrMap->first, regEx))
//             foundSyms.insert(*addrMap);
//     }
//     return foundSyms;
// }

///Given an address, it returns the symbol found there,
///"" if no symbol is found at the specified address; note
///That if address is in the middle of a function, the symbol
///returned refers to the function itself
std::list<std::string> trap::BFDFrontend::symbolAt(unsigned int address){
    std::map<unsigned int, std::list<std::string> >::iterator symMap1 = this->addrToSym.find(address);
    if(symMap1 == this->addrToSym.end()){
        std::map<unsigned int, std::string>::iterator symMap2 = this->addrToFunction.find(address);
        std::list<std::string> emptyList;
        if(symMap2 != this->addrToFunction.end())
            emptyList.push_back(symMap2->second);
        return emptyList;
    }

    return symMap1->second;
}

///Given the name of a symbol it returns its value
///(which usually is its address);
///valid is set to false if no symbol with the specified
///name is found
unsigned int trap::BFDFrontend::getSymAddr(std::string symbol, bool &valid){
    std::map<std::string, unsigned int>::iterator addrMap = this->symToAddr.find(symbol);
    if(addrMap == this->symToAddr.end()){
        valid = false;
        return 0;
    }
    else{
        valid = true;
        return addrMap->second;
    }
}

///Accesses the BFD internal structures in order to get the dissassbly of the symbols
void trap::BFDFrontend::readSyms(){
    //make sure there are symbols in the file
    if ((bfd_get_file_flags (execImage) & HAS_SYMS) == 0)
        return;

    long symcount = 0;
    unsigned int size = 0;
    void *minisyms = NULL;
    char *name = NULL;
    symcount = bfd_read_minisymbols(this->execImage, 0, &minisyms, &size);
    asymbol *store = NULL;
    bfd_byte *from = NULL, *fromend = NULL;
    store = bfd_make_empty_symbol(this->execImage);
    if(store == NULL){
        THROW_ERROR("Error in allocating space for symbols -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }
    from = (bfd_byte *) minisyms;
    fromend = from + symcount * size;
    for (; from < fromend; from += size){
        asymbol *sym = NULL;
        symbol_info syminfo;

        sym = bfd_minisymbol_to_symbol (this->execImage, 0, from, store);
        if (sym == NULL){
            THROW_ERROR("Error in while getting symbol from file -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
        }
        bfd_get_symbol_info (this->execImage, sym, &syminfo);

        if((sym->flags & BSF_DEBUGGING) || bfd_is_target_special_symbol(this->execImage, sym) ||
                    (char)syminfo.type == 'b' || (char)syminfo.type == 'r' || (char)syminfo.type == 'a' || bfd_is_undefined_symclass (syminfo.type)){
            continue;
        }

        name = (char *)syminfo.name;
        if(name[0] == '$')
            continue;

        this->addrToSym[syminfo.value].push_back(name);
        this->symToAddr[name] = syminfo.value;
    }
}

///Returns the name of the executable file
std::string trap::BFDFrontend::getExecName(){
    return this->execName;
}

///Returns the end address of the loadable code
unsigned int trap::BFDFrontend::getBinaryEnd(){
    return (this->codeSize.first + this->wordsize);
}


std::string trap::BFDFrontend::getMatchingFormats (char **p){
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
