#include <string>
#include <map>
#include <iostream>

#include "utils.hpp"

extern "C" {
#include <bfd.h>
}

#include "execLoader.hpp"

using namespace resp;

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
        THROW_EXCEPTION("Error in reading input file " << fileName << " --> " << bfd_errmsg(bfd_get_error()));
    }
    if (bfd_check_format (this->execImage, bfd_archive)){
        THROW_EXCEPTION("Error in reading input file " << fileName << " --> The input file is an archive; executable file required");
    }
    if (!bfd_check_format_matches (this->execImage, bfd_object, &matching)){
        THROW_EXCEPTION("Error in reading input file " << fileName << " --> The input file is not an object file");
    }
    this->loadProgramData();
}

ExecLoader::~ExecLoader(){
    if(this->execImage != NULL){
        if(!bfd_close_all_done(this->execImage)){
            //An Error has occurred; lets see what it is
            THROW_EXCEPTION("Error in closing the binary parser --> " << bfd_errmsg(bfd_get_error()));
        }
    }
    if(this->programData != NULL){
        delete [] this->programData;
    }
}

unsigned long ExecLoader::getProgStart(){
    #ifndef NDEBUG
    if(this->execImage == NULL){
        THROW_EXCEPTION("The binary parser not yet correcly created");
    }
    #endif
    return bfd_get_start_address(this->execImage);
}

unsigned long ExecLoader::getProgDim(){
    #ifndef NDEBUG
    if(this->execImage == NULL){
        THROW_EXCEPTION("The binary parser not yet correcly created");
    }
    #endif
    return this->progDim;
}

unsigned long ExecLoader::getProgData(){
    #ifndef NDEBUG
    if(this->execImage == NULL){
        THROW_EXCEPTION("The binary parser not yet correcly created");
    }
    #endif
    #ifndef NDEBUG
    if(this->programData == NULL){
        THROW_EXCEPTION("The program data was not correcly computed");
    }
    #endif
    return (unsigned long)this->programData;
}

unsigned long ExecLoader::getDataStart(){
    #ifndef NDEBUG
    if(this->execImage == NULL){
        THROW_EXCEPTION("The binary parser not yet correcly created");
    }
    #endif
    return this->dataStart;
}

void ExecLoader::loadProgramData(){
    bfd_section *p = NULL;
    std::map<unsigned long, unsigned char> memMap;
    #ifdef LITTLE_ENDIAN_BO
    bool swapEndianess = bfd_header_big_endian(this->execImage);
    #else
    #ifdef BIG_ENDIAN_BO
    bool swapEndianess = bfd_header_little_endian(this->execImage);
    #else
    bool swapEndianess = false;
    #endif
    #endif
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
                #ifndef NDEBUG
                std::cerr << "Loading data fom section " << p->name << " Start Address " << std::showbase << std::hex << vma << " Size " << std::hex << datasize << " End Address " << std::hex << datasize + vma << std::dec << std::endl;
                #endif
                bfd_byte *data = new bfd_byte[datasize];
                bfd_get_section_contents (this->execImage, p, data, 0, datasize);
                for(unsigned int i = 0; i < datasize; i += 4){
                    if(swapEndianess){
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i, data[i + 3]));
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i + 1, data[i + 2]));
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i + 2, data[i + 1]));
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i + 3, data[i ]));
                    }
                    else{
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i, data[i]));
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i + 1, data[i + 1]));
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i + 2, data[i + 2]));
                         curMapPos = memMap.insert(curMapPos, std::pair<unsigned long, unsigned char>(vma + i + 3, data[i  + 3]));
                    }
                }
                delete [] data;
            }
            else{
                #ifndef NDEBUG
                std::cerr << "Filling with 0s section " << p->name << " Start Address " << std::showbase << std::hex << vma << " Size " << std::hex << datasize << " End Address " << std::hex << datasize + vma << std::dec << std::endl;
                #endif
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
