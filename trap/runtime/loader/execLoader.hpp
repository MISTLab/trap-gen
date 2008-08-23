#ifndef EXECLOADER_HPP
#define EXECLOADER_HPP

#include <string>

extern "C" {
#include <bfd.h>
}

class ExecLoader{
  private:
    bfd * execImage;
    unsigned char * programData;
    unsigned int progDim;
    unsigned int dataStart;
    bool keepEndianess;
    
    ///examines the bfd in order to find the sections containing data
    ///to be loaded; at the same time it fills the programData
    ///array
    void loadProgramData();
  public:
    ///Initializes the loader of executable files by creating
    ///the corresponding bfd image of the executable file
    ///specified as parameter
    ExecLoader(std::string fileName, bool keepEndianess = true);
    ~ExecLoader();
    ///Returns the entry point of the loaded program
    unsigned int getProgStart();
    ///Returns the start address of the data to load
    unsigned int getDataStart();
    ///Returns the dimensione of the loaded program
    unsigned int getProgDim();
    ///Returns a pointer to the array contianing the program data
    unsigned char * getProgData();
};

#endif
