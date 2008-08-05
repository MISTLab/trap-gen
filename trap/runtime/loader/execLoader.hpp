#ifndef EXECLOADER_HPP
#define EXECLOADER_HPP

#include <string>

extern "C" {
#include <bfd.h>
}

namespace resp{

class ExecLoader{
  private:
    bfd * execImage;
    unsigned char * programData;
    unsigned long progDim;
    unsigned long dataStart;
    
    ///examines the bfd in order to find the sections containing data
    ///to be loaded; at the same time it fills the programData
    ///array
    void loadProgramData();
  public:
    ///Initializes the loader of executable files by creating
    ///the corresponding bfd image of the executable file
    ///specified as parameter
    ExecLoader(std::string fileName);
    ~ExecLoader();
    ///Returns the entry point of the loaded program
    unsigned long getProgStart();
    ///Returns the start address of the data to load
    unsigned long getDataStart();
    ///Returns the dimensione of the loaded program
    unsigned long getProgDim();
    ///Returns a pointer to the array contianing the program data
    unsigned long getProgData();
};

}

#endif
