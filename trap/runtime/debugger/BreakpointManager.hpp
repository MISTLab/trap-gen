#ifndef BREAKPOINTMANAGER_HPP
#define BREAKPOINTMANAGER_HPP

#include <iostream>
#include <vector>
#include <map>
#include <string>

namespace resp{

template <class AddressType> struct Breakpoint{
   enum Type{MEM=0, HW, WRITE, READ, ACCESS};
   AddressType address;
   unsigned int length;
   Type type;
};

template <class AddressType> class BreakpointManager{
  private:
   std::map<AddressType, Breakpoint<AddressType> > breakpoints;
  public:
   //Eliminates all the breakpoints
   void clearAllBreaks(){
      this->breakpoints.clear();
   }
   bool addBreakpoint(typename Breakpoint<AddressType>::Type type, AddressType address, unsigned int length){
      #ifndef NDEBUG
      std::cerr << "GDB-break " << __PRETTY_FUNCTION__ << ": Adding Breakpoint at address " << address << std::endl;
      #endif
      if(this->breakpoints.find(address) != this->breakpoints.end())
         return false;
      this->breakpoints[address].address = address;
      this->breakpoints[address].length = length;
      this->breakpoints[address].type = type;
      return true;
   }
   
   bool removeBreakpoint(AddressType address){
      #ifndef NDEBUG
      std::cerr << "GDB-break " << __PRETTY_FUNCTION__ << ": Removing Breakpoint at address " << address << std::endl;
      #endif      
      if(this->breakpoints.find(address) == this->breakpoints.end())
         return false;
      this->breakpoints.erase(address);
      return true;
   }
   
   bool hasBreakpoint(AddressType address){
      return this->breakpoints.find(address) != this->breakpoints.end();
   }
   
   Breakpoint<AddressType> * getBreakPoint(AddressType address){
      if(this->breakpoints.find(address) == this->breakpoints.end())
         return NULL;
      else
         return &(this->breakpoints[address]);
   }
   
   std::map<AddressType, Breakpoint<AddressType> > & getBreakpoints(){
        return this->breakpoints;
   }
};

}

#endif
