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
#include <dis-asm.h>
}

#include <sys/types.h>
#include <cstdio>
#include <stdarg.h>

#include <map>
#include <string>
#include <vector>
#include <list>
#include <iostream>

#include "utils.hpp"

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

BFDFrontend::BFDFrontend(std::string binaryName, bool readSrc){
    char ** matching = NULL;
    this->sy = NULL;

    bfd_init();
    this->execImage = bfd_openr(binaryName.c_str(), "default");
    if(execImage == NULL){
        THROW_EXCEPTION("Error in reading input file " << binaryName << " --> " << bfd_errmsg(bfd_get_error()));
    }
    if (bfd_check_format (execImage, bfd_archive)){
        THROW_EXCEPTION("Error in reading input file " << binaryName << " --> The input file is an archive; executable file required");
    }
    if (!bfd_check_format_matches (execImage, bfd_object, &matching)){
        THROW_EXCEPTION("Error in reading input file " << binaryName << " --> The input file is not an object file or the target is ambiguous -- " << this->getMatchingFormats(matching));
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
            #ifndef NDEBUG
            std::cerr << "Section " << p->name << " Start Address " << std::hex << vma << " Size " << std::hex << datasize << " End Address " << std::hex << datasize + vma << std::dec << std::endl;
            #endif
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
        THROW_EXCEPTION("There are no symbols in file " << bfd_get_filename(this->execImage));
    }
    int storage = bfd_get_symtab_upper_bound(this->execImage);
    if (storage < 0){
        THROW_EXCEPTION("Error in getting symbol table upper bound -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }
    if(storage != 0)
        this->sy = (asymbol **)malloc (storage);
    if (this->sy == NULL){
        THROW_EXCEPTION("Error in allocating space for symbol storage -- " << bfd_get_filename(this->execImage));
    }
    long symcount = 0;
    symcount = bfd_canonicalize_symtab (this->execImage, this->sy);
    if (symcount < 0){
        THROW_EXCEPTION("Error in getting symbol count -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }

    //Now I call the various functions which extract all the necessary information form the BFD
    this->readDisass();
    this->readSyms();
    if(readSrc)
        this->readSrc();

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
            THROW_EXCEPTION("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
        this->execImage = NULL;
    }
}

BFDFrontend::~BFDFrontend(){
    if(this->execImage != NULL){
        if(!bfd_close_all_done(this->execImage)){
            //An Error has occurred; lets see what it is
            THROW_EXCEPTION("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
        this->execImage = NULL;
    }
}

///It returns all the symbols that match the given regular expression
std::map<std::string,  unsigned int> BFDFrontend::findFunction(boost::regex &regEx){
    std::map<std::string,  unsigned int> foundSyms;
    std::map<std::string, unsigned int>::iterator addrMap, addrMapEnd;
    for(addrMap = this->symToAddr.begin(), addrMapEnd = this->symToAddr.end(); addrMap != addrMapEnd; addrMap++){
        if(boost::regex_match(addrMap->first, regEx))
            foundSyms.insert(*addrMap);
    }
    return foundSyms;
}

///Given an address, it returns the symbol found there,
///"" if no symbol is found at the specified address; note
///That if address is in the middle of a function, the symbol
///returned refers to the function itself
std::list<std::string> BFDFrontend::symbolAt(unsigned int address){
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
unsigned int BFDFrontend::getSymAddr(std::string symbol, bool &valid){
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

///Given an address, it sets fileName to the name of the source file
///which contains the code and line to the line in that file. Returns
///false if the address is not valid
bool BFDFrontend::getSrcFile(unsigned int address, std::string &fileName, unsigned int &line){
    std::map<unsigned int, std::pair<std::string, unsigned int> >::iterator srcMap = this->addrToSrc.find(address);
    if(srcMap == this->addrToSrc.end()){
        return false;
    }
    else{
        fileName = srcMap->second.first;
        line = srcMap->second.second;
        return true;
    }
}

///Given an address it returns the assembly code at that
///address, "" if there is none or address is not valid
std::string BFDFrontend::getAssembly(unsigned int address){
    std::map<unsigned int, std::string>::iterator assMap = this->addrToAssembly.find(address);
    if(assMap == this->addrToAssembly.end())
        return "";
    else
        return assMap->second;
}


void BFDFrontend::sprintf_wrapper(char *str, const char *format, ...) {
    va_list ap;
    va_start(ap, format);
    vsprintf(str+strlen(str),format, ap);
    va_end(ap);
}

///Accesses the BFD internal structures in order to get the dissassbly of the instructions
void BFDFrontend::readDisass(){
    char myMemStream[100];
    myMemStream[0] = '\0';

    disassembler_ftype disassFun = disassembler(this->execImage);
    if(!disassFun){
        THROW_EXCEPTION("Error in initializing the disassembler for " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }

    disassemble_info disasm_info;
    init_disassemble_info(&disasm_info, myMemStream, (fprintf_ftype) BFDFrontend::sprintf_wrapper);

    disasm_info.flavour = bfd_get_flavour(this->execImage);
    disasm_info.arch = bfd_get_arch(this->execImage);
    disasm_info.mach = bfd_get_mach(this->execImage);
    disasm_info.disassembler_options = (char *)"";
    disasm_info.octets_per_byte = bfd_octets_per_byte(this->execImage);
    disasm_info.skip_zeroes = 8;
    disasm_info.skip_zeroes_at_end = 3;
    disasm_info.disassembler_needs_relocs = FALSE;
    if (bfd_big_endian(this->execImage))
        disasm_info.display_endian = disasm_info.endian = BFD_ENDIAN_BIG;
    else if (bfd_little_endian(this->execImage))
        disasm_info.display_endian = disasm_info.endian = BFD_ENDIAN_LITTLE;
    else
        disasm_info.endian = BFD_ENDIAN_UNKNOWN;

    disassemble_init_for_target(&disasm_info);

    disasm_info.symbols = NULL;
    disasm_info.num_symbols = 0;
    disasm_info.symtab_pos = -1;

    //Finally I can iterate all over the sections and get the disassembly of each instruction
    std::vector<Section>::iterator sectionsIter, sectionsEnd;
    for(sectionsIter = this->secList.begin(), sectionsEnd = this->secList.end(); sectionsIter != sectionsEnd; sectionsIter++){
        disasm_info.buffer = sectionsIter->data;
        disasm_info.buffer_vma = sectionsIter->startAddr;
        disasm_info.buffer_length = sectionsIter->datasize;
        disasm_info.section = sectionsIter->descriptor;
        for(bfd_vma i = 0; i < sectionsIter->datasize; i += this->wordsize){
            (*disassFun)(i + sectionsIter->startAddr, &disasm_info);
            this->addrToAssembly[i + sectionsIter->startAddr] = myMemStream;
            myMemStream[0] = '\0';
        }
    }
}

///Accesses the BFD internal structures in order to get correspondence among machine code and
///the source code
void BFDFrontend::readSrc(){
    std::vector<Section>::iterator sectionsIter, sectionsEnd;
    for(sectionsIter = this->secList.begin(), sectionsEnd = this->secList.end(); sectionsIter != sectionsEnd; sectionsIter++){
        for(bfd_vma i = 0; i < sectionsIter->datasize; i += this->wordsize){
            const char *filename = NULL;
            const char *functionname = NULL;
            unsigned int line = 0;

            if(!bfd_find_nearest_line (this->execImage, sectionsIter->descriptor, this->sy, i + sectionsIter->startAddr, &filename,
                        &functionname, &line))
                continue;

            if (filename != NULL && *filename == '\0')
                filename = NULL;
            if (functionname != NULL && *functionname == '\0')
                functionname = NULL;

            if (functionname != NULL && this->addrToFunction.find(i + sectionsIter->startAddr) == this->addrToFunction.end()){
                char *name = bfd_demangle (this->execImage, functionname, DMGL_ANSI | DMGL_PARAMS);
                if(name == NULL)
                    name = (char *)functionname;
                this->addrToFunction[i + sectionsIter->startAddr] = name;
            }
            if (line > 0 && this->addrToSrc.find(i + sectionsIter->startAddr) == this->addrToSrc.end())
                this->addrToSrc[i + sectionsIter->startAddr] = std::pair<std::string, unsigned int>(filename == NULL ? "???" : filename, line);
        }
    }
}

///Accesses the BFD internal structures in order to get the dissassbly of the symbols
void BFDFrontend::readSyms(){
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
        THROW_EXCEPTION("Error in allocating space for symbols -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
    }
    from = (bfd_byte *) minisyms;
    fromend = from + symcount * size;
    for (; from < fromend; from += size){
        asymbol *sym = NULL;
        symbol_info syminfo;

        sym = bfd_minisymbol_to_symbol (this->execImage, 0, from, store);
        if (sym == NULL){
            THROW_EXCEPTION("Error in while getting symbol from file -- " << bfd_get_filename(this->execImage) << " --> " << bfd_errmsg(bfd_get_error()));
        }
        bfd_get_symbol_info (this->execImage, sym, &syminfo);

        if((sym->flags & BSF_DEBUGGING) || bfd_is_target_special_symbol(this->execImage, sym) ||
                    (char)syminfo.type == 'b' || (char)syminfo.type == 'r' || (char)syminfo.type == 'a' || bfd_is_undefined_symclass (syminfo.type)){
            continue;
        }

        name = bfd_demangle (this->execImage, syminfo.name, DMGL_ANSI | DMGL_PARAMS);
        if(name == NULL)
            name = (char *)syminfo.name;
        if(name[0] == '$')
            continue;

        this->addrToSym[syminfo.value].push_back(name);
        this->symToAddr[name] = syminfo.value;

        const char *filename = NULL;
        unsigned int line = 0;

        if(!bfd_find_line (this->execImage, this->sy, sym, &filename, &line))
            continue;
        if (line > 0)
            this->addrToSrc[syminfo.value] = std::pair<std::string, unsigned int>(filename == NULL ? "???" : filename, line);
    }
}

///Returns the name of the executable file
std::string BFDFrontend::getExecName(){
    return this->execName;
}

///Returns the end address of the loadable code
unsigned int BFDFrontend::getBinaryEnd(){
    return (this->codeSize.first + this->wordsize);
}


std::string BFDFrontend::getMatchingFormats (char **p){
    std::string match = "";
    while (*p){
        match += *p;
        *p++;
        match += " ";
    }
    return match;
}
