#include <iostream>
#include <string>
#include <ostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <boost/thread/thread.hpp>
#include <boost/thread/condition.hpp>
#include <boost/thread/mutex.hpp>
#include <map>

#include "utils.hpp"

#include "Interval.hpp"

using namespace resp;

namespace resp{
unsigned int maxIntervalId = 0;
std::set<Interval *> intervals;
Interval * nullInterval = (Interval *)NULL;
boost::mutex interval_mutex;
}

Interval::Interval() : lowerBound(0),  upperBound(0),  id(0){}

Interval::Interval(unsigned int lowerBound,  unsigned int upperBound) : lowerBound(lowerBound),  upperBound(upperBound){
    id = maxIntervalId;
    #ifndef NDEBUG
    std::set<Interval *>::iterator intIter,  intIterEnd;
    for(intIter = intervals.begin(),  intIterEnd = intervals.end(); intIter != intIterEnd; intIter++){
        if((*intIter)->lowerBound < lowerBound && (*intIter)->upperBound > upperBound)
            THROW_EXCEPTION("Creating a colliding interval");
        if((*intIter)->lowerBound > lowerBound && (*intIter)->upperBound < upperBound)
            THROW_EXCEPTION("Creating a colliding interval");
        if((*intIter)->lowerBound > lowerBound && (*intIter)->lowerBound < upperBound)
            THROW_EXCEPTION("Creating a colliding interval");
        if((*intIter)->upperBound > lowerBound && (*intIter)->upperBound < upperBound)
            THROW_EXCEPTION("Creating a colliding interval");
    }
    #endif
    intervals.insert(this);
    maxIntervalId++;
}

bool Interval::isIn(unsigned int toFind) const{
    return (toFind >= lowerBound && toFind <= upperBound);
}

bool Interval::operator() (const Interval& a, const Interval& b) const{
    return a.lowerBound < b.lowerBound;
}

std::string Interval::dump() const{
    std::ostringstream stream;
    stream << this->id << "," << this->lowerBound << "," << this->upperBound << std::endl;
    return stream.str();
}

unsigned int Interval::getId() const{
    return this->id;
}

std::string Interval::dumpIntervals(){
    //boost::mutex::scoped_lock lock(interval_mutex);
    std::ostringstream stream;
    stream << "Thread Id" << "," << "Stack Lower Bound" << "," << "Stack Upper Bound" << std::endl;
    std::set<Interval *>::iterator interIter,  interInterEnd;
    for(interIter = intervals.begin(),  interInterEnd = intervals.end(); interIter !=  interInterEnd; interIter++){
        stream << (*interIter)->dump() << std::endl;
    }
    return stream.str();
}

unsigned int Interval::getCenter() const{
    return (this->lowerBound + this->upperBound)/2;
}

void Interval::update(unsigned int newAddr){
    if(newAddr < this->lowerBound)
        this->lowerBound = newAddr;
    else if(newAddr > this->upperBound)
        this->upperBound = newAddr;
}

std::pair<Interval *,  bool> Interval::getInterval(unsigned int value,  unsigned int limit){
    //boost::mutex::scoped_lock lock(interval_mutex);
    //Here I have to determine if an interval exists for value: in case I
    //return it. Otherwise I create a new one and return it
    std::set<Interval *>::iterator interIter,  interInterEnd;
    for(interIter = intervals.begin(),  interInterEnd = intervals.end(); interIter !=  interInterEnd; interIter++){
        if((*interIter)->isIn(value)){
            std::pair<Interval *,  bool> retVal(*interIter,  true);
            return retVal;
        }
    }
    for(interIter = intervals.begin(),  interInterEnd = intervals.end(); interIter !=  interInterEnd; interIter++){
        if(((unsigned int)abs((*interIter)->lowerBound - value)) < limit || ((unsigned int)abs((*interIter)->upperBound - value)) < limit){
            std::pair<Interval *,  bool> retVal(*interIter,  true);
            return retVal;
        }
    }
    
    //Ok,  if I'm here it means that I have to create a new interval and return it
    Interval * newInter = new Interval(value,  value);
    std::pair<Interval *,  bool> retVal(newInter,  false);
    return retVal;
}
