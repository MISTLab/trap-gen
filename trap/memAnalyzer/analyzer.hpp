#ifndef ANALYZER_HPP
#define ANALYZER_HPP

#include <iostream>
#include <fstream>
#include <string>

#include <boost/filesystem/path.hpp>

struct MemAccessType;

class MemAnalyzer{
    private:
    std::ifstream dumpFile;
    unsigned int memSize;

    ///Given an array of chars (either in hex or decimal form) if converts it to the
    ///corresponding integer representation
    int toIntNum(const std::string &numStr);

    public:
    MemAnalyzer(std::string fileName, unsigned int memSize);
    ~MemAnalyzer();
    ///Creates the image of the memory as it was at cycle procCycle
    void createMemImage(boost::filesystem::path &outFile, double simTime = -1);
    ///Returns the first memory access that modifies the address addr after
    ///procCycle
    MemAccessType getFirstModAfter(unsigned int addr, double simTime = 0);
    ///Returns the last memory access that modified addr
    MemAccessType getLastMod(unsigned int addr);
    ///Prints all the modifications done to address addr
    void getAllModifications(unsigned int addr, double initSimTime, double endSimTime, boost::filesystem::path &outFile);
};

#endif
