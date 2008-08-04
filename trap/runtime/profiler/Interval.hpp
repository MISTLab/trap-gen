#ifndef INTERVAL_HPP
#define INTERVAL_HPP

#include <set>
#include <string>

namespace resp{

struct Interval{
  private:
    unsigned int lowerBound;
    unsigned int upperBound;
    unsigned int id;
  public:
    Interval();
    Interval(unsigned int lowerBound,  unsigned int upperBound);
    bool isIn(unsigned int toFind) const;
    bool operator() (const Interval& a, const Interval& b) const;
    std::string dump() const;
    unsigned int getId() const;
    unsigned int getCenter() const;
    void update(unsigned int newAddr);
    static std::string dumpIntervals();
    static std::pair<Interval *,  bool> getInterval(unsigned int value,  unsigned int limit);
};

extern Interval * nullInterval;

}

#endif
