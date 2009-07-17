#ifndef MEMACCESSTYPE_HPP
#define MEMACCESSTYPE_HPP

namespace trap{

struct MemAccessType{
    double simulationTime;
    unsigned int programCounter;
    unsigned int address;
    char val;
};

}

#endif
