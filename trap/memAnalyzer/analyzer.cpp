#include <ctype.h>
#include <cstring>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

#include <boost/filesystem/operations.hpp>
#include <boost/filesystem/fstream.hpp>
#include <boost/filesystem/convenience.hpp>
#include <boost/filesystem/path.hpp>

#include <boost/lexical_cast.hpp>

#include "utils.hpp"

#include "memAccessType.hpp"
#include "analyzer.hpp"

///Given an array of chars (either in hex or decimal form) if converts it to the
///corresponding integer representation
unsigned int MemAnalyzer::toIntNum(const std::string &numStr){
    if(numStr.size() > 2 && numStr[0] == '0' && tolower(numStr[1]) == 'x'){
        int result;
        std::stringstream converter(numStr);
        converter >> std::hex >> result;
        return result;
    }
    else{
        //It still might be the string does not start with 0x but it is still a hex number;
        //I also have to check that it is a valid string
        bool ishex = false;
        for(unsigned int i = 0; i < numStr.size(); i++){
            if(tolower(numStr[i]) >= 'a' && tolower(numStr[i]) <= 'f'){
                ishex = true;
            }else if (tolower(numStr[i]) > 'f' || (tolower(numStr[i]) < 'a' && tolower(numStr[i]) > '9')  || tolower(numStr[i]) < '0'){
                THROW_EXCEPTION(numStr << " is not a valid number");
            }
        }
        if(ishex){
            int result;
            std::stringstream converter(numStr);
            converter >> std::hex >> result;
            return result;
        }
        else
            return boost::lexical_cast<int>(numStr);
    }
    return 0;
}

MemAnalyzer::MemAnalyzer(std::string fileName, std::string memSize){
    this->memSize = this->toIntNum(memSize);
    boost::filesystem::path memDumpPath = boost::filesystem::system_complete(boost::filesystem::path(fileName, boost::filesystem::native));
    if ( !boost::filesystem::exists( memDumpPath ) ){
        THROW_EXCEPTION("Path " << fileName << " specified for the memory dump does not exists");
    }
    else{
        this->dumpFile.open(fileName.c_str(), std::ifstream::in | std::ifstream::binary);
        if(!this->dumpFile.good())
            THROW_EXCEPTION("Error in opening file " << fileName);
    }
}

MemAnalyzer::~MemAnalyzer(){
    if(this->dumpFile.is_open()){
        this->dumpFile.close();
    }
}

///Creates the image of the memory as it was at cycle procCycle
void MemAnalyzer::createMemImage(boost::filesystem::path &outFile, double simTime){
    char * tempMemImage = new char[this->memSize];
    MemAccessType readVal;
    unsigned int maxAddress = 0;

    ::bzero(tempMemImage, this->memSize);

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.simulationTime > simTime && simTime > 0) //I've reached the desired cycle
                break;
            if(readVal.address < this->memSize){
                tempMemImage[readVal.address] = readVal.val;
                if(readVal.address > maxAddress)
                    maxAddress = readVal.address;
            }
        }
    }
    this->dumpFile.seekg(std::ifstream::beg);

    //Now I print on the output file the memory image
    std::ofstream memImageFile(outFile.native_file_string().c_str());
    for(int i = 0; i < maxAddress; i+=sizeof(int)){
        memImageFile << "MEM[" << std::hex << std::showbase << i << "] = " << ((int *)tempMemImage)[i/sizeof(int)] << std::endl;
    }
    memImageFile.close();
    delete [] tempMemImage;
}

///Returns the first memory access that modifies the address addr after
///procCycle
MemAccessType MemAnalyzer::getFirstModAfter(std::string addr, double simTime){
    MemAccessType readVal;
    unsigned int address = this->toIntNum(addr);

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.simulationTime >= simTime && readVal.address == address){
                this->dumpFile.seekg(std::ifstream::beg);
                return readVal;
            }
        }
    }

    THROW_EXCEPTION("No modifications performed to address " << std::hex << std::showbase << address);

    return readVal;
}

///Returns the last memory access that modified addr
MemAccessType MemAnalyzer::getLastMod(std::string addr){
    MemAccessType readVal;
    MemAccessType foundVal;
    bool found = false;
    unsigned int address = this->toIntNum(addr);

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.address == address){
                foundVal = readVal;
                found = true;
            }
        }
    }

    if(!found)
        THROW_EXCEPTION("No modifications performed to address " << std::hex << std::showbase << address);

    this->dumpFile.seekg(std::ifstream::beg);
    return foundVal;
}

///Prints all the modifications done to address addr
void MemAnalyzer::getAllModifications(std::string addr, boost::filesystem::path &outFile, double initSimTime, double endSimTime){
    MemAccessType readVal;
    unsigned int address = this->toIntNum(addr);
    std::ofstream memImageFile(outFile.native_file_string().c_str());

    while(this->dumpFile.good()){
        this->dumpFile.read((char *)&readVal, sizeof(MemAccessType));
        if(this->dumpFile.good()){
            if(readVal.address == address && readVal.simulationTime >= initSimTime && (endSimTime < 0 || readVal.simulationTime <= endSimTime)){
                memImageFile << "MEM[" << std::hex << std::showbase << readVal.address << "] = " << readVal.val << " time " << std::dec << readVal.simulationTime << " program counter " << std::hex << std::showbase << readVal.programCounter << std::endl;
            }
        }
    }

    memImageFile.close();
    this->dumpFile.seekg(std::ifstream::beg);
}
