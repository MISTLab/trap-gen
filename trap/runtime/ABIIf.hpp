#ifndef ABIIF_HPP
#define ABIIF_HPP

template<class regWidth> class ABIIf{
    public:
    bool isLittleEndian() = 0;
    regWidth readLR() = 0;
    void setLR( const regWidth & newValue ) = 0;
    regWidth readPC() = 0;
    void setPC( const regWidth & newValue ) = 0;
    regWidth readSP() = 0;
    void setSP( const regWidth & newValue ) = 0;
    regWidth readFP() = 0;
    void setFP( const regWidth & newValue ) = 0;
    regWidth readRetVal() = 0;
    void setRetVal( const regWidth & newValue ) = 0;
    std::vector< regWidth > readArgs() = 0;
    void setArgs( const std::vector< regWidth > & args ) = 0;
    regWidth readGDBReg( const unsigned int & gdbId ) = 0;
    void setGDBReg( const regWidth & newValue, const unsigned int & gdbId ) = 0;
    regWidth readMem( const regWidth & address ) = 0;
    void writeMem( const regWidth & address, const regWidth & datum ) = 0;
    void writeMem( const regWidth & address, const regWidth & datum ) = 0;
};

#endif
