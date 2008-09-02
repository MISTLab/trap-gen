#ifndef ABIIF_HPP
#define ABIIF_HPP

#include <vector>

template<class regWidth> class ABIIf{
    public:
    virtual bool isLittleEndian() = 0;
    virtual regWidth readLR() = 0;
    virtual void setLR( const regWidth & newValue ) = 0;
    virtual regWidth readPC() = 0;
    virtual void setPC( const regWidth & newValue ) = 0;
    virtual regWidth readSP() = 0;
    virtual void setSP( const regWidth & newValue ) = 0;
    virtual regWidth readFP() = 0;
    virtual void setFP( const regWidth & newValue ) = 0;
    virtual regWidth readRetVal() = 0;
    virtual void setRetVal( const regWidth & newValue ) = 0;
    virtual std::vector< regWidth > readArgs() = 0;
    virtual void setArgs( const std::vector< regWidth > & args ) = 0;
    virtual regWidth readGDBReg( const unsigned int & gdbId ) = 0;
    virtual void setGDBReg( const regWidth & newValue, const unsigned int & gdbId ) = 0;
    virtual regWidth readMem( const regWidth & address ) = 0;
    virtual void writeMem( const regWidth & address, const regWidth & datum ) = 0;
    virtual void writeMem( const regWidth & address, const unsigned char & datum ) = 0;
};

#endif
