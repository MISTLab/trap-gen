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
    unsigned int toIntNum(const std::string &numStr);

    public:
    MemAnalyzer(std::string fileName, std::string memSize);
    ~MemAnalyzer();
    ///Creates the image of the memory as it was at cycle procCycle
    void createMemImage(boost::filesystem::path &outFile, double simTime = -1);
    ///Returns the first memory access that modifies the address addr after
    ///procCycle
    MemAccessType getFirstModAfter(std::string addr, double simTime = 0);
    ///Returns the last memory access that modified addr
    MemAccessType getLastMod(std::string addr);
    ///Prints all the modifications done to address addr
    void getAllModifications(std::string addr, boost::filesystem::path &outFile, double initSimTime = 0, double endSimTime = -1);
};

#endif
