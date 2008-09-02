#ifndef CUSTOMEXCEPTION_HPP
#define CUSTOMEXCEPTION_HPP

#include <exception>
#include <stdexcept>

class flush_exception: public std::runtime_error{
    flush_exception() : std::runtime_error(""){}
    flush_exception(const char * message) : std::runtime_error(message){}
};

#endif
